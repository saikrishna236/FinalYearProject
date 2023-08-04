from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    aadhar = db.Column(db.String(16), nullable=False)
    account_number = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
            aadhar = request.form['aadhar']
            password = request.form['password']

            # Generate an account number (simple example)
            account_number = str(int(round(1000000000 + random.random() * 900000000)))

            user = User(
                name=name,
                email=email,
                phone=phone,
                dob=dob,
                aadhar=aadhar,
                account_number=account_number,
                password=password
            )
            with app.app_context():
                db.session.add(user)
                db.session.commit()

            return f"Registration Successful. Your account number is: {account_number}"
        except Exception as e:
            return f"Registration failed. Error: {str(e)}"

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            account_number = request.form['account_number']
            password = request.form['password']

            with app.app_context():
                user = User.query.filter_by(account_number=account_number).first()

                if user and user.password == password:
                    # User authenticated, display account options
                    return render_template('account.html', user=user)
                else:
                    return "Invalid account number or password"
        except Exception as e:
            return f"Login failed. Error: {str(e)}"

    return render_template('login.html')

@app.route('/account/<int:user_id>', methods=['POST'])
def account(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        try:
            option = request.form['option']

            if option == 'balance':
                return f"Your account balance is: {user.balance}"
            elif option == 'deposit':
                amount = float(request.form['amount'])
                user.balance += amount
                with app.app_context():
                    db.session.commit()
                return f"Amount {amount} deposited successfully."
            elif option == 'withdraw':
                amount = float(request.form['amount'])

                if user.balance >= amount:
                    user.balance -= amount
                    with app.app_context():
                        db.session.commit()
                    return f'Amount {amount} withdrawn'
        except Exception as e:
            return f"Error: {str(e)}"

    return render_template('account.html', user=user)