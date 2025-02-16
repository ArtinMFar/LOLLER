from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/')
def index():
    # Get the 'javascript' query parameter from the URL.
    query = request.args.get('javascript')
    if not query:
        return "Please provide the 'javascript' query parameter in the URL."

    # Extract package names enclosed in parentheses, e.g. (discord.js) becomes 'discord.js'
    packages = re.findall(r'\((.*?)\)', query)
    if not packages:
        return "No valid package names found in the query parameter."

    combined_result = ""
    for package in packages:
        npm_url = f"https://www.npmjs.com/package/{package}"
        try:
            # Fetch the npm package page.
            response = requests.get(npm_url)
            response.raise_for_status()
            
            # Parse the HTML and extract text.
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text(separator="\n", strip=True)
        except Exception as e:
            text_content = f"Error fetching {package}: {e}"
        
        # Append the package header and text content.
        combined_result += f"Start of {package}\n{text_content}\n\n"
    
    return Response(combined_result, mimetype='text/plain')

if __name__ == '__main__':
    # Run the Flask app on port 5000.
    app.run(host='0.0.0.0', port=5000, debug=True)
