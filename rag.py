
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from rich import prompt

load_dotenv()

with open ("hospital_knowledge.txt","r") as file:
    text=file.read()
#print(text)

splitter=RecursiveCharacterTextSplitter(
   chunk_size=200,
    chunk_overlap=20
)
chunks=splitter.split_text(text)
for i,chunk in enumerate(chunks):
    print(f"\n chunk {i+1}")
    print(chunk)
embeddings=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
#vector=embeddings.embed_query(chunks[0]) #for single chunk
vector=embeddings.embed_documents(chunks)
print("number of chunks",len(vector))
print("vector size",len(vector[0]))

# Delete old collection if it exists
old_vectorstore = Chroma(
    collection_name="hospital_knowledge_v2",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

old_vectorstore.delete_collection()

vectorstore = Chroma.from_texts(
    texts=chunks,  #gives Chroma our 5 chunks
    embedding=embeddings,  #tells Chroma how to convert the text into vectors
    collection_name="hospital_knowledge_v2",
    persist_directory="./chroma_db" #saves the vector database on your computer
)
#Create Retriever
retriever=vectorstore.as_retriever(
    search_kwargs={"k":2}
)
 #Test Retriever


def ask_hospital_rag(query):

    results = retriever.invoke(query)
    for i, result in enumerate(results):
        print(f"\n--- Retrieved Chunk {i + 1} ---")
        print(result.page_content)

# Combine retrieved chunks
    context = "\n\n".join(doc.page_content for doc in results)

#Create LLM
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )
#Create prompt
    prompt = ChatPromptTemplate.from_template("""
    You are a hospital assistant.

    Answer the user's question using only the information
    provided in the context.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """)
    rag_chain=(
    {
        "context":retriever,
        "question":RunnablePassthrough()
    }
    |prompt
    |llm
)

# Generate answer
    response =rag_chain.invoke("What are the hospital timings?")
    print("\n--- Final Answer ---")
    return response.content





question = "What are the hospital timings?"

answer = ask_hospital_rag(question)

print(answer)