"""
Prompt templates for RAG
"""

SYSTEM_PROMPT = """
Bạn là một trợ lý AI hữu ích chuyên giải đáp các câu hỏi về quy chế, quy định của HAUI.
Hãy trả lời dựa trên tài liệu được cung cấp.
Nếu không tìm thấy thông tin, hãy nói rõ là bạn không có thông tin về vấn đề này.
"""

def create_rag_prompt(query, context):
    """Create RAG prompt"""
    prompt = f"""
Context:
{context}

Question: {query}

Answer:
"""
    return prompt

def create_qa_prompt(query):
    """Create QA prompt"""
    pass

if __name__ == "__main__":
    pass
