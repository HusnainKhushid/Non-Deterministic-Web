import os
from flask import Flask, request, Response
import google.generativeai as genai
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Hardcoded Gemini API key ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=GEMINI_API_KEY)

def get_html_for_route(route_path: str) -> str:
    logger.info(f"Generating HTML for route: {route_path}")
    base_url = request.host_url.rstrip("/")
    full_url = base_url + (route_path if route_path.startswith("/") else f"/{route_path}")
    prompt = f"""
You are a web designer. For the following URL: {full_url}, generate a SINGLE, fully self-contained, valid HTML5 document.

STRICT REQUIREMENTS:
1. OUTPUT:
   - Output ONLY the final HTML code, nothing else (no markdown, no explanations).
   - Document MUST start with <!doctype html>, contain <html lang="en">, a <head> (with <meta charset>, viewport, <title>), and a <body>.

2. STYLING:
   - All CSS must be inline in a single <style> tag in the <head>.
   - Use system fonts (no external fonts).
   - Minimal but modern design: centered layout, fluid spacing, gradients, soft shadows, rounded corners.
   - Ensure good contrast, visible focus outlines, and responsive layout (mobile-first but looks good on desktop).

3. INTERACTIVITY:
   - If JavaScript is needed, it must be inline in a single <script> tag at the end of <body>.
   - Keep JS short and efficient (e.g., random suffix for links).

4. NAVIGATION:
   - Include a header or nav bar plus an “Explore” section.
   - Provide at least 6 navigation links.
   - ALL links must be absolute and same-origin, starting with {base_url}.
   - Each link must go deeper under the current route, e.g.:
     {base_url}{route_path.rstrip('/')}/about
     {base_url}{route_path.rstrip('/')}/gallery
     {base_url}{route_path.rstrip('/')}/services
     {base_url}{route_path.rstrip('/')}/contact
     {base_url}{route_path.rstrip('/')}/blog/2025/launch
     {base_url}{route_path.rstrip('/')}/play/demo
   - At least 3 links must get a short random suffix via JS (e.g., "-x7").

5. CONTENT:
   - Simple structure only (to keep generation fast):
     • Hero section: big headline, subheadline, 2 CTA buttons.
     • Explore section: grid of link-buttons (styled <a role="button">).
     • Footer: repeat sitemap-style links.
   - No heavy feature grids, no long text — keep content concise.

6. SECURITY / ROBUSTNESS:
   - No external assets (no <link>, @import, external <script>, external images).
   - If images are needed, use inline SVG placeholders only.
   - No template placeholders like {{mustache}}.
"""
    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(prompt)
    html = getattr(response, "text", None)

    html = html.replace("```" , "")
    html = html.replace("html\n" , "")
    if not html:
        try:
            html = "".join(
                part.text
                for cand in response.candidates
                for part in cand.content.parts
                if hasattr(part, "text")
            )
        except Exception:
            html = "<!doctype html><html><body><h1>Error</h1><p>No content returned.</p></body></html>"
    # Basic validation: ensure HTML starts with <!doctype html> and contains <html> and <body>
    if not (html.strip().lower().startswith("<!doctype html>") and "<html" in html.lower() and "<body" in html.lower()):
        logger.error("Invalid HTML structure detected. Returning error page.")
        html = "<!doctype html><html><body><h1>Error</h1><p>Invalid HTML structure returned by Gemini.</p></body></html>"
    return html

# --- Catch-all route for any path, including '/' ---
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    logger.info(f"Accessed route: /{path}")
    route_path = "/" + path if path else "/"
    try:
        html = get_html_for_route(route_path)
        logger.info(f"Successfully generated HTML for {route_path}")
        return Response(html, mimetype="text/html")
    except Exception as e:
        logger.error(f"Error generating HTML for {route_path}: {e}")
        return Response(f"<h1>Error</h1><pre>{str(e)}</pre>", mimetype="text/html", status=500)

if __name__ == "__main__":
    logger.info("Starting Flask app on port 5001...")
    app.run(host="0.0.0.0", port=5001, debug=True)
