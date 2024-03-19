import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage 
from chat_utils import get_vectorstore_and_BM25, get_response, get_text_chunks, get_pdf_text
from summarize import build_final_context, Prompts, summarize_chunk
from openai import OpenAI
import queue
import threading


def main():

    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:")
    st.header("Chat with Multiple PDFs :books:")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I'm a bot. How can I help you today?"),
        ]

    with st.sidebar:

        st.subheader("Your documents")  
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click in 'Process'", 
            accept_multiple_files=True)  
        
        process_button = st.button("Process")
        uploaded = pdf_docs
        
        if process_button:
            if not uploaded:
                st.warning("Please upload PDFs first.")
            else:
                with st.spinner("Processing..."):
                    st.session_state.vector_store, st.session_state.bm25_retriever = get_vectorstore_and_BM25(pdf_docs)

        if st.button("Summarize"):

            if "vector_store" in st.session_state:
                with st.spinner("Summarizing"):

                    if "chunks" not in st.session_state:
                        st.session_state.chunks = get_text_chunks(get_pdf_text(pdf_docs))

                    llm = OpenAI(api_key=openai_api_key)
                    results_queue = queue.Queue()  

                    threads = []
                    for chunk in st.session_state.chunks:
                        thread = threading.Thread(target=summarize_chunk, args=(chunk, results_queue, llm))
                        thread.start()
                        threads.append(thread)

                    for thread in threads:
                        thread.join()

                    summarize_chunks = []
                    while not results_queue.empty():
                        summarize_chunks.append(results_queue.get())

                context = build_final_context(summarize_chunks)
                message = [{"role": "user", "content": Prompts.final_ans_prompt(context)}]

                final_response = llm.chat.completions.create(model='gpt-3.5-turbo',
                    messages= message,
                    temperature=0.1,
                    max_tokens=4096)
                
                st.write(final_response.choices[0].message.content)

            else:
                if not uploaded:
                    st.warning("Please upload PDFs first.")
                else:
                    st.warning("Please process the PDFs.")


    user_query = st.chat_input("Type your mesage here ...")

    if user_query is not None and user_query != "":
        # Check if PDF files have been uploaded
        if not uploaded:
            st.warning("Please upload PDFs first.")
        # Check if PDF files have been processed
        elif "vector_store" not in st.session_state:
            st.warning("Please process the PDFs.")
        else:
            # Get response from the model based on user's message
            response = get_response(user_query, st.session_state.bm25_retriever)
            # Append user's message and response to the chat history
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=response))


    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message,  HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)


if __name__ == '__main__':
    main()