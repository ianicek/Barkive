from flask import Flask, jsonify, request 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import yaml 

with open('config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + config_data['database']['username'] + ':' + config_data['database']['password'] + '@' + config_data['database']['host'] + ':' + str(config_data['database']['port']) + '/' + config_data['database']['dbname'] 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserModel(db.Model):
    __tablename__ = 'users'  
    idUser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    userRole = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Integer, default=1) 

class DogBreedModel(db.Model):
    __tablename__ = 'dog_breeds'  
    breed = db.Column(db.Text, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    temperament = db.Column(db.Text, nullable=False)
    popularity = db.Column(db.Integer, default=None)
    min_height = db.Column(db.Numeric(6, 3), default=None)
    max_height = db.Column(db.Numeric(6, 3), default=None)
    min_weight = db.Column(db.Numeric(6, 3), default=None)
    max_weight = db.Column(db.Numeric(6, 3), default=None)
    min_expectancy = db.Column(db.Integer, default=None)
    max_expectancy = db.Column(db.Integer, default=None)
    group = db.Column(db.String(80), nullable=False)
    grooming_frequency_value = db.Column(db.Numeric(3, 1), default=None)
    grooming_frequency_category = db.Column(db.String(80), nullable=False)
    shedding_value = db.Column(db.Numeric(3, 1), default=None)
    shedding_category = db.Column(db.String(100), default=None)
    energy_level_value = db.Column(db.Numeric(3, 1), default=None)
    energy_level_category = db.Column(db.String(100), default=None)
    trainability_value = db.Column(db.Numeric(3, 1), default=None)
    trainability_category = db.Column(db.String(150), default=None)
    demeanor_value = db.Column(db.Numeric(3, 1), default=None)
    demeanor_category = db.Column(db.String(150), default=None)

class DogInsuranceModel(db.Model):
    __tablename__ = 'dog_insurance'
    insurance_id = db.Column(db.BigInteger, primary_key=True)
    provider = db.Column(db.String(255), default=None)
    coverage_min = db.Column(db.Integer, default=None)
    coverage_max = db.Column(db.Integer, default=None)
    accident_waiting_period = db.Column(db.Integer, default=None)
    illness_waiting_period = db.Column(db.Integer, default=None)
    wellness_addon = db.Column(db.Boolean, default=None)
    coverage_area = db.Column(db.String(255), default=None)
    website = db.Column(db.Text, default=None)
    covered_illnesses = db.Column(db.Text, default=None)

class MedicationModel(db.Model): 
    __tablename__ = 'Medication'
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(100), nullable=False)
    generic_name = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)
    information = db.Column(db.Text, nullable=True)
    side_effects = db.Column(db.Text, nullable=True)

# Route to ge all users 
@app.route('/get-users', methods=['GET'])
@cross_origin()
def get_data():
    results = UserModel.query.all()  # Fetch all rows from the table
    data = [{"idUser": row.idUser, "username": row.username, 
             "email": row.email, "password": row.password, 
             "userRole": row.userRole, "status": row.status} for row in results]
    return jsonify(data)

# Route to get a specific user by username
@app.route('/get-user/<string:username>', methods=['GET'])
@cross_origin()
def get_user(username):
    user = UserModel.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"idUser": user.idUser, "username": user.username, 
             "email": user.email, "password": user.password, 
             "userRole": user.userRole, "status": user.status}), 200

# Route to get a specific user by idUser
@app.route('/get-user-id/<int:idUser>', methods=['GET'])
@cross_origin()
def get_user_by_id(idUser):
    user = UserModel.query.filter_by(idUser=idUser).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"idUser": user.idUser, "username": user.username, 
             "email": user.email, "password": user.password, 
             "userRole": user.userRole, "status": user.status}), 200

# Route to get a specific user by email
@app.route('/get-user-email/<string:email>', methods=['GET'])
@cross_origin()
def get_user_by_email(email):
    user = UserModel.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"idUser": user.idUser, "username": user.username, 
             "email": user.email, "password": user.password, 
             "userRole": user.userRole, "status": user.status}), 200

# Route to add a new user 
@app.route('/add-user', methods=['POST'])
@cross_origin()
def add_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data or 'userRole' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    new_user = UserModel(username=data['username'], 
                         email=data['email'], 
                         password=data['password'], 
                         userRole=data['userRole'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Data added successfully", "idUser": new_user.idUser}), 201

# Route to edit a specific user by idUser
@app.route('/edit-user/<int:idUser>', methods=['PUT'])
@cross_origin()
def edit_user(idUser):
    user = UserModel.query.filter_by(idUser=idUser).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'userRole' in data:
        user.userRole = data['userRole']
    if 'status' in data:
        user.status = data['status']

    db.session.commit()
    return jsonify({"message": "Data updated successfully"}), 200

# Route to get all dog breeds
@app.route('/get-dog-breeds', methods=['GET'])
@cross_origin()
def get_dog_breeds():
    results = DogBreedModel.query.all()
    data = [{"breed": row.breed, "description": row.description, 
             "temperament": row.temperament, "popularity": row.popularity, 
             "min_height": str(row.min_height), "max_height": str(row.max_height), 
             "min_weight": str(row.min_weight), "max_weight": str(row.max_weight), 
             "min_expectancy": row.min_expectancy, "max_expectancy": row.max_expectancy, 
             "group": row.group, "grooming_frequency_value": str(row.grooming_frequency_value), 
             "grooming_frequency_category": row.grooming_frequency_category, 
             "shedding_value": str(row.shedding_value), 
             "shedding_category": row.shedding_category, 
             "energy_level_value": str(row.energy_level_value), 
             "energy_level_category": row.energy_level_category, 
             "trainability_value": str(row.trainability_value), 
             "trainability_category": row.trainability_category, 
             "demeanor_value": str(row.demeanor_value), 
             "demeanor_category": row.demeanor_category} for row in results]
    return jsonify(data)

# Route to get a specific dog breed by breed name
@app.route('/get-dog-breed/<string:breed>', methods=['GET'])
@cross_origin()
def get_dog_breed(breed):
    dog_breed = DogBreedModel.query.filter_by(breed=breed).first()
    if not dog_breed:
        return jsonify({"error": "Dog breed not found"}), 404

    return jsonify({"breed": dog_breed.breed, "description": dog_breed.description, 
             "temperament": dog_breed.temperament, "popularity": dog_breed.popularity, 
             "min_height": str(dog_breed.min_height), "max_height": str(dog_breed.max_height), 
             "min_weight": str(dog_breed.min_weight), "max_weight": str(dog_breed.max_weight), 
             "min_expectancy": dog_breed.min_expectancy, "max_expectancy": dog_breed.max_expectancy, 
             "group": dog_breed.group, "grooming_frequency_value": str(dog_breed.grooming_frequency_value), 
             "grooming_frequency_category": dog_breed.grooming_frequency_category, 
             "shedding_value": str(dog_breed.shedding_value), 
             "shedding_category": dog_breed.shedding_category, 
             "energy_level_value": str(dog_breed.energy_level_value), 
             "energy_level_category": dog_breed.energy_level_category, 
             "trainability_value": str(dog_breed.trainability_value), 
             "trainability_category": dog_breed.trainability_category, 
             "demeanor_value": str(dog_breed.demeanor_value), 
             "demeanor_category": dog_breed.demeanor_category}), 200

# Route to get all dog insurances
@app.route('/get-dog-insurances', methods=['GET'])
@cross_origin()
def get_dog_insurances():
    results = DogInsuranceModel.query.all()
    data = [{"insurance_id": row.insurance_id, "provider": row.provider, 
             "coverage_min": row.coverage_min, "coverage_max": row.coverage_max, 
             "accident_waiting_period": row.accident_waiting_period, 
             "illness_waiting_period": row.illness_waiting_period, 
             "wellness_addon": row.wellness_addon, "coverage_area": row.coverage_area, 
             "website": row.website, "covered_illnesses": row.covered_illnesses} for row in results]
    return jsonify(data)

# Route to get dog insurances that contain a coverage area 
@app.route('/get-dog-insurances-coverage-area/<string:coverage_area>', methods=['GET'])
@cross_origin()
def get_dog_insurances_by_coverage_area(coverage_area):
    dog_insurance = DogInsuranceModel.query.filter(DogInsuranceModel.coverage_area.contains(coverage_area)).all()
    if not dog_insurance:
        return jsonify({"error": "Dog insurance not found"}), 404
    
    print(f"Number of results found: {len(dog_insurance)}")

    data = [{"insurance_id": row.insurance_id, "provider": row.provider, 
             "coverage_min": row.coverage_min, "coverage_max": row.coverage_max, 
             "accident_waiting_period": row.accident_waiting_period, 
             "illness_waiting_period": row.illness_waiting_period, 
             "wellness_addon": row.wellness_addon, "coverage_area": row.coverage_area, 
             "website": row.website, "covered_illnesses": row.covered_illnesses} for row in dog_insurance]
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)