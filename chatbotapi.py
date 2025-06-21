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

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    message = None

    if request.method == "POST":
        if "quit" in request.form:
            session.clear()
            message = "Session cleared. Please enter your API key."
            return render_template("chatbotapi.html", answer=None, message=message, history=[], has_key=False, doc_uploaded=False)

        # Save API key
        if "api_key" in request.form:
            session["api_key"] = request.form.get("api_key")
            message = "API key saved. Upload a document."

        # Handle PDF upload
        elif "document" in request.files:
            file = request.files["document"]
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                session["file_path"] = file_path
                message = "Document uploaded. Ask your question."
                session["chat_history"] = []

        # Handle Question
        elif "question" in request.form:
            if "api_key" in session and "file_path" in session:
                chunks = load_and_split_pdf(session["file_path"])
                embeddings = OpenAIEmbeddings(openai_api_key=session["api_key"])
                db = FAISS.from_documents(chunks, embeddings)
                llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=session["api_key"])
                qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

                question = request.form.get("question")
                answer = qa_chain.run(question)

                history = session.get("chat_history", [])
                history.append({"question": question, "answer": answer})
                session["chat_history"] = history

            else:
                message = "Missing API key or document."

    return render_template("chatbotapi.html",
                           answer=answer,
                           message=message,
                           history=session.get("chat_history", []),
                           has_key="api_key" in session,
                           doc_uploaded="file_path" in session)

if __name__ == "__main__":
    app.run(debug=True)
