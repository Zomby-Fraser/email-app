from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import mysql.connector
import hashlib
import database
import os
import pwd
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET')

@app.route('/accounts')
def accounts():
    user_emails = {}
    users = pwd.getpwall()  # Get all accounts
    for user in users:
        mail_dir = f'/home/{user.pw_name}/Maildir/new/'
        try:
            # List all files in the user's mail directory
            emails = os.listdir(mail_dir)
            user_emails[user.pw_name] = emails
        except FileNotFoundError:
            # If the mail directory does not exist, skip the user
            continue

    return render_template('accounts.html', user_emails=user_emails)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	user = request.form.get('user')
	password = request.form.get('password')

	if not user or not password:
		return jsonify({'error': 'Missing username or password'}), 400

	hashed_password = hashlib.sha256(password.encode()).hexdigest()
	print(hashed_password)

	try:
		conn = database.new_conn()

		query = '''SELECT 
            u.user_name AS user_name
        FROM Users u
        WHERE u.user_name = %s AND u.user_password = %s'''
		user = database.pull(conn, query, (user, hashed_password))
		conn.close()

		if len(user) == 0:
			return jsonify({'error': 'Invalid credentials', 'password': hashed_password}), 401

		user = user[0]

		if user:
			session['user_name'] = user['user_name']
			return jsonify({'message': 'Login successful'}), 200
		else:
			return jsonify({'error': 'Invalid credentials'}), 401

	except mysql.connector.Error as err:
		return jsonify({'error': str(err)}), 500
	except Exception as err:
		return jsonify({'error': str(err)}), 500

if __name__ == '__main__':
	app.run(host='0.0.0.0')

