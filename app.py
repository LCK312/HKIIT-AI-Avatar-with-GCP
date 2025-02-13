from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import current_user  # Assuming using Flask-Login
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os
from datetime import date

app = Flask(__name__)

# Provide default values when environment variables are not set to avoid program crashes
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY', 'your_default_secret_key')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', 'your_default_salt')

# Error handling when initialising serializer
try:
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
except KeyError as e:
    print(f"Error initializing serializer: Missing config key {e}")
    serializer = None  # Or other more appropriate error handling, such as exiting the programme

def generate_reset_token(email):
    if serializer is None:
        print("Serializer is not initialized, cannot generate token.")
        return None  # Or throw an exception
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def verify_reset_token(token, expiration=3600):  # Token expires in 1 hour
    if serializer is None:
        print("Serializer is not initialized, cannot verify token.")
        return None  # Or throw an exception
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
        return email
    except SignatureExpired:
        print("Token has expired.")  # Add Log
        return None  # Token has expired
    except BadSignature:
        print("Invalid token.")  # Add Log
        return None  # Invalid token

@app.route('/')
def index():
    return render_template('index.html.j2')

@app.route('/login')
def login():
    return render_template('login.html.j2')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html.j2', error='Passwords do not match')

        # Add user registration logic here (e.g., save to database)
        # ...

        # If registration is successful, redirect to login
        return redirect(url_for('login'))

    return render_template('register.html.j2')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        return render_template('reset_password.html.j2', token_valid=False)  # Token invalid or expired

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            return render_template('reset_password.html.j2', token_valid=True, token=token, error='Passwords do not match')

        # Here would update the user's password in database.
        # Use a strong password hashing algorithm like bcrypt.
        # (replace with actual database update):
        print(f"Password reset for {email} with new password (hashed): {new_password}")
        flash('Your password has been reset successfully!', 'success') #Provide feedback

        return redirect(url_for('login'))  # Redirect to login page

    return render_template('reset_password.html.j2', token_valid=True, token=token)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # In real app, validate email exists in the database
        token = generate_reset_token(email)
        # Send email to user
        print(f"Reset password URL: {url_for('reset_password', token=token, _external=True)}")
        flash('Check your email to reset your password', 'info') # Feedback for user

        return redirect(url_for('index')) #Redirect to home or informational page
    return render_template('reset_password_request.html.j2')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html.j2')

@app.route('/reviewa')
def reviewa():
    return render_template('reviewa.html.j2')

@app.route('/payment')
def payment():
    return render_template('payment.html.j2')

# Sample movie data (replace with database or data source)
movies = [
    {'id': 1, 'title': '獅子王：木法沙(英語版)', 'description': '經典動畫重製', 'showtimes': ['10:00', '13:00', '16:00'], 'date': date(2024, 7, 1)},
    {'id': 2, 'title': '「進擊的巨人」完結篇THE LAST ATTACK', 'description': '史詩動畫完結', 'showtimes': ['11:00', '14:00', '17:00'], 'date': date(2024, 7, 1)},
    {'id': 3, 'title': '明日邊界', 'description': '阿湯哥經典科幻片', 'showtimes': ['12:00', '15:00', '18:00'], 'date': date(2024, 7, 2)},
]

@app.route('/daymovie')
def daymovie():
    today = date.today()
    today_movies = [movie for movie in movies if movie['date'] == today] #Filter the movies based on the current date
    return render_template('daymovie.html.j2', movies=today_movies) #Pass the filtered movies to the template

@app.route('/seatingmap')
def seatingmap():
    return render_template('seatingmap.html.j2')

@app.route('/settlement')
def settlement():
    return render_template('settlement.html.j2')

#  NEW: Cinema Location Route
@app.route('/cinema_location')
def cinema_location():
    # Might want to pass data to the template, like a list of cinema locations
    cinema_locations = [
        {'name': 'Cinema A', 'address': '123 Main St'},
        {'name': 'Cinema B', 'address': '456 Oak Ave'},
    ]  # Replace with actual data source

    return render_template('cinema_location.html.j2', locations=cinema_locations)


# Custom error handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html.j2'), 404

# Custom error handler for 500 errors (Internal Server Error)
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html.j2'), 500

if __name__ == '__main__':
    app.run(debug=True)
