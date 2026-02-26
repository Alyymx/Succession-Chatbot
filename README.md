# Succession Chatbot

A conversational chatbot website about the HBO show "Succession" with a sleek black theme matching the show's aesthetic.

## Features

- Chat interface styled like Succession
- Answers questions about characters, actors, and plot
- Web search capability for unknown questions
- Friendly conversational responses

## Setup Instructions

### 1. Install Python Dependencies

Open a terminal in the `succession-chat` folder and run:

```bash
pip install -r requirements.txt
```

### 2. Start the Python Backend

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Open the Website

Open `index.html` in your web browser, or serve it with a local server:

```bash
# Option 1: Python
python -m http.server 8000

# Option 2: Node.js
npx serve .
```

Then visit `http://localhost:8000` (or whatever port you used)

## Example Questions

- "Who plays Kendall Roy?"
- "Tell me about Logan Roy"
- "Who is Shiv Roy?"
- "What is Waystar Royco?"
- "Who plays Tom Wambsgans?"

## Files

- `index.html` - Main HTML structure
- `style.css` - Succession-themed styling (black, elegant)
- `script.js` - Frontend chat functionality
- `app.py` - Python Flask backend with chatbot logic
- `requirements.txt` - Python dependencies

## Notes

- The chatbot uses a knowledge base for common questions
- For unknown questions, it attempts web search
- Make sure both the Python server and the frontend are running
