from app.rag.vectorstore import get_vectorstore

def test_search(query):
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=2)

    print(f"\nQuery: {query}")
    print("-" * 50)
    for i, doc in enumerate(results, 1):
        print(f"Result {i}: {doc.page_content}\n")

if __name__ == "__main__":
    test_search("How do I get a refund?")