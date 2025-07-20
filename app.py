import os
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from my_html_assets import get_profile_image_base64, PUBLICATIONS, EDUCATION, EXPERIENCE, SKILLS, AWARDS, PROFILE_SUMMARY

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "super-secret-key")

# Configure Flask-Mail
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='vidyapatikumar.me@gmail.com',
    MAIL_PASSWORD=os.environ.get('GMAIL_APP_PASSWORD'),
    MAIL_DEFAULT_SENDER='vidyapatikumar.me@gmail.com'
)
mail = Mail(app)

# Logging
logging.basicConfig(level=logging.DEBUG)

# Routes
@app.route('/')
def home():
    return render_template('home.html', profile_image=get_profile_image_base64())

@app.route('/about')
def about():
    return render_template('about.html', summary=PROFILE_SUMMARY)

@app.route('/education')
def education():
    return render_template('education.html', education=EDUCATION)

@app.route('/experience')
def experience():
    return render_template('experience.html', experience=EXPERIENCE)

@app.route('/publications')
def publications():
    return render_template('publications.html', publications=PUBLICATIONS)

@app.route('/skills')
def skills():
    return render_template('skills.html', skills=SKILLS, awards=AWARDS)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            data = request.get_json()
            name, email, subject, message = data.get('name'), data.get('email'), data.get('subject'), data.get('message')

            msg = Message(subject=f"Contact Form: {subject}",
                          recipients=["vidyapatikumar.me@gmail.com"],
                          body=f"Name: {name}\nEmail: {email}\n\n{message}")
            mail.send(msg)
            logging.info(f"Contact form submitted successfully by {name}")
            return jsonify({'success': True, 'message': 'Thank you! I will get back to you soon.'})
        except Exception as e:
            logging.error(f"Error in contact form: {e}")
            return jsonify({'success': False, 'error': 'Failed to send message'}), 500
    return render_template('contact.html')

@app.route('/cv')
def download_cv():
    try:
        return send_from_directory('static', 'CV_VK_git.pdf', as_attachment=True)
    except Exception as e:
        logging.error(f"Error serving CV: {e}")
        return "CV not found", 404

# Error Handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
