import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class TextSearch:
    def __init__(self, model_name="all-MiniLM-L6-v2", index_file="vector_index.faiss"):
        # 使用 sentence-transformers 加载模型
        self.model = SentenceTransformer(model_name)
        
        self.index = None
        self.index_file = index_file
        self.texts = []  # 存储文本

        self.load_index()

    def encode_texts(self, texts):
        """批量编码文本为向量"""
        vectors = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return vectors

    def add_texts(self, texts):
        """添加文本并加入索引"""
        vectors = self.encode_texts(texts)
        self.texts.extend(texts)
        self.add_vectors_to_index(vectors)

    def add_vectors_to_index(self, vectors):
        """把向量添加进索引"""
        if self.index is None:
            dim = vectors.shape[1]
            self.index = faiss.IndexFlatIP(dim)  # 用内积做相似度（向量先归一化）
        self.index.add(vectors)

    def search(self, query_text, top_k=5, threshold=0.7):
        """搜索最相似的文本，返回相似度超过阈值的结果"""
        query_vec = self.encode_texts([query_text])
        D, I = self.index.search(query_vec, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if score >= threshold:
                results.append((self.texts[idx], float(score)))
        return results

    def save_index(self):
        if self.index is not None:
            faiss.write_index(self.index, self.index_file)
            # 文本列表也需要持久化，否则下次无法恢复原文
            import json
            with open(self.index_file + ".txt", "w", encoding="utf-8") as f:
                json.dump(self.texts, f)

    def load_index(self):
        import os
        import json
        if os.path.exists(self.index_file) and os.path.exists(self.index_file + ".txt"):
            self.index = faiss.read_index(self.index_file)
            with open(self.index_file + ".txt", "r", encoding="utf-8") as f:
                self.texts = json.load(f)
            print(f"Loaded index and texts from {self.index_file}")
        else:
            print("No existing index found, will create a new one.")

# 示例
if __name__ == "__main__":
    ts = TextSearch()

    ts.add_texts([
        "Hello, how are you?",
        "What is your name?",
        "How old are you?",
        "I am learning machine learning.",
        "BERT is a transformer model."
    ])

    ts.save_index()

    query = "Tell me about BERT"
    results = ts.search(query, top_k=3, threshold=0.5)
    print("Search results:")
    for text, score in results:
        print(f"Text: {text} - Similarity: {score:.4f}")

