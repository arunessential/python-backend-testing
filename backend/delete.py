from flask import Flask, jsonify
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
# DELETE USER
# =========================
@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            # 🔍 Check if user exists
            check_query = f"SELECT * FROM {TABLE_NAME} WHERE id = %s"
            cursor.execute(check_query, (user_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({'error': 'User not found'}), 404

            # 🗑 Delete user
            delete_query = f"DELETE FROM {TABLE_NAME} WHERE id = %s"
            cursor.execute(delete_query, (user_id,))
            connection.commit()

        return jsonify({'message': 'User deleted successfully'})

    except Exception as err:
        return jsonify({'error': str(err)}), 500

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
# ENTRY POINT
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
