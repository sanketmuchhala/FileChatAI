import streamlit as st
import os
from document_processor import DocumentProcessor
from vector_store import VectorStore
from chat_handler import ChatHandler

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "document_processed" not in st.session_state:
    st.session_state.document_processed = False
if "chat_handler" not in st.session_state:
    st.session_state.chat_handler = None

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Document Chatbot")
st.markdown("Upload a document and chat with its content using DeepSeek AI and Google Gemini embeddings.")

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Document Upload")
    
    # Check for API keys
    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    
    if not deepseek_key or not gemini_key:
        st.error("⚠️ Missing API keys. Please set DEEPSEEK_API_KEY and GEMINI_API_KEY environment variables.")
        if not deepseek_key:
            st.info("• DeepSeek API key needed for chat responses")
        if not gemini_key:
            st.info("• Google Gemini API key needed for document processing")
        st.stop()
    
    uploaded_file = st.file_uploader(
        "Choose a document",
        type=['pdf', 'txt', 'docx'],
        help="Upload a PDF, TXT, or DOCX file to chat with its content"
    )
    
    if uploaded_file is not None:
        # Show file details
        st.write(f"**File:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size} bytes")
        st.write(f"**Type:** {uploaded_file.type}")
        
        # Process document button
        if st.button("🔄 Process Document", type="primary"):
            with st.spinner("Processing document..."):
                try:
                    # Initialize document processor
                    processor = DocumentProcessor()
                    
                    # Extract text from document
                    text = processor.extract_text(uploaded_file)
                    
                    if not text.strip():
                        st.error("❌ No text content found in the document.")
                        st.stop()
                    
                    # Chunk the text
                    chunks = processor.chunk_text(text)
                    
                    if not chunks:
                        st.error("❌ Failed to create text chunks from the document.")
                        st.stop()
                    
                    # Create vector store with Gemini API
                    vector_store = VectorStore(gemini_key)
                    vector_store.add_documents(chunks)
                    
                    # Initialize chat handler with DeepSeek API
                    chat_handler = ChatHandler(deepseek_key, vector_store)
                    
                    # Store in session state
                    st.session_state.vector_store = vector_store
                    st.session_state.chat_handler = chat_handler
                    st.session_state.document_processed = True
                    st.session_state.messages = []  # Clear previous messages
                    
                    st.success(f"✅ Document processed successfully! Created {len(chunks)} text chunks.")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
    
    # Document status
    if st.session_state.document_processed:
        st.success("✅ Document ready for chat")
        if st.button("🗑️ Clear Document"):
            st.session_state.vector_store = None
            st.session_state.chat_handler = None
            st.session_state.document_processed = False
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("📤 Upload and process a document to start chatting")

# Main chat interface
if st.session_state.document_processed and st.session_state.chat_handler:
    st.header("💬 Chat with your document")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show source chunks for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📄 Source chunks used"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**Chunk {i}:**")
                        st.markdown(f"```\n{source}\n```")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your document..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response, sources = st.session_state.chat_handler.generate_response(prompt)
                    st.markdown(response)
                    
                    # Show source chunks
                    if sources:
                        with st.expander("📄 Source chunks used"):
                            for i, source in enumerate(sources, 1):
                                st.markdown(f"**Chunk {i}:**")
                                st.markdown(f"```\n{source}\n```")
                    
                    # Add assistant message to chat
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                
                except Exception as e:
                    error_msg = f"❌ Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })

else:
    # Show welcome message when no document is processed
    st.header("👋 Welcome to RAG Document Chatbot")
    st.markdown("""
    This application allows you to upload documents and have natural language conversations about their content using AI.
    
    **How it works:**
    1. 📤 Upload a document (PDF, TXT, or DOCX) using the sidebar
    2. 🔄 Click "Process Document" to analyze and index the content with Google Gemini
    3. 💬 Start asking questions about your document
    4. 🤖 Get AI-powered answers from DeepSeek with relevant source excerpts
    
    **Features:**
    - Support for multiple document formats
    - Google Gemini embeddings for accurate document understanding
    - DeepSeek AI for intelligent, cost-effective responses
    - Context-aware responses using retrieval augmented generation
    - Source citation showing which parts of the document were used
    - Persistent chat history during your session
    
    Get started by uploading a document in the sidebar! 👈
    """)
