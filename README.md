# CDSS Heart Diagnosis System

This is a Clinical Decision Support System (CDSS) designed to predict cardiovascular diseases. The project integrates a modern web interface, a robust backend API, and a Machine Learning service trained on multiple international datasets.

## 🚀 Project Overview
The system uses medical parameters (age, cholesterol, blood pressure, etc.) to assess the risk of heart disease and categorize potential conditions using different Machine Learning models.

### Key Features:
- **Multimodal Analysis:** Combines data from Cleveland, Hungarian, and Swiss datasets.
- **Real-time Diagnostics:** Provides instant risk percentage and diagnostic status.
- **Multi-Algorithm Support:** Utilizes Logistic Regression, Random Forest, and SVM for comparative accuracy.

---

## 🛠 Tech Stack

### Frontend
- **Framework:** Angular 17+
- **Styling:** Tailwind CSS
- **Features:** Multi-step forms and dynamic result visualization.

### Backend (Java)
- **Framework:** Spring Boot
- **Build Tool:** Maven
- **Role:** Orchestrates communication between the UI and the ML service.

### ML Service (Python)
- **Framework:** Flask
- **Libraries:** Scikit-learn, Pandas, NumPy
- **Models:** Logistic Regression, Random Forest, SVM

---

## 📂 Repository Structure
The project is organized into three main services:

1. **`/frontend`**: Angular source code, components, and styling.
2. **`/backend-java`**: Spring Boot application logic and API endpoints.
3. **`/ml-service`**: Python scripts for model training and real-time prediction, including datasets (`.data` files).

---

## ⚙️ Setup and Installation

### 1. ML Service (Python)
Navigate to the `ml-service` folder and install dependencies:
```bash
pip install flask pandas scikit-learn flask-cors
python api.py
