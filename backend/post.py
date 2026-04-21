from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

# =========================
# RDS CONFIG
# =========================
RDS_HOST = 'rds-backend-db1.cbe8cwmc8aqr.eu-north-1.rds.amazonaws.com'
RDS_USER = 'admin'
RDS_PASSWORD = 'Yawetag5194'
RDS_DB_NAME = 'dev'
TABLE_NAME = 'users'

# =========================
# DB CONNECTION
# =========================
def get_connection():
    return pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# =========================
# POST USER
# =========================
@app.route('/users/add', methods=['POST'])
def add_user():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Name and Email required"}), 400

        connection = get_connection()

        with connection.cursor() as cursor:
            query = f"INSERT INTO {TABLE_NAME} (name, email) VALUES (%s, %s)"
            cursor.execute(query, (name, email))

        connection.commit()

        return jsonify({"message": "User added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'connection' in locals():
            connection.close()

# =========================
# HEALTH CHECK
# =========================
@app.route('/')
def index():
    return "RDS Master API running"

# =========================
# ENTRY
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
