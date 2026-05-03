"""
Secret Manager service — fetches secrets from GCP Secret Manager.
"""

from google.cloud import secretmanager
from config import GCP_PROJECT_ID


def get_secret(secret_id: str, version_id: str = "latest") -> str:
    """
    Fetch a secret value from GCP Secret Manager.
    
    Args:
        secret_id: The ID of the secret to fetch.
        version_id: The version of the secret (default 'latest').
        
    Returns:
        The secret string, or an empty string if not found/error.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{GCP_PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error fetching secret {secret_id}: {e}")
        return ""
