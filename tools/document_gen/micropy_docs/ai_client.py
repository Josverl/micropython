"""Azure OpenAI client setup with token caching."""

import os
import threading
import time
from typing import Callable, Optional

# Lazy imports to avoid requiring azure packages when not using AI features
_client = None
_client_lock = threading.Lock()


def get_default_config() -> dict:
    """Get default Azure OpenAI configuration from environment."""
    return {
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "https://jvai.openai.azure.com/"),
        "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini-2"),
        "api_version": os.getenv("AZURE_OPENAI_VERSION", "2024-12-01-preview"),
    }


class TokenProvider:
    """Thread-safe token provider with caching."""

    def __init__(self):
        self._token_lock = threading.Lock()
        self._cached_token: Optional[str] = None
        self._token_expires_at: float = 0
        self._credential = None

    def _get_credential(self):
        """Lazily initialize the credential."""
        if self._credential is None:
            from azure.identity import DefaultAzureCredential

            self._credential = DefaultAzureCredential(
                exclude_visual_studio_code_credential=True,
                exclude_environment_credential=False,
                additionally_allowed_tenants=["*"],
            )
        return self._credential

    def __call__(self) -> str:
        """Get a valid token, refreshing if needed."""
        # Return cached token if still valid (with 60s buffer)
        if self._cached_token and time.time() < self._token_expires_at - 60:
            return self._cached_token

        with self._token_lock:
            # Double-check after acquiring lock
            if self._cached_token and time.time() < self._token_expires_at - 60:
                return self._cached_token

            try:
                credential = self._get_credential()
                token_response = credential.get_token(
                    "https://cognitiveservices.azure.com/.default"
                )
                self._cached_token = token_response.token
                self._token_expires_at = token_response.expires_on
                return self._cached_token
            except Exception:
                # Reset credential and retry
                from azure.identity import DefaultAzureCredential

                self._credential = DefaultAzureCredential(
                    exclude_visual_studio_code_credential=True,
                    exclude_environment_credential=False,
                    additionally_allowed_tenants=["*"],
                )
                token_response = self._credential.get_token(
                    "https://cognitiveservices.azure.com/.default"
                )
                self._cached_token = token_response.token
                self._token_expires_at = token_response.expires_on
                return self._cached_token


def get_client():
    """Get or create the Azure OpenAI client singleton."""
    global _client

    if _client is not None:
        return _client

    with _client_lock:
        if _client is not None:
            return _client

        from openai import AzureOpenAI

        config = get_default_config()
        token_provider = TokenProvider()

        _client = AzureOpenAI(
            azure_endpoint=config["endpoint"],
            api_version=config["api_version"],
            azure_ad_token_provider=token_provider,
        )
        return _client


def get_deployment() -> str:
    """Get the deployment name."""
    return get_default_config()["deployment"]
