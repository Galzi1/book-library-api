import json
import urllib.request
import urllib.parse
import argparse
import sys

def fetch_book_data(title):
    """Fetches book metadata from Open Library API."""
    encoded_title = urllib.parse.quote(title)
    url = f"https://openlibrary.org/search.json?title={encoded_title}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if data['numFound'] == 0:
                return None
            
            # Extract the first/most relevant result
            doc = data['docs'][0]
            return {
                "title": doc.get("title"),
                "author": doc.get("author_name", ["Unknown"])[0],
                "publish_year": doc.get("first_publish_year"),
                "isbn": doc.get("isbn", ["N/A"])[0]
            }
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True, help="Title of the book to validate")
    args = parser.parse_args()

    print(f"--- Searching Open Library for: {args.title} ---")
    remote_data = fetch_book_data(args.title)

    if not remote_data:
        print(f"Result: No matches found for '{args.title}'.")
        sys.exit(1)

    if "error" in remote_data:
        print(f"Error: {remote_data['error']}")
        sys.exit(1)

    # Output formatted for the Agent to parse easily
    print("\n[EXTERNAL METADATA FOUND]")
    print(json.dumps(remote_data, indent=2))
    print("\nInstruction to Agent: Compare the above with the local FastAPI model and report discrepancies.")

if __name__ == "__main__":
    main()