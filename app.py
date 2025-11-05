from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)

# ------------------------------
# App Configuration
# ------------------------------
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Flask-Mail configuration
app.config.update(
    MAIL_SERVER='smtp.gmail.com',          # e.g. smtp.gmail.com
    MAIL_PORT=587,                         # or 465 for SSL
    MAIL_USE_TLS=True,                     # Use TLS (recommended)
    MAIL_USE_SSL=False,
    MAIL_USERNAME='your_email@gmail.com',  # Replace with your Gmail
    MAIL_PASSWORD='your_app_password',     # Use a Gmail app password
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
    # You can add logic here to fetch specific blog post data from database
    # For now, we'll just pass the slug to the template
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
            recipients=[app.config['MAIL_USERNAME']],  # You receive the message
            body=f"From: {name} <{email}>\n\n{message}"
        )

        try:
            mail.send(msg)
            flash('✅ Your message has been sent successfully!', 'success')
        except Exception as e:
            print(f"Email failed to send: {e}")
            flash('❌ Something went wrong while sending your message.', 'error')

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
# Context Processors (Optional - for global template variables)
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