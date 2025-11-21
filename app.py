import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# ------------------------------
# App Configuration
# ------------------------------
# Use SECRET_KEY from environment for production; fall back to a dev value for local runs
app.secret_key = os.environ.get('SECRET_KEY', 'kangajunior')

# Flask-Mail configuration
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    # FIXED: Use os.environ.get() instead of app.config.get()
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME', 'kmainanderitu44@gmail.com'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD', 'fhsh prof bthx pldf')
)

mail = Mail(app)

# ------------------------------
# Routes
# ------------------------------

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', title='Home')

@app.route('/services')
def services():
    """Services page"""
    return render_template('services.html', title='Services')

@app.route('/portfolio')
def portfolio():
    """Portfolio/Courses page"""
    return render_template('portfolio.html', title='Courses')

@app.route('/about')
def about():
    """About Us page"""
    return render_template('about.html', title='About Us')

@app.route('/blog')
def blog():
    """Blog listing page"""
    return render_template('blog.html', title='Blog')

@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    return render_template('blog-post.html', title='Blog Post', slug=slug)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form submission"""
    if request.method == 'POST':
        # Collect form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Validate form fields
        if not name or not email or not message:
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('contact'))

        # Create the email message
        msg = Message(
            subject=f'New Contact Message from {name}',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"From: {name} <{email}>\n\n{message}"
        )

        try:
            mail.send(msg)
            flash('✅ Your message has been sent successfully!', 'success')
        except Exception as e:
            print(f"Email failed to send: {e}")
            flash('❌ Something went wrong while sending your message. Please try again later.', 'error')

        return redirect(url_for('contact'))

    return render_template('contact.html', title='Contact')

# ------------------------------
# Error Handling
# ------------------------------

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return render_template('500.html', title='Server Error'), 500

# ------------------------------
# Context Processors
# ------------------------------

@app.context_processor
def inject_year():
    """Make current year available in all templates"""
    from datetime import datetime
    return {'current_year': datetime.now().year}

# ------------------------------
# Run the App
# ------------------------------

if __name__ == '__main__':
    app.run(debug=True)