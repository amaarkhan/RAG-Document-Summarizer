from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader
)
import os

class RAGToolInput(BaseModel):
    filename: str = Field(..., description="Path to the document file")
    query: str = Field(..., description="The user query")

class RAGTool(BaseTool):
    name: str = "Document RAG Tool"
    description: str = "Tool to chunk documents, embed them, and retrieve relevant chunks for a query"
    args_schema: Type[BaseModel] = RAGToolInput

    def load_document(self, file_path: str):
        """Load document based on file extension with error handling"""
        try:
            if file_path.endswith(".pdf"):
                return PyMuPDFLoader(file_path).load()
            elif file_path.endswith(".txt"):
                return TextLoader(file_path, encoding='utf-8').load()
            elif file_path.endswith(".md"):
                return UnstructuredMarkdownLoader(file_path).load()
            elif file_path.endswith((".docx", ".doc")):
                return UnstructuredWordDocumentLoader(file_path).load()
            else:
                raise ValueError(f"Unsupported file format. Only PDF, TXT, DOCX, DOC, and MD are supported. Got: {file_path}")
        except Exception as e:
            raise Exception(f"Failed to load document '{file_path}': {str(e)}")

    def _run(self, filename: str, query: str) -> str:
        try:
            # Check if file exists
            if not os.path.exists(filename):
                return f"Error: File '{filename}' not found."
            
            docs = self.load_document(filename)
            if not docs:
                return "Error: No content could be extracted from the document."
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(docs)
            
            if not chunks:
                return "Error: No chunks could be created from the document."

            embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            db = FAISS.from_documents(chunks, embedder)
            retriever = db.as_retriever(search_kwargs={"k": 5})
            results = retriever.invoke(query)

            if not results:
                return "No relevant content found for the given query."

            return "\n\n".join([doc.page_content for doc in results[:5]])
        
        except Exception as e:
            return f"Error processing document: {str(e)}"
