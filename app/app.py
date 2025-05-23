from flask import Flask, request, jsonify
import mysql.connector
import time
import os

app = Flask(__name__)

DB_HOST= os.environ.get("DB_HOST","localhost")
DB_USER= os.environ.get("DB_USER","root")
DB_PASSWORD= os.environ.get("DB_PASSWORD","root")
DB_NAME= os.environ.get("DB_NAME","user_db")
DB_PORT= int(os.environ.get("DB_PORT","3306"))


def get_connection():
    while True:
        try:
            connection = mysql.connector.connect(
                host=DB_HOST,        
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT
            )
            return connection
        except:
            print("Waiting for DB...")
            time.sleep(2)

@app.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data['name']
    age = data['age']
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT
        )
    """)
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User added successfully!"})

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, age FROM users")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
