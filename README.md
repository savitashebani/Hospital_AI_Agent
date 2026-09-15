# 🏥 Hospital Management AI Agent

A GenAI-powered Hospital Management System built using Python, Streamlit, LangChain, RAG, LLMs, and AI Agents.

The application provides hospital management features along with an AI Assistant that can retrieve information from hospital documents and interact with hospital tools.

## 🚀 Features

* Patient management
* Doctor management
* Appointment booking
* Appointment cancellation
* Appointment retrieval
* Doctor search by specialization
* AI-powered hospital assistant
* Retrieval-Augmented Generation (RAG)
* Document-based question answering
* AI Agent with tool calling
* Vector search using Chroma
* Streamlit web interface

## 🛠️ Technologies Used

* Python
* Streamlit
* LangChain
* LangGraph / AI Agents
* Groq LLM
* RAG
* Hugging Face Embeddings
* ChromaDB
* SQLite
* Sentence Transformers

## 🧠 Generative AI Components

### RAG

The project uses Retrieval-Augmented Generation to answer questions based on hospital information stored in documents.

The RAG pipeline includes:

```text
Hospital Knowledge Document
        ↓
Text Splitting
        ↓
Embeddings
        ↓
Chroma Vector Database
        ↓
Similarity Search
        ↓
Relevant Context
        ↓
LLM
        ↓
Answer
```

## 🤖 AI Agent

The application uses a LangChain AI Agent with a Groq-hosted LLM and
tool calling to perform hospital management operations.

The agent can:

- Find doctors by specialization
- Find doctors by name
- Find patients
- Find patients by name
- Book appointments
- Cancel appointments
- Reschedule appointments
- Retrieve upcoming appointments
- Retrieve complete appointment history
- Retrieve patient-specific appointments

The agent uses the appropriate tool based on the user's request and
returns the tool result as a natural-language response.
## 🏗️ Architecture

```text
User
  ↓
Streamlit UI
  ↓
LangChain AI Agent
  ↓
Groq LLM
  ↓
Tool Calling
  ↓
Hospital Management Tools
  ↓
SQLite Database
  ↓
Tool Result
  ↓
AI Agent
  ↓
Final Response

## 📁 Project Structure

```text
Hospital_AI_Agent/
│
├── app.py
├── agent.py
├── tools.py
├── database.py
├── models.py
├── rag.py
├── hospital_knowledge.txt
├── requirements.txt
├── README.md
└── .gitignore
```

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/savitashebani/Hospital_AI_Agent.git
```

### 2. Open the project

```bash
cd Hospital_AI_Agent
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the API key

Create a `.env` file and add your Groq API key:

```text
GROQ_API_KEY=your_api_key_here
```

**Never commit your `.env` file or API keys to GitHub.**

### 7. Run the application

```bash
streamlit run app.py
```

## 📌 Project Purpose

This project demonstrates how Generative AI can be integrated with a traditional hospital management application.

It combines:

* Python application development
* Database operations
* LLM integration
* Retrieval-Augmented Generation
* Vector databases
* AI Agents
* Tool calling

## 👩‍💻 Author

Savita R Shebani

Software Engineer
