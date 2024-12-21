from flask import Flask, request, jsonify
from config import Config
import uuid
import os
from calculate_shoulder_length import calculate_shoulder_length
from waist_length import calculate_waist_length
import db
import utils
from decimal import Decimal

app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = 'uploads'

@app.route('/')
def index():
    return 'Welcome to StickPerfect!'

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'front-hand-closed' not in request.files or 'front-hand-raised' not in request.files or 'side' not in request.files or 'front-hand-open' not in request.files:
        return jsonify({"error": "All images are required."}), 400
    
    if 'height' not in request.form:
        return jsonify({"error": "Height is required."}), 400
    
    try:
        height = float(request.form['height'])
    except ValueError:
        return jsonify({"error": "Invalid height value."}), 400

    measurement_id = str(uuid.uuid4())
    measurement_folder = os.path.join(UPLOAD_FOLDER, measurement_id)
    
    image_paths = {}
    variable_to_image_map = {
        'front-hand-closed': request.files['front-hand-closed'],
        'front-hand-raised': request.files['front-hand-raised'],
        'side': request.files['side'],
        'front-hand-open': request.files['front-hand-open']
    }

    for variable_name, image in variable_to_image_map.items():
        filename = f"{variable_name}.jpg" 
        file_path = os.path.join(measurement_folder, filename)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        image.save(file_path)
        image_paths[variable_name] = file_path

        variable_to_image_map[variable_name] = file_path
    
    height_in_inches = utils.get_inches_from_feet(height)
    shoulder_length = calculate_shoulder_length(variable_to_image_map['front-hand-closed'], height_in_inches)
    waist_length = calculate_waist_length(variable_to_image_map['front-hand-open'], height_in_inches)

    for file_path in image_paths.values():
        if os.path.exists(file_path):
            os.remove(file_path)

    if os.path.exists(measurement_folder):
        os.rmdir(measurement_folder)

    data = {
        "id": measurement_id,
        "chest": 0,
        "waist": waist_length,
        "shoulder": shoulder_length,
        "arm_length": 0,
        "height": height
    }
    
    db.add_measurement(data)
    
    return jsonify({"message": "Images uploaded successfully", "id": measurement_id}), 201


@app.route('/measurement/<id>', methods=['GET'])
def get_measurement(id):
    result = db.get_measurement(id)

    if result:
        # Convert all decimal values to float and return the result as a JSON response
        return jsonify({key: float(value) if isinstance(value, Decimal) else value 
                        for key, value in result.items()})
    else:
        return jsonify({"error": "Measurement not found."}), 404



if __name__ == "__main__":
    app.run(debug=True)
