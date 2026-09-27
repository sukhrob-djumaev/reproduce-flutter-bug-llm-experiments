"""Configurable LM Studio model setup for the PydanticAI agent."""

from dataclasses import dataclass
import os

from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


DEFAULT_LM_STUDIO_BASE_URL = "http://127.0.0.1:1234/v1"
DEFAULT_LM_STUDIO_MODEL = "qwen2.5-7b-instruct"


@dataclass(frozen=True)
class LocalModelConfig:
    """Settings for LM Studio's OpenAI-compatible local server."""

    base_url: str
    model_name: str
    api_key: str


def get_local_model_config() -> LocalModelConfig:
    """Read the single supported local-model configuration from the environment."""
    return LocalModelConfig(
        base_url=os.getenv("LM_STUDIO_BASE_URL", DEFAULT_LM_STUDIO_BASE_URL),
        model_name=os.getenv("LM_STUDIO_MODEL", DEFAULT_LM_STUDIO_MODEL),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
    )


def create_local_client(config: LocalModelConfig) -> AsyncOpenAI:
    """Create the local client without requiring a cloud API key."""
    return AsyncOpenAI(base_url=config.base_url, api_key=config.api_key)


async def verify_configured_model(config: LocalModelConfig, client: AsyncOpenAI) -> None:
    """Fail clearly when LM Studio or the configured model is unavailable."""
    try:
        available_models = await client.models.list()
    except Exception as error:
        raise RuntimeError(
            f"Cannot reach LM Studio at {config.base_url}. Start its local server first."
        ) from error

    model_ids = {model.id for model in available_models.data}
    if config.model_name not in model_ids:
        raise RuntimeError(
            "Configured LM Studio model is not available: "
            f"{config.model_name!r}. Available models: {sorted(model_ids)}"
        )


def create_local_model(config: LocalModelConfig, client: AsyncOpenAI) -> OpenAIChatModel:
    """Create PydanticAI's OpenAI-compatible model for LM Studio."""
    provider = OpenAIProvider(openai_client=client)
    return OpenAIChatModel(config.model_name, provider=provider)
