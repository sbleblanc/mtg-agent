from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


def get_local_model() -> OpenAIChatModel:
    return OpenAIChatModel(
        '',
        provider=OpenAIProvider(
            api_key='your-api-key',
            base_url="http://127.0.0.1:8080/v1"
        )
    )

