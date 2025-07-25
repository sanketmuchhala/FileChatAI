# RAG Document Chatbot

## Overview

This is a Retrieval-Augmented Generation (RAG) chatbot built with Streamlit that allows users to upload documents and interact with their content through natural language conversations. The system extracts text from uploaded documents, creates vector embeddings, and uses OpenAI's GPT models to provide contextually relevant responses based on the document content.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular architecture with separation of concerns across four main components:

1. **Frontend Layer**: Streamlit-based web interface for user interactions
2. **Document Processing Layer**: Handles text extraction from various file formats
3. **Vector Storage Layer**: Manages document embeddings and similarity search
4. **Chat Handler Layer**: Orchestrates AI-powered conversations with document context

The architecture uses a stateful session management approach where processed documents and chat history persist throughout the user session.

## Key Components

### Frontend (app.py)
- **Purpose**: Main Streamlit application entry point
- **Responsibilities**: UI rendering, file upload handling, session state management
- **Key Features**: Sidebar document upload, chat interface, error handling for missing API keys

### Document Processor (document_processor.py)
- **Purpose**: Text extraction and chunking from various document formats
- **Supported Formats**: PDF, TXT, DOCX
- **Chunking Strategy**: Fixed-size chunks with overlap to maintain context continuity
- **Default Settings**: 1000 character chunks with 200 character overlap

### Vector Store (vector_store.py)
- **Purpose**: Document embedding generation and similarity search
- **Embedding Model**: OpenAI's text embedding models
- **Storage**: In-memory storage using numpy arrays
- **Search Algorithm**: Cosine similarity for document retrieval

### Chat Handler (chat_handler.py)
- **Purpose**: Manages conversational AI interactions with document context
- **Model**: GPT-4o (OpenAI's latest model as of May 2024)
- **Context Strategy**: Retrieves top-k similar document chunks for each query
- **Response Generation**: Combines retrieved context with user queries for informed responses

## Data Flow

1. **Document Upload**: User uploads document through Streamlit sidebar
2. **Text Extraction**: DocumentProcessor extracts text based on file type
3. **Text Chunking**: Document is split into overlapping chunks for better retrieval
4. **Embedding Generation**: VectorStore creates embeddings for all chunks using OpenAI API
5. **Storage**: Embeddings and chunks stored in session state
6. **Query Processing**: User queries trigger similarity search against stored embeddings
7. **Context Retrieval**: Top-k most similar chunks retrieved as context
8. **Response Generation**: ChatHandler combines context with query to generate AI response
9. **Display**: Response and sources displayed in chat interface

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework
- **OpenAI**: API client for embeddings and chat completions
- **NumPy**: Numerical operations for vector similarity calculations

### Document Processing Dependencies
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing
- **Built-in io**: Text file handling

### API Requirements
- **OpenAI API Key**: Required environment variable (OPENAI_API_KEY)
- **Internet Connection**: Required for OpenAI API calls

## Deployment Strategy

### Environment Setup
- **API Configuration**: OpenAI API key must be set as environment variable
- **Dependency Management**: Standard Python requirements.txt approach
- **Session Management**: Streamlit's built-in session state for user data persistence

### Scalability Considerations
- **Memory Usage**: Current implementation stores all embeddings in memory
- **Session Isolation**: Each user session maintains independent document storage
- **API Rate Limits**: No built-in rate limiting for OpenAI API calls

### Security Features
- **API Key Protection**: Environment variable-based API key management
- **File Type Validation**: Restricted upload types (PDF, TXT, DOCX)
- **Error Handling**: Comprehensive exception handling for file processing and API calls

The application is designed for single-user sessions with ephemeral document storage, making it suitable for personal document analysis and exploration tasks.