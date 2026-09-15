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

### 🔎 Retrieval-Augmented Generation (RAG)

The project uses Retrieval-Augmented Generation (RAG) to answer
hospital-related questions using information stored in a hospital
knowledge document.

The RAG pipeline includes:

1. Load hospital knowledge from `hospital_knowledge.txt`
2. Split the document using `RecursiveCharacterTextSplitter`
3. Generate embeddings using Hugging Face
   `sentence-transformers/all-MiniLM-L6-v2`
4. Store document embeddings in Chroma vector database
5. Retrieve the top 2 relevant document chunks
6. Pass the retrieved context to the Groq LLM
7. Generate an answer using the retrieved hospital information

### 🏗️ RAG Architecture

```text
Hospital Knowledge Document
        ↓
Text Splitting
        ↓
Hugging Face Embeddings
        ↓
Chroma Vector Database
        ↓
Retriever
        ↓
Top 2 Relevant Chunks
        ↓
Context + User Question
        ↓
Groq LLM
        ↓
Final Answer
```

### 💡 Example Query

```text
User:
What are the hospital timings?

        ↓

Retriever:
Finds relevant information from hospital_knowledge.txt

        ↓

LLM:
Generates the answer using the retrieved context

        ↓

Assistant:
The hospital is open from 9:00 AM to 6:00 PM,
Monday to Saturday.
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

## 🏗️ AI Agent Architecture

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
```

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
