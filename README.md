# RAG Hybrid Retrieval Assistant

Một chatbot thông minh sử dụng kỹ thuật RAG (Retrieval Augmented Generation) với tìm kiếm lai (hybrid search) để trả lời câu hỏi về thông tin đại học.

## Tính năng chính

- Tìm kiếm lai (hybrid search) kết hợp:
  - Full-text search
  - Vector search với embedding
  - Re-ranking kết quả
- Giao diện chat trực quan với Streamlit
- Tích hợp nhiều nguồn tri thức:
  - Knowledge base từ Elasticsearch
  - Tìm kiếm web với DuckDuckGo

## Công nghệ sử dụng

### Core Components
- **Agno Framework**: Framework chính để xây dựng agent
- **Gemini**: Mô hình ngôn ngữ từ Google
- **Elasticsearch**: Vector database và full-text search
- **LangChain**: Framework cho RAG pipeline

### Frontend & UI
- **Streamlit**: Xây dựng giao diện web
- **Rich**: Formatting terminal output

### Embeddings & Search
- **Sentence Transformers**: Tạo vector embeddings
- **Hybrid Search**: Kết hợp full-text và vector search

### Storage & Database
- **SQLite**: Lưu trữ phiên chat
- **Elasticsearch**: Vector database

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/hainqh2506/RAG_hybrid_retrieval.git
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Tạo file .env từ .env.example và cập nhật các API keys

4. Chạy ứng dụng:
```bash
streamlit run src/st_main.py
```

## Cấu trúc Project 