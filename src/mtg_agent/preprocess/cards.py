import re
from typing import List

from mtg_agent.models.reddit import SimplifiedRedditPost
from mtg_agent.utils.api import get_scryfall_card_data


_card_regex = re.compile(r'\[\[([^]]+)]]')

def extract_card_data(content: str) -> List[str]:
    pass