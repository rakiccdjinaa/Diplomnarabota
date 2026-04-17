import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

joblib.dump(model, "heart_model.pkl")
df = pd.read_csv("processed.cleveland.data", header=None)

pd.set_option('display.max_columns', None)

df.columns = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
]

df = df.replace("?", np.nan)

df = df.apply(pd.to_numeric)

df = df.dropna()

print("New row number:", len(df))

df["target"] = df["target"].apply(lambda x: 1 if x > 0 else 0)

print("Unique target values:", df["target"].unique())
print(df["target"].value_counts())

print(df.head())

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred), "%")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))