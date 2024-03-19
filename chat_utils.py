import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.retrievers import BM25Retriever, EnsembleRetriever



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(raw_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(raw_text)

    return chunks


def get_vectorstore_and_BM25(pdf_docs):
    raw_text = get_pdf_text(pdf_docs)
    
    text_chunks = get_text_chunks(raw_text)
    emb_model = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=emb_model)

    bm25_retriever = BM25Retriever.from_texts(texts=text_chunks, embedding=emb_model)
    return vectorstore, bm25_retriever     


def get_context_retriever_chain(vectorstore, bm25_retriever, k=2):

    bm25_retriever.k = k

    llm = ChatOpenAI()
    faiss_retriever = vectorstore.as_retriever()

    ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5])

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    retriever_chain = create_history_aware_retriever(llm, ensemble_retriever, prompt)

    return retriever_chain


def get_conversational_rag_chain(retriever_chain):   

    llm = ChatOpenAI()  
    prompt = ChatPromptTemplate.from_messages([
      ("system", "Answer the user's questions based on the below context:\n\n{context}"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
    ])  
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)


def get_response(user_query, bm25_retriever):

    retriever_chain = get_context_retriever_chain(st.session_state.vector_store, bm25_retriever)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    response = conversation_rag_chain.invoke({
            "chat_history": st.session_state.chat_history,
            "input": user_query
        })
    
    return response["answer"]