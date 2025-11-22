import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss
import fitz  # PyMuPDF

MODEL_NAME = "all-MiniLM-L6-v2"

class Retriever:
    def __init__(self, index_path="docs_index/faiss.index"):
        self.index_path = index_path
        self.model = SentenceTransformer(MODEL_NAME)
        self.documents = []

    def index_documents(self, doc_folder="data"):
        os.makedirs("docs_index", exist_ok=True)
        texts = []
        for filename in os.listdir(doc_folder):
            if filename.endswith(".pdf"):
                path = os.path.join(doc_folder, filename)
                doc = fitz.open(path)
                for page in doc:
                    texts.append(page.get_text())
            elif filename.endswith(".docx"):
                from docx import Document
                doc = Document(os.path.join(doc_folder, filename))
                for para in doc.paragraphs:
                    texts.append(para.text)
        self.documents = texts
        embeddings = self.model.encode(texts)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        faiss.write_index(index, self.index_path)
        with open("docs_index/meta.pkl", "wb") as f:
            pickle.dump(texts, f)
        print("Documentos indexados.")

    def retrieve(self, query, top_k=3):
        index = faiss.read_index(self.index_path)
        with open("docs_index/meta.pkl", "rb") as f:
            texts = pickle.load(f)
        query_emb = self.model.encode([query])
        D, I = index.search(query_emb, top_k)
        results = [texts[i] for i in I[0]]
        return results
