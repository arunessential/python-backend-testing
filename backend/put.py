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
# PUT USER
# =========================
@app.route('/users/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({'error': 'Name and Email are required'}), 400

        connection = get_connection()

        with connection.cursor() as cursor:
            query = f"""
                UPDATE {TABLE_NAME}
                SET name=%s, email=%s
                WHERE id=%s
            """
            rows = cursor.execute(query, (name, email, user_id))

        connection.commit()
        if rows == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({'message': 'User updated successfully'})

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
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
