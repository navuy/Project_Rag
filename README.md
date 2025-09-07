# 🚀 Project RAG

> **A Retrieval-Augmented Generation (RAG) system with FastAPI backend and Flask UI. Store project data in ChromaDB, use SentenceTransformers for embeddings, and LLaMA API for contextual answers.**

## 📋 Table of Contents
- [🌟 Overview](#overview)
- [🏗️ Architecture](#architecture)  
- [✨ Features](#features)
- [🔧 Prerequisites](#prerequisites)
- [⚡ Quick Start](#quick-start)
- [🐳 Docker Deployment](#docker-deployment)
- [🔌 API Usage](#api-usage)
- [🎨 Frontend Interface](#frontend-interface)
- [⚙️ Configuration](#configuration)
- [🤝 Contributing](#contributing)

## 🌟 Overview

Project RAG is a modern Retrieval-Augmented Generation system that combines the power of document retrieval with large language models to provide contextual, intelligent responses about your project data. The system consists of two main components working in harmony:

### Backend Architecture
- **FastAPI Service**: High-performance API backend
- **ChromaDB**: Vector database for document storage and retrieval
- **SentenceTransformers**: Advanced embedding generation
- **LLaMA Integration**: Powered by Together API for contextual responses

### Frontend Experience  
- **Flask Web UI**: Clean, intuitive web interface
- **Matrix-Style Terminal**: Cyberpunk-inspired design
- **Project Selection**: Easy project navigation
- **Interactive Chat**: Real-time AI conversations

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask UI      │◄──►│   FastAPI       │◄──►│   ChromaDB      │
│   (Port 5000)   │    │   (Port 8001)   │    │   Vector Store  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ SentenceTransf. │
                       │ + LLaMA API     │
                       └─────────────────┘
```

## ✨ Features

### 🎯 Core Capabilities
- **Document Ingestion**: Store and index project documents
- **Semantic Search**: Find relevant information using vector similarity
- **Context-Aware Responses**: Generate answers with project-specific context
- **Real-time Chat**: Interactive conversational interface
- **Multi-Project Support**: Manage multiple project contexts

### 🎨 User Interface
- **Cyberpunk Theme**: Matrix-inspired terminal design
- **Responsive Design**: Works on desktop and mobile
- **Project Selector**: Easy switching between projects
- **Chat History**: Persistent conversation tracking

### 🔧 Technical Features
- **FastAPI Backend**: High-performance async API
- **ChromaDB Integration**: Efficient vector storage and retrieval
- **Sentence Transformers**: State-of-the-art embeddings
- **Docker Support**: Easy deployment and scaling

## 🔧 Prerequisites

Before getting started, ensure you have the following installed:

- **Python 3.8+**
- **pip** (Python package installer)
- **Docker** (optional, for containerized deployment)
- **Git** (for cloning the repository)

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/navuy/Project_Rag.git
cd Project_Rag
```

### 2. Backend Setup

#### Install Dependencies
```bash
pip install fastapi uvicorn sentence-transformers chromadb requests
```

#### Start the Backend Server
```bash
cd rag_git
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

**Backend will be available at:** `http://127.0.0.1:8001`

### 3. Frontend Setup

#### Install Dependencies
```bash
pip install flask requests
```

#### Start the Frontend Server
```bash
cd rag_git/rag-ui
python app.py
```

**Frontend will be available at:** `http://127.0.0.1:5000`

## 🐳 Docker Deployment

> **Recommended Method**: Use Docker for easy deployment and consistent environments

Docker files are provided for both backend and frontend components. This ensures:
- ✅ Consistent environment across different systems
- ✅ Easy scaling and deployment  
- ✅ Isolated dependencies
- ✅ Production-ready setup

```bash
# Build and run with Docker Compose (recommended)
docker-compose up --build
```

## 🔌 API Usage

### Ask a Question
Send queries to your project context using the REST API:

```bash
curl -X POST "http://127.0.0.1:8001/ask/my_project" \
     -H "Content-Type: application/json" \
     -d '{"query": "explain login logic?"}'
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask/{project_id}` | POST | Ask a question about a specific project |
| `/projects` | GET | List all available projects |
| `/health` | GET | Health check endpoint |

### Request Format
```json
{
  "query": "Your question here",
  "context_limit": 5,
  "temperature": 0.7
}
```

### Response Format
```json
{
  "answer": "AI-generated response with context",
  "sources": ["document1.txt", "document2.py"],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🎨 Frontend Interface

### Matrix-Style Terminal
The web UI features a cyberpunk-inspired design reminiscent of the Matrix:
- **Green text on black background**
- **Terminal-like command interface**
- **Smooth typing animations**
- **Project selection dropdown**

### Usage Flow
1. **Select Project**: Choose from available projects in dropdown
2. **Ask Questions**: Type your queries in the terminal
3. **Get Responses**: Receive contextual AI-powered answers
4. **Continue Conversation**: Build on previous context

## ⚙️ Configuration

### Backend Configuration
Edit `rag-api/config.py` or environment variables:

```python
# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8001

# ChromaDB Settings  
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "project_docs"

# LLaMA API Settings
TOGETHER_API_KEY = "your_api_key_here"
MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
```

### Frontend Configuration
Edit `rag-ui/app.py`:

```python
# Backend API URL
API_BASE_URL = "http://127.0.0.1:8001"

# UI Settings
DEBUG = False
HOST = "127.0.0.1" 
PORT = 5000
```

### Environment Variables
```bash
# Backend
export TOGETHER_API_KEY="your_api_key"
export CHROMA_DB_PATH="./data/chroma_db"

# Frontend  
export API_BASE_URL="http://backend:8001"
```

## 🛠️ Development

### Project Structure
```
Project_Rag/
├── rag_git/
│   ├── main.py              # FastAPI backend
│   ├── models/              # Data models
│   ├── services/            # Business logic
│   └── rag-ui/
│       ├── app.py          # Flask frontend
│       ├── templates/      # HTML templates
│       └── static/         # CSS, JS assets
├── docker-compose.yml       # Container orchestration
├── Dockerfile.backend      # Backend container
├── Dockerfile.frontend     # Frontend container
└── README.md              # This file
```

### Adding New Features
1. **Backend**: Add endpoints in `main.py` and logic in `services/`
2. **Frontend**: Update templates and routes in `app.py`
3. **Database**: Extend ChromaDB collections as needed

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Ensure Docker builds pass

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

Having issues? Here are some resources:

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the inline code documentation
- **Docker Logs**: Use `docker-compose logs` for troubleshooting

## 🔗 Related Projects

- [ChromaDB](https://www.trychroma.com/) - Vector database
- [SentenceTransformers](https://www.sbert.net/) - Embedding models
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python API framework
- [LLaMA](https://ai.meta.com/llama/) - Large Language Model

---

**Built with ❤️ by [navuy](https://github.com/navuy)**

*Ready to chat with your code? Get started now!* 🚀
