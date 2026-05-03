import pytest
from unittest.mock import MagicMock, patch
from services.auth_service import create_token, verify_token
from services.firestore_service import get_session_history
import os

def test_jwt_flow():
    """Test that we can create and verify a token."""
    user_id = "test-user-123"
    token = create_token(user_id)
    assert isinstance(token, str)
    
    decoded_sub = verify_token(token)
    assert decoded_sub == user_id

@patch("google.cloud.firestore.Client")
def test_firestore_get_history(mock_firestore):
    """Test Firestore service logic with a mocked client."""
    # Setup mock
    mock_db = MagicMock()
    mock_firestore.return_value = mock_db
    
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {"history": [{"role": "user", "content": "hi"}]}
    
    mock_db.collection.return_value.document.return_value.get.return_value = mock_doc
    
    # Call service
    history = get_session_history("session-abc")
    
    # Assert
    assert len(history) == 1
    assert history[0]["role"] == "user"

@patch("google.cloud.secretmanager.SecretManagerServiceClient")
def test_get_secret_mock(mock_sm):
    """Test Secret Manager service logic with a mocked client."""
    from services.secret_manager import get_secret
    
    # Setup mock
    mock_client = MagicMock()
    mock_sm.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.payload.data.decode.return_value = "secret-value"
    mock_client.access_secret_version.return_value = mock_response
    
    # Call service
    secret = get_secret("MY_SECRET")
    
    # Assert
    assert secret == "secret-value"

@patch("google.genai.Client")
def test_rag_service_mock(mock_genai):
    """Test RAG service logic with a mocked Vertex AI client."""
    from services.rag_service import search_rag
    from config import RAG_CORPUS_ID
    
    if not RAG_CORPUS_ID:
        # Mock RAG_CORPUS_ID for test
        with patch("services.rag_service.RAG_CORPUS_ID", "test-corpus"):
            mock_client = MagicMock()
            mock_genai.return_value = mock_client
            
            mock_response = MagicMock()
            mock_chunk = MagicMock()
            mock_chunk.retrieved_context.text = "Sample context"
            mock_chunk.retrieved_context.uri = "http://example.com"
            mock_response.candidates[0].grounding_metadata.grounding_chunks = [mock_chunk]
            mock_client.models.generate_content.return_value = mock_response
            
            results = search_rag("how to vote")
            assert len(results) == 1
            assert results[0]["text"] == "Sample context"
    else:
        mock_client = MagicMock()
        mock_genai.return_value = mock_client
        # same logic
        results = search_rag("how to vote")
        assert results is not None
