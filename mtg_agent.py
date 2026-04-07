from docutils.nodes import description
from pydantic_ai import Agent, RunContext, WrapperToolset, ToolsetTool, ModelRetry
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai_skills import SkillsToolset, SkillResourceNotFoundError
import urllib.parse

import asyncio
from typing import Any

import logfire
from httpx import AsyncClient
from pydantic import BaseModel, Field, field_validator
from collections import defaultdict


class SkillsToolsetWithRetry(WrapperToolset):

    test_cache = defaultdict(list)

    async def call_tool(
        self, name: str, tool_args: dict[str, Any], ctx: RunContext, tool: ToolsetTool
    ) -> Any:
        try:
            print(f"tool: {name}")
            print(f"run_id: {ctx.run_id}")
            # if name == "read_skill_resource":
            #     if ctx.run_id in self.test_cache and tool_args in self.test_cache[ctx.run_id]:
            #         print("on repete!")
            #     else:
            #         self.test_cache[ctx.run_id].append(tool_args)

            res = await super().call_tool(name, tool_args, ctx, tool)
            # print(self.test_cache)

        except ModelRetry:
            raise
        except SkillResourceNotFoundError as e:
            print("Skill not found, retry raised")
            raise ModelRetry(str(e))
        else:
            return res


class ScryfallQuery(BaseModel):
    query: str = Field(description="The generated scryfall search query")

    @field_validator("query", mode="after")
    @classmethod
    def convert_url(cls, value: str) -> str:
        return urllib.parse.quote_plus(value)

logfire.configure(send_to_logfire='if-token-present')
logfire.instrument_pydantic_ai()

llama_cpp_model = OpenAIChatModel(
    '',
    provider=OpenAIProvider(
        api_key='your-api-key',
        base_url="http://127.0.0.1:8080/v1"
    )
)

# skills_toolset = SkillsToolset(directories=["./skills"])
skills_toolset = SkillsToolsetWithRetry(SkillsToolset(directories=["./skills"]))

agent = Agent(
    model=llama_cpp_model,
    output_type=ScryfallQuery,
    instructions='You are a helpful assistant that helps building Scryfall queries.',
    toolsets=[skills_toolset]
)

@agent.instructions
async def add_skills(ctx: RunContext) -> str | None:
    """Add skills instructions to the agent's context."""
    return await skills_toolset.wrapped.get_instructions(ctx)


agent2 = Agent(
    model=llama_cpp_model,
    output_type=ScryfallQuery
)

@agent2.instructions
async def load_scryfall_instructions(ctx: RunContext) -> str:
    with open("prompts/scryfall.md") as f:
        return f.read()

app = agent2.to_web()


# async def main():
#     res = await agent2.run(
#         "Build a Scryfall query to find instant that can destroy flying creatures."
#     )
#     print(res.output)
#
# if __name__ == "__main__":
#     asyncio.run(main())

# t%3Aland+produces%3Du+produces%3Dg