# rag/embeddings.py

import os
import sys
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load the embedding model
# This model converts text into numbers
# It downloads automatically the first time (~90MB)
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Embedding model loaded!")


def create_embeddings(chunks):
    """
    Takes a list of text chunks and converts
    each one into a list of numbers (embedding).
    """
    print(f"\n🔢 Creating embeddings for {len(chunks)} chunks...")

    # Convert all chunks to embeddings at once
    embeddings = model.encode(chunks, show_progress_bar=True)

    print(f"   ✅ Created {len(embeddings)} embeddings")
    print(f"   📐 Each embedding has {len(embeddings[0])} numbers")

    return embeddings


def build_index(embeddings):
    """
    Stores all embeddings in a FAISS index.
    FAISS lets us search through millions of
    embeddings very fast.
    """
    print(f"\n🗂️  Building search index...")

    # Get the size of each embedding
    dimension = embeddings.shape[1]

    # Create a FAISS index
    # IndexFlatL2 means it finds closest embeddings
    # using L2 distance (straight line distance)
    index = faiss.IndexFlatL2(dimension)

    # Add all embeddings to the index
    index.add(embeddings.astype(np.float32))

    print(f"   ✅ Index built with {index.ntotal} embeddings")

    return index


def save_index(index, chunks, filepath="uploads/index"):
    """
    Saves the FAISS index and chunks to disk
    so we don't have to rebuild every time.
    """
    # Save the FAISS index
    faiss.write_index(index, f"{filepath}.faiss")

    # Save the chunks alongside it
    with open(f"{filepath}.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print(f"\n💾 Index saved to {filepath}")


def load_index(filepath="uploads/index"):
    """
    Loads a previously saved index from disk.
    """
    # Check if index exists
    if not os.path.exists(f"{filepath}.faiss"):
        return None, None

    # Load the FAISS index
    index = faiss.read_index(f"{filepath}.faiss")

    # Load the chunks
    with open(f"{filepath}.pkl", "rb") as f:
        chunks = pickle.load(f)

    print(f"\n📂 Loaded index with {index.ntotal} embeddings")
    return index, chunks


def process_document(file_path):
    """
    Full pipeline — loads a document, chunks it,
    creates embeddings and saves the index.
    """
    from rag.document_loader import load_document, split_into_chunks

    # Step 1 — Load the document
    text = load_document(file_path)

    # Step 2 — Split into chunks
    chunks = split_into_chunks(text)

    # Step 3 — Create embeddings
    embeddings = create_embeddings(chunks)

    # Step 4 — Build search index
    index = build_index(embeddings)

    # Step 5 — Save everything
    save_index(index, chunks)

    return index, chunks


# Test it directly
if __name__ == "__main__":
    index, chunks = process_document("uploads/test_notes.txt")

    print(f"\n✅ Document processed successfully!")
    print(f"   Total chunks indexed: {len(chunks)}")