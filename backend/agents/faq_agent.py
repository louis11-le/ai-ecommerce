import os

from langchain.chains import RetrievalQA
from langchain_community.document_loaders import CSVLoader
from langchain_community.llms import HuggingFaceHub  # Updated LLM import
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings  # Updated embeddings import


def get_faq_agent():
    # Create embeddings using a free Hugging Face model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Check if vector store exists, if not create it
    if not os.path.exists("chroma_db"):
        # Load FAQ documents from CSV
        loader = CSVLoader(file_path="data/faq.csv")
        documents = loader.load()
        vectorstore = Chroma.from_documents(
            documents, embedding=embeddings, persist_directory="chroma_db"
        )
        vectorstore.persist()
    else:
        # Load existing vector store
        vectorstore = Chroma(
            persist_directory="chroma_db", embedding_function=embeddings
        )

    # Create a retriever from the vector store
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

    # Get the Hugging Face API token from the environment
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if hf_token is None:
        raise ValueError(
            "HUGGINGFACEHUB_API_TOKEN is not set. Please add it to your .env file."
        )

    # Use a free LLM from Hugging Face Hub (e.g., "distilgpt2", "gpt2") with the API token
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-base",  # QA-specific model
        huggingfacehub_api_token=hf_token,
        model_kwargs={"temperature": 0.1},
    )

    # Create and return the RetrievalQA chain (RAG)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain
