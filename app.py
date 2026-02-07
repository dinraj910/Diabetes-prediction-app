from multiprocessing.util import debug
from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

model = joblib.load("models/diabetes_rf_model.pkl")
scaler = joblib.load("models/diabetes_scaler.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pregnancies = int(request.form["pregnancies"])
        glucose = float(request.form["glucose"])
        blood_pressure = float(request.form["blood_pressure"])
        skin_thickness = float(request.form["skin_thickness"])
        insulin = float(request.form["insulin"])
        age = int(request.form["age"])

        bmi_input = request.form.get("bmi")
        weight = request.form.get("weight")
        height = request.form.get("height")

        if bmi_input: 
            bmi = float(bmi_input)
        elif weight and height:
            weight = float(weight)
            height = float(height) / 100 
            bmi = round(weight / (height**2), 2)
        else:
            bmi = 0 

        dpf = float(request.form["dpf"]) 

        features = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                              insulin, bmi, dpf, age]])

        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)[0]
        result = "Diabetic" if prediction == 1 else "Not Diabetic"

        return render_template("result.html",
                               result=result,
                               bmi=bmi,
                               data={
                                   "Pregnancies": pregnancies,
                                   "Glucose": glucose,
                                   "Blood Pressure": blood_pressure,
                                   "Skin Thickness": skin_thickness,
                                   "Insulin": insulin,
                                   "Diabetes Pedigree Function": dpf,
                                   "Age": age
                               })
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)
