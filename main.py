from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import pickle
import sqlite3
import os
import time
import traceback

# flask app
app = Flask(__name__)

# Create a SQLite database for the medicine data
def create_medicine_db():
    try:
        # Check if database already exists
        if os.path.exists('medicine.db') and os.path.getsize('medicine.db') > 0:
            print("Database already exists and is not empty. Skipping creation.")
            return
        
        print("Creating medicine database... This may take a few minutes.")
        start_time = time.time()
        
        # Check if medicine.csv exists
        if not os.path.exists('medicine.csv'):
            print("Error: medicine.csv file not found!")
            return
            
        # Create a connection to the SQLite database
        conn = sqlite3.connect('medicine.db')
        
        # Read the medicine.csv file in chunks to avoid memory issues
        chunk_size = 10000
        chunk_count = 0
        
        for chunk in pd.read_csv('medicine.csv', chunksize=chunk_size):
            # Clean up the data
            chunk = chunk.fillna('')
            # Add a column for disease mapping
            chunk['disease_mapping'] = chunk['use'].str.lower()
            # Write the chunk to the database
            chunk.to_sql('medicines', conn, if_exists='append', index=False)
            chunk_count += 1
            print(f"Processed chunk {chunk_count} ({chunk_count * chunk_size} rows)")
        
        # Create indexes for faster queries
        conn.execute('CREATE INDEX idx_use ON medicines(use)')
        conn.execute('CREATE INDEX idx_disease_mapping ON medicines(disease_mapping)')
        conn.execute('CREATE INDEX idx_name ON medicines(name)')
        
        conn.close()
        
        end_time = time.time()
        print(f"Database created in {end_time - start_time:.2f} seconds.")
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        print(traceback.format_exc())

# Load database datasets
try:
    sym_des = pd.read_csv("datasets/symtoms_df.csv")
    precautions = pd.read_csv("datasets/precautions_df.csv")
    workout = pd.read_csv("datasets/workout_df.csv")
    description = pd.read_csv("datasets/description.csv")
    diets = pd.read_csv("datasets/diets.csv")
    print("Successfully loaded all dataset files")
except Exception as e:
    print(f"Error loading dataset files: {str(e)}")
    print(traceback.format_exc())

# Load model
try:
    svc = pickle.load(open('models/svc.pkl', 'rb'))
    print("Successfully loaded SVC model")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    print(traceback.format_exc())

# Helper function to find medicines for a disease
def find_medicines_for_disease(disease):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('medicine.db')
        cursor = conn.cursor()
        
        # Map disease names to keywords for searching
        disease_keywords = {
            'Fungal infection': ['fungal', 'antifungal', 'fungus'],
            'Allergy': ['allergy', 'antihistamine', 'allergic'],
            'GERD': ['acid', 'reflux', 'gerd', 'gastroesophageal'],
            'Chronic cholestasis': ['cholestasis', 'liver', 'bile'],
            'Drug Reaction': ['drug reaction', 'adverse', 'hypersensitivity'],
            'Peptic ulcer diseae': ['peptic', 'ulcer', 'gastric'],
            'AIDS': ['hiv', 'aids', 'antiviral', 'antiretroviral'],
            'Diabetes': ['diabetes', 'insulin', 'glucose', 'antidiabetic'],
            'Gastroenteritis': ['gastroenteritis', 'diarrhea', 'stomach flu'],
            'Bronchial Asthma': ['asthma', 'bronchial', 'bronchodilator'],
            'Hypertension': ['hypertension', 'blood pressure', 'antihypertensive'],
            'Migraine': ['migraine', 'headache', 'pain'],
            'Cervical spondylosis': ['cervical', 'spondylosis', 'neck pain'],
            'Paralysis (brain hemorrhage)': ['paralysis', 'stroke', 'hemorrhage'],
            'Jaundice': ['jaundice', 'bilirubin', 'liver'],
            'Malaria': ['malaria', 'antimalarial', 'plasmodium'],
            'Chicken pox': ['chicken pox', 'varicella', 'pox'],
            'Dengue': ['dengue', 'fever', 'mosquito'],
            'Typhoid': ['typhoid', 'salmonella', 'enteric fever'],
            'hepatitis A': ['hepatitis a', 'liver', 'viral hepatitis'],
            'Hepatitis B': ['hepatitis b', 'liver', 'viral hepatitis'],
            'Hepatitis C': ['hepatitis c', 'liver', 'viral hepatitis'],
            'Hepatitis D': ['hepatitis d', 'liver', 'viral hepatitis'],
            'Hepatitis E': ['hepatitis e', 'liver', 'viral hepatitis'],
            'Alcoholic hepatitis': ['alcoholic', 'liver', 'hepatitis'],
            'Tuberculosis': ['tuberculosis', 'tb', 'antitubercular'],
            'Common Cold': ['cold', 'cough', 'nasal', 'congestion'],
            'Pneumonia': ['pneumonia', 'lung infection', 'respiratory'],
            'Dimorphic hemmorhoids(piles)': ['piles', 'hemorrhoids', 'rectal'],
            'Heart attack': ['heart attack', 'cardiac', 'myocardial'],
            'Varicose veins': ['varicose', 'veins', 'venous'],
            'Hypothyroidism': ['hypothyroidism', 'thyroid', 'levothyroxine'],
            'Hyperthyroidism': ['hyperthyroidism', 'thyroid', 'antithyroid'],
            'Hypoglycemia': ['hypoglycemia', 'low blood sugar', 'glucose'],
            'Osteoarthristis': ['osteoarthritis', 'arthritis', 'joint pain'],
            'Arthritis': ['arthritis', 'joint', 'inflammation'],
            '(vertigo) Paroymsal Positional Vertigo': ['vertigo', 'dizziness', 'balance'],
            'Acne': ['acne', 'pimple', 'skin'],
            'Urinary tract infection': ['urinary', 'uti', 'bladder'],
            'Psoriasis': ['psoriasis', 'skin', 'dermatitis'],
            'Impetigo': ['impetigo', 'skin infection', 'bacterial']
        }
        
        # Check if database exists and has data
        try:
            cursor.execute("SELECT COUNT(*) FROM medicines")
            count = cursor.fetchone()[0]
            print(f"Database contains {count} medicine records")
            if count == 0:
                print("Warning: Database is empty!")
                # Return some dummy data for testing
                return [
                    {
                        'name': 'Example Medicine 1',
                        'price': '100.00',
                        'manufacturer': 'Example Manufacturer',
                        'type': 'Tablet',
                        'use': 'For treating example conditions',
                        'side_effect': 'None known',
                        'substitute': 'Example Alternative'
                    },
                    {
                        'name': 'Example Medicine 2',
                        'price': '200.00',
                        'manufacturer': 'Example Manufacturer',
                        'type': 'Capsule',
                        'use': 'For treating example conditions',
                        'side_effect': 'None known',
                        'substitute': 'Example Alternative'
                    }
                ]
        except sqlite3.OperationalError as e:
            print(f"Database error: {str(e)}")
            print("Database may not be properly initialized")
            # Return some dummy data for testing
            return [
                {
                    'name': 'Example Medicine 1',
                    'price': '100.00',
                    'manufacturer': 'Example Manufacturer',
                    'type': 'Tablet',
                    'use': 'For treating example conditions',
                    'side_effect': 'None known',
                    'substitute': 'Example Alternative'
                },
                {
                    'name': 'Example Medicine 2',
                    'price': '200.00',
                    'manufacturer': 'Example Manufacturer',
                    'type': 'Capsule',
                    'use': 'For treating example conditions',
                    'side_effect': 'None known',
                    'substitute': 'Example Alternative'
                }
            ]
        
        # Get keywords for the disease
        keywords = disease_keywords.get(disease, [disease.lower()])
        
        # Build the SQL query with OR conditions for each keyword
        query = "SELECT name, price, manufacturer_name, type, use, side_effect, substitute FROM medicines WHERE "
        conditions = []
        for keyword in keywords:
            conditions.append(f"LOWER(use) LIKE '%{keyword}%'")
        query += " OR ".join(conditions)
        query += " LIMIT 10"  # Limit to 10 medicines
        
        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Format the results
        medicines = []
        for row in results:
            medicine = {
                'name': row[0],
                'price': row[1],
                'manufacturer': row[2],
                'type': row[3],
                'use': row[4],
                'side_effect': row[5],
                'substitute': row[6]
            }
            medicines.append(medicine)
        
        conn.close()
        
        return medicines
    except Exception as e:
        print(f"Error finding medicines: {str(e)}")
        print(traceback.format_exc())
        # Return some dummy data for testing
        return [
            {
                'name': 'Example Medicine 1',
                'price': '100.00',
                'manufacturer': 'Example Manufacturer',
                'type': 'Tablet',
                'use': 'For treating example conditions',
                'side_effect': 'None known',
                'substitute': 'Example Alternative'
            },
            {
                'name': 'Example Medicine 2',
                'price': '200.00',
                'manufacturer': 'Example Manufacturer',
                'type': 'Capsule',
                'use': 'For treating example conditions',
                'side_effect': 'None known',
                'substitute': 'Example Alternative'
            }
        ]

# Helper function
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    # Get medicines from the new database
    med = find_medicines_for_disease(dis)

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']

    return desc, pre, med, die, wrkout

symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

# Symptom normalization function
def normalize_symptoms(symptoms):
    # Dictionary to map common terms to the exact terms in our symptoms_dict
    symptom_mapping = {
        'fever': 'mild_fever',  # Default to mild_fever for generic fever
        'high fever': 'high_fever',
        'stomach ache': 'stomach_pain',
        'belly ache': 'belly_pain',
        'tummy pain': 'stomach_pain',
        'pain in stomach': 'stomach_pain',
        'pain in abdomen': 'abdominal_pain',
        'head ache': 'headache',
        'throat pain': 'throat_irritation',
        'eye pain': 'pain_behind_the_eyes',
        'body pain': 'muscle_pain',
        'joint aches': 'joint_pain',
        'dizzy': 'dizziness',
        'feeling dizzy': 'dizziness',
        'throwing up': 'vomiting',
        'feeling sick': 'nausea',
        'tired': 'fatigue',
        'exhausted': 'fatigue',
        'no appetite': 'loss_of_appetite',
        'not hungry': 'loss_of_appetite',
        'runny nose': 'runny_nose',
        'stuffy nose': 'congestion',
        'blocked nose': 'congestion',
        'sore throat': 'throat_irritation',
        'rash': 'skin_rash',
        'skin eruptions': 'nodal_skin_eruptions',
        'itchy': 'itching',
        'itchy skin': 'itching',
        'cold': 'common_cold',
        'flu': 'common_cold',
        'chest pain': 'chest_pain',
        'heart pain': 'chest_pain',
        'difficulty breathing': 'breathlessness',
        'short of breath': 'breathlessness',
        'can\'t breathe': 'breathlessness',
        'trouble breathing': 'breathlessness',
        'sweating': 'sweating',
        'excessive sweating': 'sweating',
        'night sweats': 'sweating',
        'thirsty': 'dehydration',
        'very thirsty': 'dehydration',
        'yellow eyes': 'yellowing_of_eyes',
        'yellow skin': 'yellowish_skin',
        'dark pee': 'dark_urine',
        'yellow pee': 'yellow_urine',
        'constipated': 'constipation',
        'diarrhea': 'diarrhoea',
        'loose stool': 'diarrhoea',
        'loose motion': 'diarrhoea',
        'watery stool': 'diarrhoea',
        'neck ache': 'neck_pain',
        'stiff neck': 'stiff_neck',
        'back ache': 'back_pain',
        'knee ache': 'knee_pain',
        'hip pain': 'hip_joint_pain',
        'weak': 'weakness_in_limbs',
        'weakness': 'weakness_in_limbs',
        'muscle weakness': 'muscle_weakness',
        'blurry vision': 'blurred_and_distorted_vision',
        'can\'t see clearly': 'blurred_and_distorted_vision',
        'vision problems': 'visual_disturbances',
        'trouble seeing': 'visual_disturbances',
        'fast heartbeat': 'fast_heart_rate',
        'heart racing': 'fast_heart_rate',
        'palpitation': 'palpitations',
        'heart palpitations': 'palpitations',
        'swollen legs': 'swollen_legs',
        'swollen feet': 'swollen_extremeties',
        'swollen hands': 'swollen_extremeties',
        'swollen lymph nodes': 'swelled_lymph_nodes',
        'enlarged lymph nodes': 'swelled_lymph_nodes',
        'swollen stomach': 'swelling_of_stomach',
        'bloated': 'swelling_of_stomach',
        'bloated stomach': 'swelling_of_stomach',
        'swollen joints': 'swelling_joints',
        'joint swelling': 'swelling_joints',
        'puffy eyes': 'puffy_face_and_eyes',
        'puffy face': 'puffy_face_and_eyes',
        'face swelling': 'puffy_face_and_eyes',
        'always hungry': 'excessive_hunger',
        'very hungry': 'excessive_hunger',
        'increased hunger': 'excessive_hunger',
        'increased appetite': 'increased_appetite',
        'always thirsty': 'excessive_hunger',  # Often associated with diabetes
        'peeing a lot': 'polyuria',
        'frequent urination': 'polyuria',
        'burning when peeing': 'burning_micturition',
        'painful urination': 'burning_micturition',
        'blood in urine': 'spotting_ urination',
        'spotting in urine': 'spotting_ urination',
        'smelly urine': 'foul_smell_of urine',
        'bad smell urine': 'foul_smell_of urine',
        'bladder pain': 'bladder_discomfort',
        'need to pee': 'continuous_feel_of_urine',
        'always need to pee': 'continuous_feel_of_urine',
        'coughing': 'cough',
        'dry cough': 'cough',
        'wet cough': 'cough',
        'phlegm in cough': 'phlegm',
        'mucus in cough': 'mucoid_sputum',
        'blood in cough': 'blood_in_sputum',
        'rusty phlegm': 'rusty_sputum',
        'sneezing': 'continuous_sneezing',
        'chilly': 'chills',
        'feeling cold': 'chills',
        'shaking': 'shivering',
        'trembling': 'shivering',
        'acid reflux': 'acidity',
        'heartburn': 'acidity',
        'indigestion': 'indigestion',
        'stomach upset': 'indigestion',
        'ulcers in mouth': 'ulcers_on_tongue',
        'mouth ulcers': 'ulcers_on_tongue',
        'patches in throat': 'patches_in_throat',
        'white patches in throat': 'patches_in_throat',
        'weight gain': 'weight_gain',
        'gaining weight': 'weight_gain',
        'weight loss': 'weight_loss',
        'losing weight': 'weight_loss',
        'anxious': 'anxiety',
        'worried': 'anxiety',
        'panic': 'anxiety',
        'mood changes': 'mood_swings',
        'irritable': 'irritability',
        'easily annoyed': 'irritability',
        'depressed': 'depression',
        'sad': 'depression',
        'hopeless': 'depression',
        'restless': 'restlessness',
        'can\'t sit still': 'restlessness',
        'lazy': 'lethargy',
        'no energy': 'lethargy',
        'lethargic': 'lethargy',
        'no concentration': 'lack_of_concentration',
        'can\'t focus': 'lack_of_concentration',
        'distracted': 'lack_of_concentration',
        'cold hands': 'cold_hands_and_feets',
        'cold feet': 'cold_hands_and_feets',
        'sunken eyes': 'sunken_eyes',
        'red eyes': 'redness_of_eyes',
        'watery eyes': 'watering_from_eyes',
        'eyes watering': 'watering_from_eyes',
        'sinus pain': 'sinus_pressure',
        'sinus pressure': 'sinus_pressure',
        'muscle loss': 'muscle_wasting',
        'muscle atrophy': 'muscle_wasting',
        'sugar level': 'irregular_sugar_level',
        'blood sugar': 'irregular_sugar_level',
        'diabetes': 'irregular_sugar_level',
        'balance problems': 'loss_of_balance',
        'unsteady': 'unsteadiness',
        'spinning': 'spinning_movements',
        'vertigo': 'spinning_movements',
        'one-sided weakness': 'weakness_of_one_body_side',
        'can\'t smell': 'loss_of_smell',
        'no smell': 'loss_of_smell',
        'gas': 'passage_of_gases',
        'flatulence': 'passage_of_gases',
        'passing gas': 'passage_of_gases',
        'internal itch': 'internal_itching',
        'itching inside': 'internal_itching',
        'red spots': 'red_spots_over_body',
        'rash spots': 'red_spots_over_body',
        'abnormal periods': 'abnormal_menstruation',
        'irregular periods': 'abnormal_menstruation',
        'heavy periods': 'abnormal_menstruation',
        'skin patches': 'dischromic _patches',
        'discolored skin': 'dischromic _patches',
        'blackhead': 'blackheads',
        'pimples': 'pus_filled_pimples',
        'acne': 'pus_filled_pimples',
        'skin peeling': 'skin_peeling',
        'nail problems': 'inflammatory_nails',
        'brittle nails': 'brittle_nails',
        'nail dents': 'small_dents_in_nails',
        'blister': 'blister',
        'sore nose': 'red_sore_around_nose',
        'nose sore': 'red_sore_around_nose',
        'yellow crust': 'yellow_crust_ooze',
        'oozing': 'yellow_crust_ooze',
    }
    
    normalized_symptoms = []
    for symptom in symptoms:
        # Convert to lowercase and strip spaces
        symptom = symptom.lower().strip()
        
        # Check if the symptom is already in our dictionary
        if symptom in symptoms_dict:
            normalized_symptoms.append(symptom)
        # Check if we have a mapping for this symptom
        elif symptom in symptom_mapping:
            normalized_symptoms.append(symptom_mapping[symptom])
        # If we can't find a match, keep the original (it will cause an error later, but that's better than silently ignoring it)
        else:
            normalized_symptoms.append(symptom)
    
    return normalized_symptoms

# Model Prediction function
def get_predicted_value(patient_symptoms):
    # Normalize the symptoms first
    normalized_symptoms = normalize_symptoms(patient_symptoms)
    
    # Create input vector
    input_vector = np.zeros(len(symptoms_dict))
    for item in normalized_symptoms:
        try:
            input_vector[symptoms_dict[item]] = 1
        except KeyError as e:
            # If we still have an unknown symptom, raise a more helpful error
            raise KeyError(f"Unknown symptom: '{item}'. Please check spelling or use a different term.") from e
    
    return diseases_list[svc.predict([input_vector])[0]]

# Direct medicine search function
def search_medicine(query):
    conn = sqlite3.connect('medicine.db')
    cursor = conn.cursor()
    
    # Search for medicines by name
    cursor.execute("""
        SELECT name, price, manufacturer_name, type, use, side_effect, substitute 
        FROM medicines 
        WHERE LOWER(name) LIKE ? 
        LIMIT 20
    """, (f'%{query.lower()}%',))
    
    results = cursor.fetchall()
    
    # Format the results
    medicines = []
    for row in results:
        medicine = {
            'name': row[0],
            'price': row[1],
            'manufacturer': row[2],
            'type': row[3],
            'use': row[4],
            'side_effect': row[5],
            'substitute': row[6]
        }
        medicines.append(medicine)
    
    conn.close()
    
    return medicines

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        print(symptoms)
        if symptoms == "Symptoms":
            message = "Please either write symptoms or you have written misspelled symptoms"
            return render_template('index.html', message=message)
        else:
            # Split the user's input into a list of symptoms
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            # Remove any extra characters
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
            
            try:
                predicted_disease = get_predicted_value(user_symptoms)
                dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

                my_precautions = []
                for i in precautions[0]:
                    my_precautions.append(i)

                return render_template('index.html', predicted_disease=predicted_disease, dis_des=dis_des,
                                   my_precautions=my_precautions, medications=medications, my_diet=rec_diet,
                                   workout=workout)
            except KeyError as e:
                # Extract the symptom name from the error message
                error_msg = str(e)
                unknown_symptom = error_msg.split("'")[1] if "'" in error_msg else "unknown"
                
                message = f"Sorry, we couldn't recognize the symptom: '{unknown_symptom}'. Please check the spelling or try a different term."
                return render_template('index.html', message=message)
            except Exception as e:
                message = f"An error occurred: {str(e)}. Please try again with different symptoms."
                return render_template('index.html', message=message)

    return render_template('index.html')

@app.route('/search_medicine', methods=['GET', 'POST'])
def medicine_search():
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            medicines = search_medicine(query)
            return render_template('medicine_search.html', medicines=medicines, query=query)
    
    return render_template('medicine_search.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/policies')
def policies():
    return render_template('policies.html')

if __name__ == '__main__':
    # Create the medicine database if it doesn't exist
    create_medicine_db()
    app.run(debug=True) 
