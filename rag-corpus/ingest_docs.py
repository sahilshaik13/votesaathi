"""
VoteSaathi RAG Corpus Ingestion Script

Uploads ECI documents (PDFs) to Cloud Storage and indexes them
into a Vertex AI RAG Engine corpus for grounded retrieval.

Usage:
    python ingest_docs.py --bucket BUCKET_NAME --corpus-display-name "VoteSaathi ECI Docs"

Prerequisites:
    - GOOGLE_APPLICATION_CREDENTIALS set to service account key
    - Cloud Storage bucket already created
    - Vertex AI API enabled in GCP project
"""

import os
import sys
import argparse
import vertexai
from vertexai.preview import rag
from google.cloud import storage
from config import GCP_PROJECT_ID, GCP_LOCATION


DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")


def upload_documents_to_gcs(bucket_name: str, source_dir: str) -> list[str]:
    """Upload all PDFs from source_dir to GCS bucket."""
    client = storage.Client(project=GCP_PROJECT_ID)
    bucket = client.bucket(bucket_name)
    uploaded = []

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(".pdf"):
            blob = bucket.blob(f"rag-corpus/{filename}")
            blob.upload_from_filename(os.path.join(source_dir, filename))
            gcs_uri = f"gs://{bucket_name}/rag-corpus/{filename}"
            uploaded.append(gcs_uri)
            print(f"  ✓ Uploaded: {filename} → {gcs_uri}")

    return uploaded


def create_rag_corpus(display_name: str, gcs_uris: list[str]) -> str:
    """Create a Vertex AI RAG corpus and import documents."""
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)

    # Create the corpus
    # Note: Using Spanner mode (default). Serverless mode is an option in some regions.
    corpus = rag.create_corpus(display_name=display_name)
    corpus_name = corpus.name
    print(f"\n✓ Created RAG corpus: {corpus_name}")

    # Import documents from GCS
    # We can import all at once using paths
    rag.import_files(
        corpus_name=corpus_name,
        paths=gcs_uris,
        chunk_size=512,
        chunk_overlap=100,
    )
    print(f"  ✓ Imported {len(gcs_uris)} documents into the corpus.")

    # Extract corpus ID for config
    corpus_id = corpus_name.split("/")[-1]
    print(f"\n🔑 Add this to your backend/.env:")
    print(f"   RAG_CORPUS_ID={corpus_id}")

    return corpus_id


def main():
    parser = argparse.ArgumentParser(description="Ingest ECI documents into Vertex AI RAG Engine")
    parser.add_argument("--bucket", required=True, help="GCS bucket name for document storage")
    parser.add_argument("--corpus-display-name", default="VoteSaathi ECI Documents",
                        help="Display name for the RAG corpus")
    args = parser.parse_args()

    if not os.path.exists(DOCUMENTS_DIR):
        print(f"✗ Documents directory not found: {DOCUMENTS_DIR}")
        print(f"  Place ECI PDF files in {DOCUMENTS_DIR}/ and re-run.")
        sys.exit(1)

    pdfs = [f for f in os.listdir(DOCUMENTS_DIR) if f.lower().endswith(".pdf")]
    if not pdfs:
        print(f"✗ No PDF files found in {DOCUMENTS_DIR}/")
        sys.exit(1)

    print(f"Found {len(pdfs)} PDF(s) to ingest:\n")

    # Step 1: Upload to GCS
    print("📤 Uploading documents to Cloud Storage...")
    gcs_uris = upload_documents_to_gcs(args.bucket, DOCUMENTS_DIR)

    # Step 2: Create RAG corpus and import
    print("\n🧠 Creating Vertex AI RAG corpus...")
    corpus_id = create_rag_corpus(args.corpus_display_name, gcs_uris)

    print("\n✅ Ingestion complete!")


if __name__ == "__main__":
    main()
