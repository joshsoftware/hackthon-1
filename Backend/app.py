from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
from config import Config
import uuid
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    conn = psycopg2.connect(app.config['DATABASE_URL'])
    return conn

@app.route('/')
def index():
    return 'Welcome to the Flask Image Processor!'

@app.route('/upload', methods=['POST'])
def upload_image():
    print("in this")
    print(request)
    if 'front-hand-close' not in request.files or 'front-hand-raised' not in request.files or 'side' not in request.files or 'back' not in request.files:
        return jsonify({"error": "All four images are required."}), 400
    
    if 'height' not in request.form:
        return jsonify({"error": "Height is required."}), 400
    
    try:
        height = float(request.form['height'])
    except ValueError:
        return jsonify({"error": "Invalid height value."}), 400

    front_hand_close = request.files['front-hand-close']
    front_hand_raised = request.files['front-hand-raised']
    side = request.files['side']
    back = request.files['back']

    image_files = [front_hand_close, front_hand_raised, side, back]
    
    measurement_id = str(uuid.uuid4())
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO measurement (id, chest, waist, shoulder, armlength, height)
        VALUES (%s, NULL, NULL, NULL, NULL, %s)
    """, (measurement_id, height))
    conn.commit()

    cursor.close()
    conn.close()

    process_images(image_files, measurement_id)

    return jsonify({"message": "Images uploaded successfully", "id": measurement_id}), 201


@app.route('/get_measurement/<measurement_id>', methods=['GET'])
def get_measurement(measurement_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT chest, waist, shoulder, armlength, height
        FROM measurement
        WHERE id = %s
    """, (measurement_id,))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return jsonify({
            "chest": result[0],
            "waist": result[1],
            "shoulder": result[2],
            "armlength": result[3],
            "height": result[4]
        })
    else:
        return jsonify({"error": "Measurement not found."}), 404


def process_images(image_files, measurement_id):
    print("in pre-process image")

if __name__ == "__main__":
    app.run(debug=True)
