from flask import Flask, render_template_string
import urllib.request
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber & AI Intel Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-100 font-sans min-h-screen">
    <header class="border-b border-gray-800 bg-gray-950 p-6 shadow-md">
        <div class="max-w-5xl mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold tracking-wider text-cyan-400">⚡ CYBER & AI INTEL</h1>
            <span class="bg-cyan-950 text-cyan-400 text-xs px-3 py-1 rounded-full font-mono border border-cyan-800">Live Global Server</span>
        </div>
    </header>
    <main class="max-w-5xl mx-auto p-6">
        <h2 class="text-xl font-semibold mb-6 text-gray-400">Latest Security Intel Feed</h2>
        <div class="space-y-4">
            {% for item in news %}
            <div class="bg-gray-950 border border-gray-800 rounded-lg p-5 hover:border-cyan-500 transition-colors duration-200">
                <a href="{{ item.link }}" target="_blank" class="text-lg font-medium text-white hover:text-cyan-400 transition-colors">
                    {{ item.title }}
                </a>
                <p class="text-gray-400 text-sm mt-2">{{ item.description }}</p>
                <div class="mt-4">
                    <a href="{{ item.link }}" target="_blank" class="text-xs text-cyan-400 underline font-mono">Read Full Intel Report →</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </main>
</body>
</html>
"""

def fetch_cyber_news():
    url = "https://thehackernews.com/rss.xml"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            root = ET.fromstring(data)
            articles = []
            for item in root.findall('.//item')[:10]:
                title = item.find('title').text if item.find('title') is not None else "No Title"
                link = item.find('link').text if item.find('link') is not None else "#"
                desc = item.find('description').text if item.find('description') is not None else "No description."
                articles.append({'title': title, 'link': link, 'description': desc[:220] + "..."})
            return articles
    except Exception as e:
        return [{'title': 'Security Feed Mirror Active', 'link': '#', 'description': f'System Status: Standby connection established. Feed details: {str(e)}'}]

@app.route('/')
def home():
    news_items = fetch_cyber_news()
    return render_template_string(HTML_TEMPLATE, news=news_items)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
