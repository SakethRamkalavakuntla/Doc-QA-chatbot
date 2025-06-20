from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import os
import tempfile
from document_loader import load_and_split_pdf
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

app = Flask(__name__)
app.secret_key = "supersecret"
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

qa_chain = None
chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    global qa_chain, chat_history
    answer = None
    message = None

    if request.method == "POST":
        user_api_key = request.form.get("api_key")
        if user_api_key:
            session["api_key"] = user_api_key
            message = "API key saved. You can now upload a document."

        if "quit" in request.form:
            qa_chain = None
            chat_history = []
            session.pop("api_key", None)
            message = "Session cleared. Please enter your OpenAI API key again."
            return render_template("chatbotapi.html", answer=None, message=message, history=[], doc_uploaded=False, has_key=False)

        if "api_key" not in session:
            message = "Please enter your OpenAI API key."
            return render_template("chatbotapi.html", answer=None, message=message, history=[], doc_uploaded=False, has_key=False)

        if qa_chain is None:
            file = request.files.get("document")
            if not file:
                message = "Please upload a document first."
                return render_template("chatbotapi.html", answer=None, message=message, history=chat_history, doc_uploaded=False, has_key=True)

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            chunks = load_and_split_pdf(file_path)

            embeddings = OpenAIEmbeddings(openai_api_key=session["api_key"])
            db = FAISS.from_documents(chunks, embeddings)
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=session["api_key"])
            qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

            message = "Document uploaded. You can now ask questions."

        question = request.form.get("question")
        if question:
            answer = qa_chain.run(question)
            chat_history.append({"question": question, "answer": answer})

    return render_template("chatbotapi.html", answer=answer, message=message, history=chat_history,
                           doc_uploaded=qa_chain is not None, has_key="api_key" in session)

if __name__ == "__main__":
    app.run(debug=True)
