#chat.py
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import tempfile
from dotenv import load_dotenv
from document_loader import load_and_split_pdf
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

qa_chain = None
chat_history = []  
@app.route("/", methods=["GET", "POST"])
def index():
    global qa_chain, chat_history
    answer = None
    message = None

    if request.method == "POST":
        if "quit" in request.form:
            qa_chain = None
            chat_history = []
            message = "Session cleared. Please upload a new document."
            doc_uploaded = False
            return render_template("chatbot.html", answer=answer, message=message, history=chat_history, doc_uploaded=doc_uploaded)

        if qa_chain is None:
            file = request.files["document"]
            if not file:
                message = "Please upload a document first."
                doc_uploaded = False
                return render_template("chatbot.html", answer=answer, message=message, history=chat_history, doc_uploaded=doc_uploaded)

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            chunks = load_and_split_pdf(file_path)
            embeddings = OpenAIEmbeddings()
            db = FAISS.from_documents(chunks, embeddings)
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
            message = "Document uploaded. You can now ask questions."

        question = request.form.get("question")
        if question:
            answer = qa_chain.run(question)
            chat_history.append({"question": question, "answer": answer})

    doc_uploaded = qa_chain is not None
    return render_template("chatbot.html", answer=answer, message=message, history=chat_history, doc_uploaded=doc_uploaded)

if __name__ == "__main__":
    app.run(debug=True)
