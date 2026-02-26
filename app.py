from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Succession knowledge base - common questions and answers
KNOWLEDGE_BASE = {
    'kendall roy': {
        'actor': 'Jeremy Strong',
        'character': 'Kendall Roy is the second son of Logan Roy and COO of Waystar Royco.',
        'info': 'Kendall Roy is played by Jeremy Strong. He is Logan Roy\'s second son and serves as COO of Waystar Royco.'
    },
    'jeremy strong': {
        'info': 'Jeremy Strong is an American actor who plays Kendall Roy in Succession. He won an Emmy Award for Outstanding Lead Actor in a Drama Series for his role.'
    },
    'logan roy': {
        'actor': 'Brian Cox',
        'character': 'Logan Roy is the patriarch and CEO of Waystar Royco, a global media and entertainment conglomerate.',
        'info': 'Logan Roy is played by Brian Cox. He is the founder and CEO of Waystar Royco.'
    },
    'brian cox': {
        'info': 'Brian Cox is a Scottish actor who plays Logan Roy in Succession. He is a veteran actor with a long career in film and television.'
    },
    'shiv roy': {
        'actor': 'Sarah Snook',
        'character': 'Shiv Roy (Siobhan Roy) is Logan\'s only daughter and a political strategist.',
        'info': 'Shiv Roy is played by Sarah Snook. She is Logan Roy\'s only daughter and works as a political strategist.'
    },
    'sarah snook': {
        'info': 'Sarah Snook is an Australian actress who plays Shiv Roy (Siobhan Roy) in Succession. She won an Emmy Award for Outstanding Lead Actress in a Drama Series.'
    },
    'roman roy': {
        'actor': 'Kieran Culkin',
        'character': 'Roman Roy is Logan\'s youngest son and head of Waystar Studios.',
        'info': 'Roman Roy is played by Kieran Culkin. He is Logan Roy\'s youngest son and head of Waystar Studios.'
    },
    'kieran culkin': {
        'info': 'Kieran Culkin is an American actor who plays Roman Roy in Succession. He won an Emmy Award for Outstanding Lead Actor in a Drama Series.'
    },
    'connor roy': {
        'actor': 'Alan Ruck',
        'character': 'Connor Roy is Logan\'s eldest son, who is largely excluded from the family business.',
        'info': 'Connor Roy is played by Alan Ruck. He is Logan Roy\'s eldest son and is largely excluded from the family business.'
    },
    'tom wambsgans': {
        'actor': 'Matthew Macfadyen',
        'character': 'Tom Wambsgans is Shiv\'s husband and head of ATN (America\'s Television Network).',
        'info': 'Tom Wambsgans is played by Matthew Macfadyen. He is Shiv Roy\'s husband and head of ATN.'
    },
    'matthew macfadyen': {
        'info': 'Matthew Macfadyen is a British actor who plays Tom Wambsgans in Succession. He won an Emmy Award for Outstanding Supporting Actor in a Drama Series.'
    },
    'greg hirsch': {
        'actor': 'Nicholas Braun',
        'character': 'Greg Hirsch (also called "Cousin Greg") is Logan\'s grandnephew who works at Waystar.',
        'info': 'Greg Hirsch is played by Nicholas Braun. He is Logan Roy\'s grandnephew, often called "Cousin Greg".'
    },
    'nicholas braun': {
        'info': 'Nicholas Braun is an American actor who plays Greg Hirsch (Cousin Greg) in Succession.'
    },
    'waystar royco': {
        'info': 'Waystar Royco is a global media and entertainment conglomerate owned by the Roy family in Succession. It includes news networks, theme parks, and other media properties.'
    },
    'atn': {
        'info': 'ATN (America\'s Television Network) is a conservative news network owned by Waystar Royco in Succession. Tom Wambsgans is the head of ATN.'
    }
}

def search_web(query):
    """Search the web for Succession-related information"""
    try:
        # Try Wikipedia API first (reliable and free)
        wiki_query = f"{query} succession hbo"
        wiki_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(wiki_query.replace(" ", "_"))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            wiki_response = requests.get(wiki_url, headers=headers, timeout=5)
            if wiki_response.status_code == 200:
                wiki_data = wiki_response.json()
                if 'extract' in wiki_data:
                    extract = wiki_data['extract']
                    # Limit to first 300 characters for concise response
                    if len(extract) > 300:
                        extract = extract[:300] + "..."
                    return f"According to Wikipedia: {extract}"
        except:
            pass
        
        # Fallback: Use DuckDuckGo Instant Answer API
        ddg_url = f"https://api.duckduckgo.com/?q={requests.utils.quote(query + ' succession hbo')}&format=json&no_html=1&skip_disambig=1"
        ddg_response = requests.get(ddg_url, headers=headers, timeout=5)
        
        if ddg_response.status_code == 200:
            ddg_data = ddg_response.json()
            if ddg_data.get('AbstractText'):
                return f"According to web sources: {ddg_data['AbstractText']}"
            elif ddg_data.get('Answer'):
                return f"Answer: {ddg_data['Answer']}"
        
        # Last resort: Try scraping DuckDuckGo HTML results
        search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query + ' succession hbo')}"
        response = requests.get(search_url, headers=headers, timeout=8)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for result snippets
            result_snippets = soup.find_all('a', class_='result__snippet')
            if result_snippets:
                snippet_text = result_snippets[0].get_text(strip=True)
                if len(snippet_text) > 300:
                    snippet_text = snippet_text[:300] + "..."
                return f"I found this information online: {snippet_text}"
            
            # Alternative: look for result descriptions
            result_links = soup.find_all('a', class_='result__a')
            if result_links:
                # Try to get context from the result
                result_text = result_links[0].get_text(strip=True)
                return f"I found information about '{result_text}' related to Succession. This appears to be a relevant topic, though I'd recommend checking the source for complete details."
                
    except Exception as e:
        print(f"Web search error: {e}")
    
    return None
def generate_response(user_message):
    """Generate a friendly response to user's question"""
    user_message_lower = user_message.lower()
    
    # Check knowledge base first
    kb_answer = get_knowledge_base_answer(user_message)
    if kb_answer:
        return kb_answer
    
    # Try web search for unknown questions
    web_result = search_web(user_message)
    if web_result:
        return web_result
    
    # If web search didn't work, try a more specific search
    # Add "Succession HBO" to make search more specific
    enhanced_query = f"{user_message} Succession HBO"
    web_result_enhanced = search_web(enhanced_query)
    if web_result_enhanced:
        return web_result_enhanced
    
    # Default friendly response
    return "I'm not entirely sure about that specific detail. I've searched online but couldn't find reliable information. Could you rephrase your question or ask about something else? I can help you with information about characters, actors, plot points, or the show in general. For example, you could ask 'Who plays Kendall Roy?' or 'Tell me about Logan Roy.'"
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'I apologize, but I encountered an error. Please try again.'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    import os

    print("Starting Succession Chatbot server...")
    print("Make sure to install required packages: pip install flask flask-cors requests beautifulsoup4")

    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' is important so Render can reach it
    app.run(host="0.0.0.0", port=port)

