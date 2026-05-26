# rag/document_loader.py

import os
import sys
import PyPDF2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_pdf(file_path):
    """
    Reads a PDF file and returns all the text inside it.
    """
    print(f"\n📄 Loading PDF: {file_path}")

    text = ""

    # Open the PDF file
    with open(file_path, "rb") as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Loop through every page and extract text
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()
            print(f"   ✅ Read page {page_number + 1} of {len(pdf_reader.pages)}")

    print(f"   📝 Total characters read: {len(text)}")
    return text


def load_text_file(file_path):
    """
    Reads a plain text file and returns the content.
    """
    print(f"\n📄 Loading text file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    print(f"   📝 Total characters read: {len(text)}")
    return text


def load_document(file_path):
    """
    Automatically detects file type and loads it.
    Supports PDF and text files.
    """
    # Get the file extension
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return load_pdf(file_path)
    elif extension in [".txt", ".md"]:
        return load_text_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}. Use PDF or TXT files.")


def split_into_chunks(text, chunk_size=1000, overlap=100):
    """
    Splits a long text into smaller overlapping chunks.

    chunk_size = how many characters per chunk
    overlap = how many characters to repeat between chunks
              (so we don't lose context at the boundaries)
    """
    print(f"\n✂️  Splitting text into chunks...")

    chunks = []
    start = 0

    while start < len(text):
        # Get a chunk of text
        end = start + chunk_size
        chunk = text[start:end]

        # Only add non-empty chunks
        if chunk.strip():
            chunks.append(chunk)

        # Move forward but overlap a little
        start += chunk_size - overlap

    print(f"   📦 Created {len(chunks)} chunks")
    return chunks


# Test it directly
if __name__ == "__main__":
    import sys

    # Create a test text file to try it out
    test_content = """
    Photosynthesis is the process by which plants use sunlight,
    water and carbon dioxide to produce oxygen and energy in the
    form of sugar.

    The process happens in the chloroplasts of plant cells.
    Chlorophyll is the green pigment that captures light energy.

    There are two main stages of photosynthesis:
    1. Light dependent reactions
    2. Light independent reactions (Calvin cycle)

    The overall equation is:
    6CO2 + 6H2O + light energy → C6H12O6 + 6O2
    """

    # Save test content to a file
    with open("uploads/test_notes.txt", "w",encoding="utf-8") as f:
        f.write(test_content)

    # Load and chunk it
    text = load_document("uploads/test_notes.txt")
    chunks = split_into_chunks(text)

    print("\n--- CHUNKS ---")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(chunk)
        print("---")