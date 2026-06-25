# 🚀 RAG-Powered Intelligent Document Search

A production-ready, full-stack application for intelligent document search using **RAG (Retrieval-Augmented Generation)** with TF-IDF embeddings and vector storage.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)

---

## 📖 About This Project

This application allows you to upload documents and search through them using natural language. It uses TF-IDF (Term Frequency-Inverse Document Frequency) to create embeddings and find the most relevant documents based on your queries.

### How It Works:
1. 📄 **Upload** - Upload text documents (TXT, PDF, DOCX, Images)
2. 🧩 **Process** - Documents are split into chunks for better search
3. 🔢 **Embed** - Each chunk gets a mathematical representation (TF-IDF)
4. 💾 **Store** - Embeddings are stored in memory for fast retrieval
5. 🔍 **Search** - Query using natural language, get ranked results

---

## ✨ Features

- 📄 **Document Upload** - Support for TXT, PDF, DOCX, DOC, and Images (with OCR)
- 🔍 **Semantic Search** - Search using natural language, not just keywords
- 📊 **Relevance Scoring** - Each result shows how relevant it is (0-100%)
- 🎨 **Web Interface** - Clean, modern UI for upload and search
- 🚀 **FastAPI Backend** - High-performance async API
- 📚 **API Documentation** - Automatic Swagger/OpenAPI docs
- 🐳 **Docker Support** - Easy deployment with Docker Compose
- 📈 **System Stats** - Monitor your document collection

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework for building APIs |
| **TF-IDF** | Embedding generation (scikit-learn) |
| **Python 3.10+** | Programming language |
| **SQLAlchemy** | ORM for database operations |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure |
| **CSS3** | Styling and responsiveness |
| **JavaScript** | Interactivity and API calls |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |

---

## 📋 Prerequisites

- **Python 3.10+**
- **Docker & Docker Compose** (optional, recommended)
- **Git** (for cloning)

---

## 🚀 Quick Start

### Option 1: Docker (Recommended - Easiest)

```bash
# Clone the repository
git clone https://github.com/pallavi-dhadage/RAG-Powered-Intelligent-Document-Search.git
cd RAG-Powered-Intelligent-Document-Search

# Start all services
docker compose up -d --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/pallavi-dhadage/RAG-Powered-Intelligent-Document-Search.git
cd RAG-Powered-Intelligent-Document-Search

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend Setup (in new terminal)
cd frontend
python -m http.server 3000
```

---

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/api/documents/upload` | Upload a document | Multipart form with file |
| `GET` | `/api/documents/` | List all documents | - |
| `DELETE` | `/api/documents/{id}` | Delete a document | - |
| `POST` | `/api/search/` | Search documents | `{"query": "text", "top_k": 5}` |
| `GET` | `/api/documents/stats` | Get system statistics | - |
| `GET` | `/health` | Health check | - |

### Example Requests

**Upload a document:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@document.txt" \
  -F "title=My Document"
```

**Search:**
```bash
curl -X POST "http://localhost:8000/api/search/" \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "top_k": 5}'
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

---

## 📁 Project Structure

```
RAG-Powered-Intelligent-Document-Search/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── documents.py      # Document upload/delete endpoints
│   │   │   └── search.py         # Search endpoint
│   │   ├── utils/
│   │   │   └── file_handlers.py  # File handling utilities
│   │   ├── config.py             # Configuration
│   │   ├── database.py           # Database setup
│   │   ├── document_processor.py # Text extraction and chunking
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── rag_engine.py         # RAG engine with TF-IDF
│   │   └── main.py               # Application entry point
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Docker configuration
│   └── .env.example              # Environment variables template
├── frontend/
│   ├── index.html                # Web interface
│   └── Dockerfile                # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
├── .gitignore                    # Git ignore file
├── LICENSE                       # MIT License
└── README.md                     # This file
```

---

## 🔧 Configuration

Create a `.env` file in the `backend` directory:

```env
# API Settings
APP_NAME=RAG Document Search
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///./rag.db

# Model Settings
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=.pdf,.txt,.docx,.doc

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## 🧪 Testing

### Test the Application

```bash
# Health check
curl http://localhost:8000/health

# Upload a document
echo "Testing RAG document search with AI" > test.txt
curl -X POST "http://localhost:8000/api/documents/upload" -F "file=@test.txt"

# Search
curl -X POST "http://localhost:8000/api/search/" \
  -H "Content-Type: application/json" \
  -d '{"query": "AI", "top_k": 3}'

# Get statistics
curl http://localhost:8000/api/documents/stats
```

### Complete Test Script

```bash
#!/bin/bash
# Run all tests
./test_api.sh
```

---

## 📱 Using the Web Interface

1. **Upload Documents**
   - Click the "Upload" tab
   - Drag and drop files or click to select
   - Click "Upload Document"

2. **Search**
   - Click the "Search" tab
   - Enter your query
   - Select number of results
   - Click "Search"

3. **View Statistics**
   - Click the "Stats" tab
   - Click "Refresh" to update

---

## 🐳 Docker Deployment

### Build and Run

```bash
# Build and start all services
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Production Deployment

```bash
# Create production .env
cp backend/.env.example backend/.env.production
# Update with production values

# Deploy
docker compose --env-file backend/.env.production up -d
```

---

## 🔒 Security Considerations

- Use strong `SECRET_KEY` in production
- Enable HTTPS (use nginx or cloud load balancer)
- Sanitize file uploads (validate file types and sizes)
- Use environment variables for sensitive data
- Regular updates for dependencies

---

## 📈 Performance Optimization

- Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP` for better retrieval
- Use sentence-transformers for better embeddings (if installed)
- Implement caching for frequent queries
- Use async processing for document uploads

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [scikit-learn](https://scikit-learn.org/) - Machine learning library
- [ChromaDB](https://www.trychroma.com/) - Vector database

---

## 📧 Contact

**Author:** Pallavi Dhadage  
**GitHub:** [pallavi-dhadage](https://github.com/pallavi-dhadage)  
**Project Link:** [RAG-Powered-Intelligent-Document-Search](https://github.com/pallavi-dhadage/RAG-Powered-Intelligent-Document-Search)

---

## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

**Made with ❤️ and Python**
