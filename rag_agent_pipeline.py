from typing import List

def ingest_data(sources: List[str]) -> List[str]:
    docs = []
    for src in sources:
        with open(src, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        docs.extend(chunks)
    return docs

def build_index(chunks: List[str]):
    return {i: chunk for i, chunk in enumerate(chunks)}

def retrieve(query: str, index: dict, top_k=2) -> List[str]:
    return [index[i] for i in range(min(top_k, len(index)))]

def agent_query(query: str, index: dict):
    context = retrieve(query, index)
    augmented_prompt = f"Question: {query}\nContext: {context}\nAnswer:"
    response = f"Simulated LLM response to '{query}' using context."
    return response

if __name__ == "__main__":
    sources = ["data.txt"]
    docs = ingest_data(sources)
    index = build_index(docs)

    query = "What is in this dataset?"
    answer = agent_query(query, index)

    print("Query:", query)
    print("Answer:", answer)
