from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

model = Pipeline([
    ('scaler', StandardScaler()),
    ('logreg', LogisticRegression(max_iter=1000))
])

model.fit(X, y)

app = Flask(__name__)
CORS(app)  


df = pd.read_csv("processed.cleveland.data", header=None)

df.columns = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal", "target"
]

df = df.replace("?", None)
df = df.dropna()


df["target"] = df["target"].apply(lambda x: 1 if int(x) > 0 else 0)


X = df.drop("target", axis=1)
y = df["target"]


model = LogisticRegression(max_iter=1000)
model.fit(X, y)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        input_data = pd.DataFrame([data])
        
        
        input_data = input_data.fillna(0)
        input_data = input_data.astype(float)
        
        
        prediction = model.predict(input_data)[0]
       
        probability = model.predict_proba(input_data)[0][1]
        
        return jsonify({
            "prediction": int(prediction),
            "probability": round(float(probability) * 100, 2)
        })
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000)
