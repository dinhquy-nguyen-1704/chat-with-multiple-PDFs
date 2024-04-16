# chat-with-multiple-PDFs
## 1. Introduction
Building a chatbot that leverages Retrieval-Augmented Generation (RAG) with the Ensemble Retriever technique. It is engineered not only to summarize but also to facilitate Q&A interactions with the content of user-uploaded PDFs using the Langchain framework through a user-friendly Streamlit interface.
<p align="center">
  <img width="800" alt="Streamlit Interface" src="https://github.com/dinhquy-nguyen-1704/chat-with-multiple-PDFs/assets/127675330/c04580c5-d63e-4076-930d-350f0d520083">
</p>
<p align="center">
  <em>Streamlit Interface</em>
</p>

### Key features:

**🌟 RAG with Ensemble Retriever:** Utilizes the RAG technique with an Ensemble Retriever (Hybrid Search).

**🌟 Interact with PDFs:** The system allows interaction with multiple PDF files uploaded by users.

**🌟 Summarization:** Capable of summarizing and displaying the content of PDF files.

**🌟 Streamlit Interface:** The interface is designed with Streamlit, user-friendly and easy to use.

## 2. How to use?
### Getting Started
```
git clone https://github.com/dinhquy-nguyen-1704/chat-with-multiple-PDFs.git
cd chat-with-multiple-PDFs
```
```
conda create -n chat-with-multiple-PDFs python=3.9.6
conda activate chat-with-multiple-PDFs
```
```
pip install -r requirements.txt
```
### Using Streamlit
Add the OpenAI API KEY in the **.env** file.
```python
OPENAI_API_KEY=sk-...
```
Then, you can run the **app.py** file and a Streamlit interface will appear.
```
python -m streamlit run app.py
```
> I have prepared a Vietnamese PDF file in the **sample** folder for you to test.
### Run on Colab
I have also provided you with a Google Colab Notebook for the convenience of running code, you just need to replace your OPEN_AI_API in the .env file.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1okCM7CxL4oDdivlG4nrjy37Hn-_Azimq?authuser=1#scrollTo=eHzY-ciU0-tK)
