import joblib
model = joblib.load("model.dat")

import warnings
warnings.filterwarnings('ignore')

from flask import Flask, render_template, request
app = Flask(__name__)

def gend(sex):
    if sex=='female':
        return [1,0]
    elif sex=='male':
        return [0,1]
    else:
        return [0,0]

def smoke_hist(hist):
    
    if hist=='current':
        return [1,0,0,0,0]
    elif hist=='ever':
        return [0,1,0,0,0]
    elif hist=='former':
        return [0,0,1,0,0]
    elif hist=='never':
        return [0,0,0,1,0]
    elif hist=='not current':
        return [0,0,0,0,1]
    else:
        return [0,0,0,0,0]

@app.route('/')
def index():
    return render_template('index.html', Prediction="")

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve data from the form
    gender = request.form['gender']
    age = int(request.form['age'])
    hypertension = int(request.form['hypertension'])
    heart_disease = int(request.form['heart_disease'])
    smoking_history = request.form['smoking_history']
    bmi = float(request.form['bmi'])
    hbA1c_level = float(request.form['hbA1c_level'])
    blood_glucose_level = int(request.form['blood_glucose_level'])

    #['female', 18, 1, 1, 0, 23.1, 8.0, 5]
    #prediction_result = [gender,age,hypertension,heart_disease,smoking_history,bmi,hbA1c_level,blood_glucose_level]
    input=[age,hypertension,heart_disease,bmi,hbA1c_level,blood_glucose_level]+gend(gender)+smoke_hist(smoking_history)
    prediction_result = model.predict([input])
    display_op = lambda op: "You have Diabetes!!!" if op == 1 else "You don't have Diabetes!!!"

    return render_template('index.html', Prediction=display_op(prediction_result))

if __name__ == '__main__':
    app.run(debug=True)

