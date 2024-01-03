from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import mysql.connector
import hashlib
import database
load_dotenv()

app = Flask(__name__)

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

	try:
		conn = database.new_conn()

		query = '''SELECT 
            u.id AS user_id,
            u.username AS username,
            ur.users_role_id AS role_id
        FROM Users u
        INNER JOIN UserRoles ur ON ur.users_id = u.id
        WHERE u.username = %s AND u.password = %s'''
		user = database.pull(conn, query, (user, hashed_password))
		conn.close()

		user = user[0]

		if user:
			session['role_id'] = user['role_id']
			session['id'] = user['user_id']
			session['username'] = user['username']
			return jsonify({'message': 'Login successful'}), 200
		else:
			return jsonify({'error': 'Invalid credentials'}), 401

	except mysql.connector.Error as err:
		return jsonify({'error': str(err)}), 500
	except Exception as err:
		return jsonify({'error': str(err)}), 500

if __name__ == '__main__':
	app.run(host='0.0.0.0')

