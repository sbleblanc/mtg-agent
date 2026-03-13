from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

import asyncio
from dataclasses import dataclass
from typing import Any

import logfire
from httpx import AsyncClient
from pydantic import BaseModel


# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')
logfire.instrument_pydantic_ai()

@dataclass
class Deps:
    client: AsyncClient

class LatLng(BaseModel):
    lat: float
    lng: float

llama_cpp_model = OpenAIChatModel(
        '',
        provider=OpenAIProvider(
            api_key='your-api-key',
            base_url="http://127.0.0.1:8080/v1"
        )
    )
weather_agent = Agent(
    llama_cpp_model,
    # 'Be concise, reply with one sentence.' is enough for some models (like openai) to use
    # the below tools appropriately, but others like anthropic and gemini require a bit more direction.
    instructions='Be concise, reply with one sentence.',
    deps_type=Deps,
    retries=2,
)

@weather_agent.tool
async def get_lat_lng(ctx: RunContext[Deps], location_description: str) -> LatLng:
    """Get the latitude and longitude of a location.

    Args:
        ctx: The context.
        location_description: A description of a location.
    """
    print("getting lat lng")
    # NOTE: the response here will be random, and is not related to the location description.
    r = await ctx.deps.client.get(
        'https://demo-endpoints.pydantic.workers.dev/latlng',
        params={'location': location_description},
    )
    r.raise_for_status()
    return LatLng.model_validate_json(r.content)


@weather_agent.tool
async def get_weather(ctx: RunContext[Deps], lat: float, lng: float) -> dict[str, Any]:
    """Get the weather at a location.

    Args:
        ctx: The context.
        lat: Latitude of the location.
        lng: Longitude of the location.
    """
    print("getting weather")
    # NOTE: the responses here will be random, and are not related to the lat and lng.
    temp_response, descr_response = await asyncio.gather(
        ctx.deps.client.get(
            'https://demo-endpoints.pydantic.workers.dev/number',
            params={'min': 10, 'max': 30},
        ),
        ctx.deps.client.get(
            'https://demo-endpoints.pydantic.workers.dev/weather',
            params={'lat': lat, 'lng': lng},
        ),
    )
    temp_response.raise_for_status()
    descr_response.raise_for_status()
    return {
        'temperature': f'{temp_response.text} °C',
        'description': descr_response.text,
    }

async def main():
    async with AsyncClient() as client:
        logfire.instrument_httpx(client, capture_all=True)
        deps = Deps(client=client)
        result = await weather_agent.run(
            'What is a Bogan in australia?', deps=deps
        )
        print('Response:', result.output)


if __name__ == "__main__":
    asyncio.run(main())
