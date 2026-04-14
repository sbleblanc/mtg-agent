from mtg_agent.agents.common import get_local_model

from pydantic import BaseModel, RootModel, Field
from pydantic_ai import Agent


class SyntheticRuleQuestion(BaseModel):
    rule_number: str = Field(description="The number of the rule that would answer the question.")
    question: str = Field(description="The generated question that could be answered by the referenced rule.")


def get_synthetic_question_generator_agent(num_questions: int = 5, retries: int = 5) -> Agent:

    agent = Agent(
        model=get_local_model(),
        output_type=list[SyntheticRuleQuestion],
        retries=5,
        system_prompt=[
            "You are an helpful assistant helping generate synthetic question from the rules the the card game Magic The Gathering.",
            f"You will be given a rule and you will need to generate {num_questions} questions that would be answered by this rule.",
            "It's important to associate the rule number that would answer the question.",
            "The rule number is a string because it can contain letters also.",
            "Do not mention the rule number in the question.",
            "Try to generate questions like a user that would be asking on an online forum.",
            "Don't be redundant.",
        ]
    )
    return agent