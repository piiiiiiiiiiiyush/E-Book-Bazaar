from flask import Flask, request, redirect, session, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,static_folder='statics')
app.secret_key = "secret123"

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

# Purchase Table
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_name = db.Column(db.String(200))
    book_price = db.Column(db.Float)

with app.app_context():
    db.create_all()

# Book data - UPDATED WITH COMPLETE INFO
BOOKS = {
    "python": {
        "name": "Python Programming", 
        "author": "Ryan Turner", 
        "price": 299,
        "original_price": 599,
        "discount": 50,
        "image": "images/download (1).jpg",
        "description": "A comprehensive guide to Python programming covering basics to advanced concepts. Perfect for beginners and experienced developers alike. Learn data structures, algorithms, web development, and more with practical examples.",
        "pages": 450,
        "language": "English",
        "publisher": "Tech Press",
        "year": 2024,
        "isbn": "978-1234567890",
        "category": "Programming",
        "review_1": "Excellent book for learning Python! Clear explanations and great examples. Helped me land my first programming job.",
        "review_2": "Very helpful for beginners. Covers all important topics with hands-on projects.",
        "review_3": "Best Python book I've read. Highly recommended for anyone starting their coding journey!",
        "author_bio": "Ryan Turner is a software engineer with 15 years of experience in Python development. He has worked with top tech companies and taught programming to thousands of students worldwide."
    },
    "power": {
        "name": "The Power of Now", 
        "author": "Eckhart Tolle", 
        "price": 399,
        "original_price": 699,
        "discount": 43,
        "image": "images/powerbook.jpg",
        "description": "A guide to spiritual enlightenment and living in the present moment. Transform your life by embracing the power of now. This groundbreaking book shows you how to free yourself from anxiety and achieve inner peace.",
        "pages": 236,
        "language": "English",
        "publisher": "Namaste Publishing",
        "year": 2004,
        "isbn": "978-1577314806",
        "category": "Self-Help",
        "review_1": "Life-changing book! Helped me find inner peace and overcome anxiety. Read it multiple times.",
        "review_2": "A must-read for anyone seeking spiritual growth. Eckhart's wisdom is profound yet simple.",
        "review_3": "Profound wisdom in every page. Absolutely transformative for my mental health and wellbeing.",
        "author_bio": "Eckhart Tolle is a spiritual teacher and best-selling author known for his teachings on mindfulness and presence. His books have been translated into 52 languages and sold millions of copies worldwide."
    },
    "monk": {
        "name": "Think Like a Monk", 
        "author": "Jay Shetty", 
        "price": 349,
        "original_price": 599,
        "discount": 42,
        "image": "images/monk.jpg",
        "description": "Train your mind for peace and purpose every day. Learn ancient wisdom from a modern perspective. Jay Shetty combines his experience as a monk with practical advice for the modern world.",
        "pages": 328,
        "language": "English",
        "publisher": "Simon & Schuster",
        "year": 2020,
        "isbn": "978-1982134488",
        "category": "Self-Help",
        "review_1": "Practical wisdom that you can apply immediately to your life. Love the monk mindset principles!",
        "review_2": "Jay Shetty's insights are amazing. Love this book! Changed how I approach daily challenges.",
        "review_3": "Changed my perspective on life. Highly inspirational! A perfect blend of ancient and modern wisdom.",
        "author_bio": "Jay Shetty is a former monk, purpose coach, and host of the #1 health podcast, On Purpose. He spent three years as a monk in India before sharing his learnings with the world through social media and books."
    },
    "avengers": {
        "name": "Avengers Storybook", 
        "author": "Stan Lee", 
        "price": 199,
        "original_price": 399,
        "discount": 50,
        "image": "images/Avengers.jpg",
        "description": "Join Earth's Mightiest Heroes in their epic adventures. Perfect for Marvel fans of all ages! Experience thrilling stories featuring Iron Man, Captain America, Thor, Hulk, and the entire Avengers team.",
        "pages": 128,
        "language": "English",
        "publisher": "Marvel Press",
        "year": 2023,
        "isbn": "978-1302946789",
        "category": "Comics",
        "review_1": "My kids love this book! Great stories and illustrations. They read it every night before bed.",
        "review_2": "Perfect for young Marvel fans. Exciting and engaging! Great introduction to the Avengers universe.",
        "review_3": "Wonderful collection of Avengers stories. Highly entertaining! Even adults will enjoy reading this.",
        "author_bio": "Stan Lee was the legendary creator of Marvel Comics and co-creator of Spider-Man, X-Men, Iron Man, and many more superheroes. His legacy continues to inspire millions of fans worldwide."
    }
}

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# NEW ROUTE - Book Info Page
@app.route('/book/<book_id>')
def book_info(book_id):
    if book_id not in BOOKS:
        return "Book not found!", 404
    
    book_data = BOOKS[book_id]
    
    # Get related books (all except current one)
    related_books = {k: v for k, v in BOOKS.items() if k != book_id}
    
    return render_template('book_info.html', 
                         book_id=book_id, 
                         book=book_data,
                         related_books=related_books)

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password != confirm:
            return render_template('signup.html', error="Passwords do not match!")

        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error="Email already exists!")

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.name
            session['user_id'] = user.id
            
            # If user came from book click, redirect to payment
            if 'redirect_book' in session:
                book = session.pop('redirect_book')
                return redirect(f'/payment/{book}')
            
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid Email or Password!")
    
    # Check if user came from book click
    book = request.args.get('book')
    if book:
        session['redirect_book'] = book
    
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user_name=session['user'])
    return redirect('/login')

# Payment page for specific book
@app.route('/payment/<book>')
def payment(book):
    if 'user' not in session:
        session['redirect_book'] = book
        return redirect('/login')
    
    if book not in BOOKS:
        return "Book not found!", 404
    
    book_data = BOOKS[book]
    return render_template('payment.html', book_id=book, book=book_data)

# Process payment
@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'user' not in session:
        return redirect('/login')
    
    book_id = request.form.get('book_id')
    book_price = float(request.form.get('book_price'))
    payment_method = request.form.get('payment_method')
    
    if book_id in BOOKS:
        # Save purchase to database
        purchase = Purchase(
            user_id=session['user_id'],
            book_name=BOOKS[book_id]['name'],
            book_price=book_price
        )
        db.session.add(purchase)
        db.session.commit()
        
        return render_template('sucess.html', 
                             book_name=BOOKS[book_id]['name'],
                             book_price=book_price)
    
    return "Invalid book selected!"

# Payment Success Page
@app.route('/payment/sucess/<book_id>')
def payment_success(book_id):
    if 'user' not in session:
        return redirect('/login')
    
    if book_id not in BOOKS:
        return redirect('/dashboard')
    
    book_data = BOOKS[book_id]
    return render_template('sucess.html', 
                         book_name=book_data['name'],
                         book_price=book_data['price'])

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    session.pop('redirect_book', None)
    return redirect('/')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Authors
@app.route('/authors')
def authors():
    return render_template('authors.html')

# Categories
@app.route('/category')
def category():
    return render_template('category.html')

if __name__ == "__main__":
    app.run(debug=True)