import requests
from pyrate_limiter import Duration, limiter_factory
from pyrate_limiter.extras.requests_limiter import RateLimitedRequestsSession

_cards_api_limiter = limiter_factory.create_inmemory_limiter(rate_per_duration=2, duration=Duration.SECOND)
_cards_api_session = RateLimitedRequestsSession(_cards_api_limiter)

def get_scryfall_card_data(card_name: str):
    """
    Calls the Scryfall API to get card data using fuzzy search, including required headers.

    Args:
        card_name (str): The name of the card to search for.

    Returns:
        str or None: The JSON response content as a string, or None if an error occurs.
    """
    base_url = "https://api.scryfall.com/cards/named"

    # 1. Define the required parameters
    params = {
        "fuzzy": card_name,
        "format": "text"
    }

    # 2. Define the required custom headers
    headers = {
        "User-Agent": "MTGAgentPreprocess/0.1",  # As specified by Scryfall
        "Accept": "*/*"     # A safe and recommended Accept header
    }

    print(f"Attempting to query Scryfall for card: '{card_name}' using custom headers...")

    try:
        # 3. Make the GET request, passing both 'params' and 'headers'
        response = _cards_api_session.get(base_url, params=params, headers=headers)

        # 4. Check for a successful response (status code 200)
        response.raise_for_status()

        # 5. Return the response content as text
        return response.text

    except requests.exceptions.HTTPError as errh:
        print(f"Http Error occurred: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

    return None