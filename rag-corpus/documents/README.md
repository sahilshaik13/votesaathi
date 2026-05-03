# VoteSaathi RAG Corpus Documents

The actual PDF documents used for the Vertex AI RAG Engine are **not stored in this repository** to keep the repository size under 10MB and adhere to GitHub file size limits.

## 📦 Cloud Storage Location
All official ECI rulebooks, manuals, and handbooks are stored in the following secure Google Cloud Storage bucket:

**Bucket Path:** `gs://votesaathi-rag-documents-495109-1777729892/`

## 🛠️ How to Sync
If you need to re-index these files into the Vertex AI RAG Corpus, ensure your GCP service account has `roles/storage.objectViewer` permission on the bucket, and run:

```bash
cd backend
python import_rag.py
```

## 📄 File List (Reference)
- Manual of Model Code of Conduct.pdf
- Form-6_en.pdf (Voter Registration)
- Form-6a_en.pdf (Overseas Voter)
- Handbook for Polling Agents.pdf
- Electoral Roll Procedures.pdf
- ... and other official ECI notifications.
