from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

def fetch_and_parse_ogp(url, alt_title=None, alt_card=None):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        parsed_url = urllib.parse.urlparse(url)
        og_tags = {}
        for tag in soup.find_all('meta', attrs={"property": True, "content": True}):
            if tag['property'].startswith("og:"):
                og_tags[tag['property']] = tag['content']

        favicon = soup.find("link", rel="icon")
        if favicon:
            if favicon['href'].startswith("http"):
                og_tags['favicon'] = favicon['href']
            else:
                if favicon['href'].startswith("/"):
                    og_tags['favicon'] = f"{parsed_url.scheme}://{parsed_url.netloc}{favicon['href']}"
                else:
                    og_tags['favicon'] = f"{parsed_url.scheme}://{parsed_url.netloc}/{favicon['href']}"
        else:
            og_tags['favicon'] = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"

        og_tags['hostname'] = url.split('/')[2]
        # replace : to _ in keys
        og_tags = {key.replace(":", "_"): value for key, value in og_tags.items()}
        
        print(og_tags)
        return og_tags
    except Exception as e:
        print(e)
        parsed_url = url.split('/')[2]
        favicon_fallback = f"https://www.google.com/s2/favicons?domain={parsed_url}"
        return {
            "og:title": alt_title or parsed_url,
            "og:image": alt_card or favicon_fallback,
            "og:description": "",
            "favicon": favicon_fallback,
        }

@app.route('/ogp', methods=['GET'])
def get_ogp():
    url = request.args.get("url")
    alt_title = request.args.get("altTitle")
    alt_card = request.args.get("altCard")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    ogp_data = fetch_and_parse_ogp(url, alt_title, alt_card)
    return jsonify(ogp_data)

if __name__ == '__main__':
    app.run(port=3000)