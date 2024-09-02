from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# PostgreSQL 데이터베이스 URI 설정
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://moneybook_db_user:CBaBtRfohayVn36bNUUyQflS5sqbyxD5@dpg-cravkg56l47c73d1cm8g-a.singapore-postgres.render.com/moneybook_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Transaction 모델 정의
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=True)

# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['POST'])
def add_transaction():
    date = request.form['date']
    amount = request.form['amount']
    category = request.form['category']
    description = request.form['description']

    new_transaction = Transaction(date=date, amount=float(amount), category=category, description=description)
    db.session.add(new_transaction)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
