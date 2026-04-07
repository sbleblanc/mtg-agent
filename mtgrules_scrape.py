#Vibe coded as experiment with Gemma 4

#!/usr/bin/env python3
import argparse
import json
import requests
import sys
import time
from typing import List, Dict, Any

# Rate Limiting State
REQUEST_LIMIT = 10
TIME_WINDOW_MINUTES = 1
MIN_INTERVAL_SECONDS = (TIME_WINDOW_MINUTES * 60) / REQUEST_LIMIT
request_timestamps: list[float] = []

def wait_for_rate_limit():
    """Pauses execution to respect the defined API rate limit."""
    global request_timestamps
    current_time = time.time()
    
    # Remove timestamps older than the time window
    request_timestamps = [t for t in request_timestamps if current_time - t <= TIME_WINDOW_MINUTES * 60]
    
    if len(request_timestamps) >= REQUEST_LIMIT:
        time_to_wait = (request_timestamps[0] + TIME_WINDOW_MINUTES * 60) - current_time + 0.1
        print(f"Rate limit hit. Waiting for {time_to_wait:.2f} seconds to respect the {REQUEST_LIMIT} req/min limit.")
        time.sleep(time_to_wait)
        # Recalculate current_time after sleeping to ensure accuracy for the next check
        current_time = time.time()

    request_timestamps.append(current_time)

# Global list to store all scraped data
all_posts_data: List[Dict[str, Any]] = []

def fetch_page(url: str, count: int, after: str = None) -> Dict[str, Any]:
    """Fetches a single page of Reddit posts with rate limit handling."""
    print(f"Fetching page from: {url}")
    max_retries = 5
    base_delay = 5
    for attempt in range(max_retries):
        wait_for_rate_limit()
        try:
            headers = {"User-Agent": "Simple script from /u/JusteLaVerit"}
            response = requests.get(url, params={"count": count, "after": after} if after else {}, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Retry on 429 (Rate Limit) or 5xx (Server Error)
            if response.status_code in [429, 500, 502, 503, 504] and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Transient error ({response.status_code}). Retrying page fetch in {delay} seconds... (Attempt {attempt + 1}/{max_retries})", file=sys.stderr)
                time.sleep(delay)
            else:
                print(f"Error fetching Reddit page after {attempt+1} attempts: {e}", file=sys.stderr)
                return {}
        except requests.exceptions.RequestException as e:
            print(f"General error fetching Reddit page: {e}", file=sys.stderr)
            return {}
    return {}

def fetch_comments(comment_url: str) -> List[str]:
    """Fetches and extracts comment bodies from a specific post link with rate limit handling."""
    max_retries = 5
    base_delay = 5
    for attempt in range(max_retries):
        wait_for_rate_limit()
        try:
            comments_url = f"{comment_url}.json"
            headers = {"User-Agent": "Simple script from /u/JusteLaVerit"}
            response = requests.get(comments_url, headers=headers)
            response.raise_for_status()
            payload = response.json()
            
            # Comments are at index 1 in the payload
            if len(payload) > 1 and isinstance(payload[1], dict) and 'data' in payload[1] and 'children' in payload[1]['data']:
                comments_list = []
                # Iterate through children in the comments payload
                for child in payload[1]['data']['children']:
                    if 'data' in child and 'body' in child['data']:
                        comments_list.append(child['data']['body'])
                return comments_list
            else:
                print(f"Could not find comments structure for URL: {comment_url}", file=sys.stderr)
                return []
        except requests.exceptions.HTTPError as e:
            # Retry on 429 (Rate Limit) or 5xx (Server Error)
            if response.status_code in [429, 500, 502, 503, 504] and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Transient error ({response.status_code}). Retrying comments fetch in {delay} seconds... (Attempt {attempt + 1}/{max_retries})", file=sys.stderr)
                time.sleep(delay)
            else:
                print(f"Error fetching comments for {comment_url} after {attempt+1} attempts: {e}", file=sys.stderr)
                return []
        except requests.exceptions.RequestException as e:
            print(f"General error fetching comments for {comment_url}: {e}", file=sys.stderr)
            return []
    return []


def scrape_subreddit(max_pages: int, start_page: int = 0, start_aid: str = None):
    """Main function to scrape posts and their comments."""
    
    base_url = "https://old.reddit.com/r/mtgrules/.json"
    current_page_count = start_page
    after_id = start_aid
    
    print("Starting subreddit scraping...")

    while current_page_count < max_pages:
        count_per_page = 25
        url = base_url
        
        if after_id:
            # Construct URL with count and after ID
            url = f"{base_url}?count={count_per_page}&after={after_id}"
        
        # Fetch posts for the current page
        page_data = fetch_page(url, count_per_page, after_id)
        
        if not page_data or 'data' not in page_data or 'children' not in page_data['data']:
            print("No more data or structure error detected. Stopping.")
            break

        children = page_data['data']['children']
        
        # Process each post on the page
        for index, child in enumerate(children):
            post = child['data']
            
            # 1. Extract required fields
            title = post.get('title')
            selftext = post.get('selftext')
            url = post.get('url')
            
            # 2. Fetch comments if a URL exists
            comments = []
            if url:
                comments = fetch_comments(url)
                
            # 3. Store data
            all_posts_data.append({
                "title": title,
                "content": selftext,
                "comments": comments,
                "url": url
            })
            
        # Update for next iteration
        after_id = page_data['data'].get('after')
        current_page_count += 1
        
        print(f"Processed page {current_page_count}/{max_pages}. Next after_id: {after_id}")

        if not after_id:
            print("End of subreddit reached before reaching max_pages limit.")
            break

    # Save data to file
    try:
        with open("data/raw/mtgrules_dump.json", "w") as f:
            json.dump(all_posts_data, f, indent=2)
        print("Successfully saved all scraped data to data.json")
    except Exception as e:
        print(f"Failed to save data.json: {e}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrapes posts and comments from r/mtgrules Reddit page by page.")
    parser.add_argument("pages", type=int, help="The number of pages to scrape.")
    args = parser.parse_args()
    
    scrape_subreddit(args.pages, 5)