#!/usr/bin/env python3
"""
Mouser Component Search Skill Script

Calls Mouser Search API and returns formatted results for component availability,
pricing, datasheets, and lead times.
"""

import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "Required library 'requests' not installed. Install with: pip install requests"
    }))
    sys.exit(1)


def load_api_key():
    """
    Load API key from skill_config.json.

    Returns:
        str: API key if found, None otherwise
    """
    # Find project root by searching upward for .elecspecify directory
    current_path = Path.cwd()
    project_root = None

    # Search up to 5 levels up
    for _ in range(5):
        if (current_path / ".elecspecify").exists():
            project_root = current_path
            break
        if current_path.parent == current_path:
            break
        current_path = current_path.parent

    if not project_root:
        return None

    config_path = project_root / ".elecspecify" / "memory" / "skill_config.json"

    if not config_path.exists():
        return None

    try:
        config = json.loads(config_path.read_text(encoding='utf-8'))
        skill_config = config.get("skills", {}).get("component_search", {}).get("mouser-component-search", {})
        api_key = skill_config.get("api_key", "")
        return api_key if api_key else None
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": f"Failed to load configuration: {str(e)}"
        }), file=sys.stderr)
        return None


def search_mouser(keyword, api_key):
    """
    Call Mouser Search API to search for components.

    Args:
        keyword (str): Search keyword (part number, manufacturer, etc.)
        api_key (str): Mouser API key

    Returns:
        dict: Response with success status and results or error message
    """
    url = f"https://api.mouser.com/api/v1/search/keyword?apiKey={api_key}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "SearchByKeywordRequest": {
            "keyword": keyword,
            "records": 0,
            "startingRecord": 0,
            "searchOptions": "",
            "searchWithYourSignUpLanguage": ""
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        # Handle 401 Unauthorized
        if response.status_code == 401:
            return {
                "success": False,
                "error": "Invalid API key, please check your configuration"
            }

        # Handle 429 Too Many Requests
        if response.status_code == 429:
            return {
                "success": False,
                "error": "API rate limit exceeded, please try again later"
            }

        # Handle 200 OK
        if response.status_code == 200:
            # Parse Mouser API response
            data = response.json()
            results = []

            # Extract parts from response
            search_results = data.get("SearchResults", {})
            parts = search_results.get("Parts", [])

            for item in parts:
                # Extract availability (stock) - handle both string and int
                availability_str = item.get("Availability", "0")
                if isinstance(availability_str, str):
                    # Remove commas and convert to int
                    stock = int(availability_str.replace(",", "").split()[0]) if availability_str else 0
                else:
                    stock = int(availability_str)

                # Extract price - get first price break
                price_breaks = item.get("PriceBreaks", [])
                price = price_breaks[0].get("Price", "$0.00") if price_breaks else "$0.00"

                results.append({
                    "part_number": item.get("MouserPartNumber", ""),
                    "manufacturer": item.get("Manufacturer", ""),
                    "stock": stock,
                    "price": price,
                    "datasheet_url": item.get("DataSheetUrl", ""),
                    "lead_time": item.get("LeadTime", "Unknown")
                })

            return {"success": True, "results": results}

        # Handle unexpected status codes
        return {
            "success": False,
            "error": f"Unexpected API response: HTTP {response.status_code}"
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "API request timeout, please try again"
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": "Unable to connect to Mouser API, please check network connection"
        }


def main():
    """Main entry point for the script."""
    # Set UTF-8 encoding for stdout (Windows compatibility)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    # Check arguments
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: mouser_search.py <keyword>"
        }))
        sys.exit(1)

    keyword = sys.argv[1]

    # Load API key
    api_key = load_api_key()
    if not api_key:
        print(json.dumps({
            "success": False,
            "error": "API key not configured. Please use /elecspeckit.skillconfig update mouser-component-search --api-key YOUR_KEY to configure"
        }))
        sys.exit(1)

    # Call Mouser API
    result = search_mouser(keyword, api_key)

    # Output result as JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
