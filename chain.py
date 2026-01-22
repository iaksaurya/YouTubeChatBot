from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def chain_model(question):
    

    # Load transcript file
    loader = TextLoader("transcripts.txt")
    documents = loader.load()   # List[Document]

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    # print(len(chunks))
    # print(chunks)

    #Embedding Generation and Storing in Vector Store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)

    #Retreival
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    # docs= retriever.invoke('What is AI Agents')

    # for i, doc in enumerate(docs, 1):
    #     print(f"\n--- Result {i} ---")
    #     print(doc.page_content)


    #Augmentation

    from langchain_google_genai import ChatGoogleGenerativeAI
    llm=ChatGoogleGenerativeAI(model='gemini-3-flash-preview')

        #prompt

    prompt = PromptTemplate(
        template="""
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you don't know.

        {context}
        Question: {question}
        """,
        input_variables = ['context', 'question']
    )


    #question= "Can you summarize the video?"
    #retrieved_docs    = retriever.invoke(question)



    def format_docs(retrieved_docs):
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
        return context_text


    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })


    #doc=parallel_chain.invoke(question)
    # print(doc)

    parser = StrOutputParser()

    main_chain = parallel_chain | prompt | llm | parser

    docs=main_chain.invoke(question)
    return docs