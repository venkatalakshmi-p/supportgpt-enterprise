from langchain_groq import ChatGroq
from app.rag.vectorstore import get_vectorstore
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

def get_rag_answer(query: str):
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=3)

    context = "\n\n".join([doc.page_content for doc in results])

    prompt = f"""You are a customer support assistant. Answer the customer's question using ONLY the context below. 
If the answer is not in the context, say "I don't have information about that, let me escalate this to a human agent."

Context:
{context}

Customer Question: {query}

Answer:"""

    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    answer = get_rag_answer("How do I get a refund?")
    print(f"\nAnswer: {answer}")