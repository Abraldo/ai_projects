import os
from typing import List
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from llama_index.core import Document as LlamaDocument
from llama_index.llms.openai import OpenAI

class HybridSearchEngine:
    def __init__(self, index_name: str = "hybrid-search-index", dimension: int = 1536):
        self.pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY", "dummy-key"))
        self.index_name = index_name
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        try:
            if self.index_name not in [idx.name for idx in self.pc.list_indexes()]:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=dimension,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
            self.index = self.pc.Index(self.index_name)
        except Exception:
            self.index = None
            
        self.bm25_retriever = None
        self.raw_docs = []

    def index_documents(self, documents: List[Document]):
        self.raw_docs = documents
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = 2
        
        if self.index:
            texts = [doc.page_content for doc in documents]
            vectors = self.embeddings.embed_documents(texts)
            
            upsert_data = []
            for i, (doc, vec) in enumerate(zip(documents, vectors)):
                upsert_data.append({
                    "id": f"doc_{i}",
                    "values": vec,
                    "metadata": {"text": doc.page_content, **doc.metadata}
                })
            self.index.upsert(vectors=upsert_data)

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        dense_docs = []
        if self.index:
            try:
                query_vector = self.embeddings.embed_query(query)
                dense_results = self.index.query(vector=query_vector, top_k=top_k, include_metadata=True)
                dense_docs = [match.metadata["text"] for match in dense_results.matches]
            except Exception:
                dense_docs = []

        sparse_docs = []
        if self.bm25_retriever:
            sparse_results = self.bm25_retriever.invoke(query)
            sparse_docs = [doc.page_content for doc in sparse_results]

        combined_context = list(dict.fromkeys(dense_docs + sparse_docs))
        return combined_context[:top_k]

class HallucinationGuardrail:
    def __init__(self):
        self.llm = OpenAI(model="gpt-4o-mini", temperature=0.0)

    def verify_and_generate(self, query: str, contexts: List[str]):
        if not contexts:
            return "❌ Guardrail Triggered: No relevant context was found in the database.", "INSUFFICIENT_CONTEXT", "N/A"
            
        joined_context = "\n---\n".join(contexts)
        
        generation_prompt = f"""
        You are a highly precise financial Q&A assistant. Answer the question based ONLY on the context provided.
        If the answer cannot be completely derived from the context, state 'INSUFFICIENT_CONTEXT'.
        
        Context:
        {joined_context}
        
        Question: {query}
        Answer:"""
        
        raw_answer = self.llm.complete(generation_prompt).text.strip()
        
        if "INSUFFICIENT_CONTEXT" in raw_answer:
            return "❌ Guardrail Triggered: The system could not find enough reliable data in the documents to answer this safely.", "INSUFFICIENT_CONTEXT", "N/A"

        evaluation_prompt = f"""
        Critical Audit Task: Analyze the Grounding Context and the Proposed Answer.
        Does the Proposed Answer contain ANY facts, metrics, or assumptions NOT explicitly present in the Grounding Context?
        Respond with exactly 'SAFE' if the answer is 100% faithful, or 'HALLUCINATION' if it contains external information.

        Grounding Context:
        {joined_context}

        Proposed Answer:
        {raw_answer}

        Verdict (SAFE or HALLUCINATION):"""
        
        verdict = self.llm.complete(evaluation_prompt).text.strip().upper()
        
        if "HALLUCINATION" in verdict:
            return "❌ Guardrail Triggered: The generated response failed consistency verification (Potential Hallucination detected).", "HALLUCINATION", raw_answer
        
        return f"Verified Answer:\n{raw_answer}", "SAFE", raw_answer
