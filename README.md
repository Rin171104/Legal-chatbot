# HAUI RAG Chatbot

Hệ thống chatbot thông minh giải đáp các câu hỏi về quy chế, quy định của Đại học HAUI.

## Tính năng
- Tìm kiếm thông tin từ tài liệu PDF
- Trả lời câu hỏi tự nhiên
- Giao diện web thân thiện

## Cài đặt
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng
```bash
streamlit run frontend/app.py
```

## Kiến trúc
- **Frontend**: Streamlit UI
- **Backend**: FastAPI
- **RAG Pipeline**: Embedding + Retrieval + Generation
- **Vector DB**: FAISS

