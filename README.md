# YouTubeChatBot 

AI chatbot that answers questions  or summary based on YouTube video transcripts .A conversational AI chatbot that interacts with YouTube transcripts and documents using semantic search and retrieval-augmented generation (RAG). Built with FAISS, LangChain and HuggingFaceEmbeddings, this project enables intelligent Q&A   and video summary over YouTube transcripts content.

## Features
- Extracts transcripts
- LLM-powered Q&A
- Streamlit UI
-  Semantic text splitting and embedding
-  FAISS vector store for similarity search
-  Text ingestion
-  Chat interface powered by RAG
## Setup
```bash
git clone https://github.com/iaksaurya/YouTubeChatBot.git
cd YouTubeChatBot
python -m venv YouTubeChatBot
# Activate env (Windows)
YouTubeChatBot\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
