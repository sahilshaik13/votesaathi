import os
import vertexai
from vertexai.preview import rag
from google.auth import default
from config import GCP_PROJECT_ID, GCP_LOCATION, RAG_CORPUS_ID

def upload_local_files():
    # Explicitly request the cloud-platform scope to bypass the invalid_scope error
    credentials, project_id = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    
    print(f"Initializing Vertex AI in {GCP_LOCATION} for {GCP_PROJECT_ID}...")
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION, credentials=credentials)
    
    corpus_name = f"projects/{GCP_PROJECT_ID}/locations/{GCP_LOCATION}/ragCorpora/{RAG_CORPUS_ID}"
    doc_dir = r"d:\votesaathi\rag-corpus\documents"
    
    for filename in os.listdir(doc_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(doc_dir, filename)
            filesize_mb = os.path.getsize(filepath) / (1024 * 1024)
            
            if filesize_mb < 25:
                print(f"Uploading {filename} ({filesize_mb:.2f} MB)...")
                try:
                    rag.upload_file(
                        corpus_name=corpus_name,
                        path=filepath,
                        display_name=filename,
                    )
                    print(f"  -> Success: {filename}")
                except Exception as e:
                    print(f"  -> Failed to upload {filename}: {e}")
            else:
                print(f"Skipping {filename} ({filesize_mb:.2f} MB) - Exceeds 25MB limit")

if __name__ == "__main__":
    upload_local_files()
