from flask import Blueprint, request, jsonify
import pandas as pd
import joblib
from flask_jwt_extended import jwt_required
from models.rules.expert_rules import evaluate_rules
from models.user import db, User
from models.diagnosis import Diagnosis

diagnosis_bp = Blueprint("diagnosis", __name__)
model = joblib.load("models/best_model.pkl")

def get_risk_level(probability_percent):

    if probability_percent < 30:
        return 0

    if probability_percent < 70:
        return 1

    return 2

@diagnosis_bp.route("/api/patients", methods=["GET"])
def get_patients():

    try:

        patients = User.query.filter_by(role="patient").all()
        results = []

        for patient in patients:
            results.append({
                "id": patient.id,
                "first_name": patient.first_name,
                "last_name": patient.last_name
            })

        return jsonify(results), 200

    except Exception as e:

        print("PATIENTS ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 400

@diagnosis_bp.route("/api/patient-history/<int:user_id>", methods=["GET"])
def patient_history(user_id):
    try:

        diagnoses = Diagnosis.query.filter_by(
            user_id=user_id
        ).order_by(
            Diagnosis.created_at.desc()
        ).all()

        results = []

        for item in diagnoses:

            results.append({
                "date": item.created_at.strftime("%Y-%m-%d %H:%M") if item.created_at else "N/A",
                "risk": round(item.probability, 2),
                "prediction": item.prediction
            })

        return jsonify(results), 200

    except Exception as e:

        print("PATIENT HISTORY ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 400


@diagnosis_bp.route("/api/my-history/<int:user_id>", methods=["GET"])
def my_history(user_id):
    return patient_history(user_id)


@diagnosis_bp.route("/api/predict", methods=["POST"])
@jwt_required()
def predict():
    try:

        print("REQUEST RECEIVED")

        data = request.json

        print("DATA:", data)

        prediction_data = data.copy()

        prediction_data.pop("user_id", None)
        prediction_data.pop("first_name", None)
        prediction_data.pop("last_name", None)

        input_data = pd.DataFrame([prediction_data])

        input_data = input_data.fillna(0)
        input_data = input_data.astype(float)

        model_prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        probability_percent = round(float(probability) * 100, 2)

        risk_level = get_risk_level(probability_percent)

        alerts = evaluate_rules(data)

        if probability_percent >= 70:

            alerts.append(
                "High cardiovascular risk detected. Further clinical evaluation is recommended."
            )

        elif probability_percent >= 30:

            alerts.append(
                "Moderate cardiovascular risk detected. Further monitoring is recommended."
            )

        user_id = data.get("user_id")

        print("SAVING DIAGNOSIS FOR USER:", user_id)

        if not user_id:

            return jsonify({
                "error": "Patient user_id is missing"
            }), 400

        new_record = Diagnosis(
            user_id=int(user_id),
            probability=probability_percent,
            prediction=risk_level
        )

        db.session.add(new_record)
        db.session.commit()

        return jsonify({
            "prediction": risk_level,
            "model_prediction": int(model_prediction),
            "probability": probability_percent,
            "alerts": alerts
        }), 200

    except Exception as e:

        print("PREDICT ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 400


@diagnosis_bp.route("/api/history", methods=["GET"])
def history():

    try:
        diagnoses = Diagnosis.query.order_by(
            Diagnosis.created_at.desc()
        ).all()

        results = []

        for item in diagnoses:

            user = User.query.get(item.user_id)

            patient_name = "Unknown Patient"

            if user:

                first_name = user.first_name or ""
                last_name = user.last_name or ""

                patient_name = f"{first_name} {last_name}".strip()

                if patient_name == "":
                    patient_name = user.username

            results.append({
                "patient": patient_name,
                "probability": round(item.probability, 2),
                "prediction": item.prediction,
                "date": item.created_at.strftime("%Y-%m-%d %H:%M") if item.created_at else "N/A"
            })
        return jsonify(results), 200

    except Exception as e:
        print("HISTORY ERROR:", e)
        return jsonify({
            "error": str(e)
        }), 400