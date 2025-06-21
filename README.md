# 🤖 DocuQuery: Document Q&A Assistant

**DocuQuery** is an intelligent, user-friendly web application that enables you to ask questions about your PDF documents using natural language. Built with **LangChain**, **FAISS**, and **OpenAI's GPT-3.5**, it brings RAG (Retrieval-Augmented Generation) to life in a clean Flask UI with full session handling, chat history, and document awareness.

---

## 🚀 Features

- 🔐 Securely input your own **OpenAI API key** (no hardcoded keys)
- 📄 Upload a **PDF document** to be indexed
- 💬 Ask **multiple natural language questions** about your document
- 🧠 Get answers grounded in your uploaded content using **GPT-3.5**
- 📜 View **chat history** for session context
- 🌙 Toggle **light/dark mode** for a better user experience
- 🔄 Option to **reset session** at any time

---

## 🧠 How It Works

1. **PDF Upload**

   - Document is uploaded via a secure form
   - Parsed using `PyMuPDFLoader` and split into chunks via `RecursiveCharacterTextSplitter`

2. **Vector Embedding & Indexing**

   - Chunks are embedded using `OpenAIEmbeddings`
   - Embedded vectors are indexed using **FAISS** for fast similarity search

3. **Retrieval + QA**

   - A `RetrievalQA` chain is set up with **ChatOpenAI**
   - Questions are matched with relevant document chunks
   - GPT-3.5 generates context-aware, accurate answers

4. **Web Interface**

   - Built with **Flask + Bootstrap**
   - Handles API key entry, file uploads, chat flow, and session state
   - Displays real-time question–answer pairs with chat history

---

## 🖼️ Demo

🎥 [Click here to watch the demo video](demo/chatbotdemo.mp4)


---

## 📦 Tech Stack

- **Backend**: Python, Flask, LangChain, FAISS
- **Frontend**: HTML, CSS (Bootstrap 5)
- **AI**: OpenAI GPT-3.5 (via LangChain)
- **Document Handling**: PyMuPDFLoader
- **Deployment**: AWS EC2, NGINX, Gunicorn, systemd

---

## 🛠️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/SakethRamkalavakuntla/Doc-QA-chatbot.git
cd Doc-QA-chatbot
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run locally**

```bash
python chatbotapi.py
```

5. **Navigate to**

```
http://127.0.0.1:5000
```

---

## 🌐 Deployment

Deployed on **AWS EC2** with:

- Reverse proxy using **NGINX**
- WSGI app server using **Gunicorn**
- Background service managed by **systemd**

Elastic IP is configured to keep a consistent endpoint.

---

## 🎯 Use Cases

- Academic research document exploration
- Legal and financial document querying
- Company policies/manuals Q&A
- Any large PDF-based knowledge retrieval

---

## ✅ To-Do (Optional Features)

- ✅ Chat persistence across reloads
- 🔒 Document encryption or authentication layer
- 🧾 Support for multiple file formats (DOCX, TXT)
- 📁 Multi-document handling
- 📊 Upload analytics/logs

---

## 🙋 FAQ

**Q: Is my document stored on your server?**

> No. Files are temporarily stored only for processing and discarded afterward.

**Q: Do you store my API key?**

> No. Your API key is stored in the session and not persisted.

**Q: Can I use another model like Claude or Gemini?**

> Currently the app is built with LangChain + OpenAI, but can be extended to support other providers.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT License](LICENSE)

---

## 👤 Author

**Saketh Ram Kalavakuntla**\
[GitHub](https://github.com/SakethRamkalavakuntla)\
[LinkedIn](https://www.linkedin.com/in/saketh-ram-kalavakuntla)

