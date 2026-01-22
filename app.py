import streamlit as st
from transcripts import fetch_and_save_transcripts
from chain import chain_model

# Page Config
st.set_page_config(
    page_title="YouTube Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title(" YouTube ChatBot")
    st.markdown(
        """
        **How it works**
        1. Enter a YouTube video ID  
        2. Fetch the transcript  
        3. Ask questions from the video  
        """
    )
    st.divider()
    st.caption("Built with Streamlit")

# Main Title
st.markdown(
    "<h1 style='text-align: center;'> YouTube Transcript Generator & Chatbot</h1>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# Video ID Input Section
with st.container():
    st.subheader(" Step 1: Enter Video ID")

    col1, col2 = st.columns([4, 1])

    with col1:
        video_id = st.text_input(
            "YouTube Video ID",
            placeholder="e.g. H4gZd4BCrDQ",
            label_visibility="collapsed"
        )

    with col2:
        fetch_btn = st.button(" Fetch Transcript", use_container_width=True)

    if fetch_btn:
        if not video_id:
            st.warning(" Please enter a valid video ID")
        else:
            with st.spinner("Fetching transcript..."):
                transcript = fetch_and_save_transcripts(video_id)

            if transcript is None:
                st.error(" No captions available for this video")
            else:
                st.success(" Transcript fetched successfully")
                st.session_state.transcript = transcript

# Transcript Display
if "transcript" in st.session_state:
    with st.expander(" View Transcript", expanded=True):
        st.text_area(
            label="",
            value=st.session_state.transcript,
            height=350
        )

# Question Section
st.markdown("<br>", unsafe_allow_html=True)
st.subheader(" Step 2: Ask a Question")

col3, col4 = st.columns([4, 1])

with col3:
    question = st.text_input(
        "Ask your question",
        placeholder="What is this video about?",
        label_visibility="collapsed"
    )

with col4:
    answer_btn = st.button(" Get Answer", use_container_width=True)

# Answer Section
if answer_btn:
    if not question:
        st.warning(" Please enter a question")
    else:
        with st.spinner("Thinking... "):
            get_answer = chain_model(question)

        if get_answer is None:
            st.error(" Answer not found")
        else:
            st.success("Answer generated")
            st.session_state.answer = get_answer

if "answer" in st.session_state:
    with st.expander(" Answer", expanded=True):
        st.text_area(
            label="",
            value=st.session_state.answer,
            height=250
        )
