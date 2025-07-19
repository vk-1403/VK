import os
import logging
import threading
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import base64
from flask_mail import Mail, Message
from scholarly import scholarly  # Google Scholar scraping library

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vidyapatikumar.me@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_APP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'vidyapatikumar.me@gmail.com'

mail = Mail(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Cache publications (update periodically)
publications_cache = []
last_update = None

# Google Scholar author ID (your profile)
SCHOLAR_ID = 'thYJjvAAAAAJ'
SCHOLAR_LINK = f'https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en'

def fetch_publications():
    """Fetch publications from Google Scholar and cache them"""
    global publications_cache, last_update
    try:
        logging.info("Fetching publications from Google Scholar...")
        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(author, sections=['publications'])
        pubs = author.get('publications', [])

        publications_cache = [
            {
                'title': pub['bib']['title'],
                'journal': pub['bib'].get('venue', 'Unknown Journal'),
                'year': pub['bib'].get('pub_year', 'NA'),
                'citations': pub.get('num_citations', 0),
                'link': pub.get('pub_url', '#')
            }
            for pub in pubs
        ]

        publications_cache.sort(key=lambda x: x['citations'], reverse=True)
        last_update = datetime.now()
        logging.info(f"Fetched {len(publications_cache)} publications (Last updated: {last_update})")
    except Exception as e:
        logging.error(f"Error fetching Google Scholar data: {e}")

    # Schedule next fetch in 24 hours
    threading.Timer(86400, fetch_publications).start()

# Start fetching publications in background on app startup
threading.Thread(target=fetch_publications).start()

# Profile photo (base64 encoded)
def get_profile_image_base64():
    """Convert the uploaded profile image to base64 for embedding in HTML"""
    try:
        with open("mypic/VK.png", "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error processing profile image: {e}")
        placeholder_svg = """<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="100" fill="#3498db"/>
            <circle cx="100" cy="80" r="30" fill="white"/>
            <ellipse cx="100" cy="160" rx="50" ry="35" fill="white"/>
        </svg>"""
        return base64.b64encode(placeholder_svg.encode()).decode('utf-8')

# Load your existing CSS, JS, and HTML_TEMPLATE here (truncated for brevity)
from my_html_assets import CSS_STYLES, JAVASCRIPT, HTML_TEMPLATE  # Put them in a separate file

@app.route('/')
def index():
    """Main page route"""
    profile_image = get_profile_image_base64()
    top_publications = publications_cache[:5]  # Show only top 5

    return render_template_string(
        HTML_TEMPLATE,
        title="Vidyapati Kumar - PhD Candidate | AI & Biomechatronics",
        css_styles=CSS_STYLES,
        javascript=JAVASCRIPT,
        profile_image=profile_image,
        publications=top_publications,
        scholar_link=SCHOLAR_LINK
    )

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submissions and send email"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        msg = Message(subject=f"New Contact Form: {subject}", recipients=["vidyapatikumar.me@gmail.com"])
        msg.body = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
        """
        mail.send(msg)

        return jsonify({'success': True, 'message': 'Thank you for your message! I will get back to you soon.'})
    except Exception as e:
        logging.error(f"Error processing contact form: {e}")
        return jsonify({'success': False, 'error': 'Failed to send message'}), 500

@app.errorhandler(404)
def not_found(error):
    return "Page not found", 404

@app.errorhandler(500)
def server_error(error):
    logging.error(f"Server error: {error}")
    return "Internal server error", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
