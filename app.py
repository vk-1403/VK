import os
import logging
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import base64
from flask_mail import Mail, Message
from scholarly import scholarly

# Import CSS, JS, and HTML from external file
from my_html_assets import CSS_STYLES, JAVASCRIPT, HTML_TEMPLATE

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vidyapatikumar.me@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_APP_PASSWORD')  # Env variable for security
app.config['MAIL_DEFAULT_SENDER'] = 'vidyapatikumar.me@gmail.com'

mail = Mail(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Google Scholar config
GOOGLE_SCHOLAR_ID = "thYJjvAAAAAJ"
PUBLICATIONS_CACHE = []
LAST_UPDATED = None

def fetch_publications():
    """Fetch publications from Google Scholar"""
    global PUBLICATIONS_CACHE, LAST_UPDATED
    try:
        logging.info("Fetching publications from Google Scholar...")
        author = scholarly.search_author_id(GOOGLE_SCHOLAR_ID)
        author = scholarly.fill(author, sections=["publications"])
        publications = author.get("publications", [])
        PUBLICATIONS_CACHE = sorted(publications, key=lambda x: x['num_citations'], reverse=True)
        LAST_UPDATED = datetime.now()
        logging.info(f"Fetched {len(PUBLICATIONS_CACHE)} publications (Last updated: {LAST_UPDATED})")
    except Exception as e:
        logging.error(f"Error fetching publications: {e}")

# Initial fetch on startup
fetch_publications()

def get_profile_image_base64():
    """Convert the uploaded profile image to base64 for embedding in HTML"""
    try:
        with open("mypic/VK.png", "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error processing profile image: {e}")
        return ""  # Return empty if not found

@app.route('/')
def index():
    """Main page route"""
    profile_image = get_profile_image_base64()
    top_publications = PUBLICATIONS_CACHE[:5]  # Show top 5
    return render_template_string(
        HTML_TEMPLATE,
        title="Vidyapati Kumar - PhD Candidate | AI & Biomechatronics",
        css_styles=CSS_STYLES,
        javascript=JAVASCRIPT,
        profile_image=profile_image,
        publications=top_publications,
        last_updated=LAST_UPDATED
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

        # Send email
        msg = Message(subject=f"New Contact Form: {subject}",
                      recipients=["vidyapatikumar.me@gmail.com"])
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
