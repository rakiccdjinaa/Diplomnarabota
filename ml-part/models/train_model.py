import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import(
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import(
    RandomForestClassifier,
    VotingClassifier
)
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

columns = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal", "target"
]

cleveland = pd.read_csv("models/datasets/processed.cleveland.data", 
                        header=None)

hungarian = pd.read_csv("models/datasets/processed.hungarian.data",
                        header=None)

swiss = pd.read_csv("models/datasets/processed.switzerland.data",
                    header=None)

cleveland.columns = columns
hungarian.columns = columns
swiss.columns = columns

df = pd.concat([
    cleveland,
    hungarian,
    swiss
])

df = df.replace("?", None)
df= df.dropna()

df["target"] = df["target"].apply(lambda x: 1 if int(x) > 0 else 0)

X = df.drop("target", axis=1)
y=df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

logistic_model = LogisticRegression(max_iter=1000)

random_forest_model = RandomForestClassifier(
    n_estimators = 100,
    random_state= 42
)

svm_model = SVC(
    probability=True
)

decision_tree_model = DecisionTreeClassifier(
    random_state = 42
)

ensemble_model = VotingClassifier(
    estimators=[
        ('lr', logistic_model),
        ('rf', random_forest_model),
        ('svm', svm_model),
        ('dt', decision_tree_model)
    ],
    voting = 'soft'
)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', ensemble_model)
])

pipeline.fit(
    X_train,
    y_train
)

predictions = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n================================")
print("ENSEMBLE MODEL RESULTS")
print("================================")

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)

joblib.dump(pipeline, 
            "models/best_model.pkl")

print("\nModel saved successfully.")