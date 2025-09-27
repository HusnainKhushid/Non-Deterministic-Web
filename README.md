# Non-Deterministic Web

A visually stunning, AI-powered Flask app that generates modern, minimalist HTML pages on-the-fly using Google Gemini. Every route produces a unique, self-contained web experience—no two visits are ever the same!

## Features
- **Non-deterministic design:** Each page is generated fresh, with random layouts, color schemes, and content.
- **Gemini-powered creativity:** Uses Google Gemini to create elegant, accessible HTML5 pages.
- **Fast & secure:** No external assets, only inline CSS/JS and SVGs.
- **Explore deeply:** Every page includes smart navigation links to deeper routes, making the site endlessly explorable.

## Getting Started
1. Clone the repo and install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Set your Gemini API key as an environment variable:
   ```sh
   export GEMINI_API_KEY=your-key-here
   ```
3. Run locally:
   ```sh
   python app.py
   ```

## Deploying on Render
- Add your `GEMINI_API_KEY` in the Render dashboard as an environment variable.
- Use the start command: `gunicorn app:app`

## License
MIT

---
Made with AI creativity and Flask magic.
