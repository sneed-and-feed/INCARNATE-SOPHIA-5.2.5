import sys
import os
from ddgs import DDGS

def test_search():
    print("--- TESTING DDGS DIRECTLY (ddgs package) ---")
    try:
        with DDGS() as ddgs:
            # Try a very common query
            results = list(ddgs.text("github sneed-and-feed", max_results=3))
            if not results:
                print("Result (text): EMPTY LIST")
            else:
                for r in results:
                    print(f"Title: {r.get('title')}")
            
            # Try news just in case
            news = list(ddgs.news("python", max_results=2))
            if not news:
                print("Result (news): EMPTY LIST")
            else:
                print(f"Found {len(news)} news items.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
