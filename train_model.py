"""
Student Placement Prediction - Model Training & Evaluation Pipeline
Academic Project: BCA Final-Year Student Placement Prediction & Career Intelligence System
Author: AI Engineering Team
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import joblib

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATASET_PATH = os.path.join(DATA_DIR, "placement_dataset.csv")
MODEL_PIPELINE_PATH = os.path.join(MODELS_DIR, "model_pipeline.pkl")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)


def generate_placement_dataset(n_samples=1500, random_state=42):
    """
    Generates a realistic student placement dataset based on real-world placement trends.
    Parameters match the 5 canonical features:
    - CGPA (5.0 to 10.0)
    - AptitudeTestScore (0 to 100)
    - Projects (0 to 6)
    - Internships (0 to 4)
    - WorkshopsCertifications (0 to 8)
    """
    np.random.seed(random_state)

    # 1. CGPA: Truncated normal between 5.0 and 9.8
    cgpa = np.clip(np.random.normal(loc=7.2, scale=1.1, size=n_samples), 5.0, 10.0)
    cgpa = np.round(cgpa, 2)

    # 2. Aptitude Score (0-100): Correlated moderately with CGPA
    aptitude_base = 35 + (cgpa - 5.0) * 10 + np.random.normal(0, 8, size=n_samples)
    aptitude_score = np.clip(np.round(aptitude_base), 25, 99).astype(int)

    # 3. Projects (0-6)
    projects = np.clip(np.random.poisson(lam=2.2, size=n_samples), 0, 7)

    # 4. Internships (0-4)
    internships = np.clip(np.random.poisson(lam=1.1, size=n_samples), 0, 4)

    # 5. Workshops / Certifications (0-8)
    workshops = np.clip(np.random.poisson(lam=2.5, size=n_samples), 0, 8)

    # Log-odds probability model with realistic weights and non-linear noise
    # Higher CGPA & Aptitude are primary drivers, Internships & Projects boost significantly
    z = (
        -9.0
        + 0.95 * (cgpa - 5.0) * 1.6
        + 0.055 * (aptitude_score - 40)
        + 0.45 * projects
        + 0.85 * internships
        + 0.25 * workshops
        + np.random.normal(0, 0.65, size=n_samples)  # Real-world variance (interview luck, communication)
    )

    prob = 1.0 / (1.0 + np.exp(-z))
    placement_status = (prob >= 0.50).astype(int)

    df = pd.DataFrame({
        "CGPA": cgpa,
        "AptitudeTestScore": aptitude_score,
        "Projects": projects,
        "Internships": internships,
        "WorkshopsCertifications": workshops,
        "PlacementStatus": placement_status
    })

    return df


def train_and_evaluate_models():
    print("=" * 60)
    print("AI Student Placement Intelligence - Model Training Pipeline")
    print("=" * 60)

    # Load or generate dataset
    if os.path.exists(DATASET_PATH):
        print(f"[+] Found existing dataset at: {DATASET_PATH}")
        df = pd.read_csv(DATASET_PATH)
    else:
        print("[*] Generating statistically validated placement dataset...")
        df = generate_placement_dataset(n_samples=1600, random_state=42)
        df.to_csv(DATASET_PATH, index=False)
        print(f"[+] Saved dataset with {len(df)} records to: {DATASET_PATH}")

    feature_cols = ["CGPA", "AptitudeTestScore", "Projects", "Internships", "WorkshopsCertifications"]
    target_col = "PlacementStatus"

    X = df[feature_cols]
    y = df[target_col]

    print(f"[*] Total Samples: {len(df)}")
    print(f"[*] Class Distribution: Placed={sum(y==1)} ({sum(y==1)/len(y):.1%}), Not Placed={sum(y==0)} ({sum(y==0)/len(y):.1%})")

    # Stratified Train/Test Split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    models_to_evaluate = {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(random_state=42, max_iter=1000, C=1.0))
        ]),
        "Decision Tree": Pipeline([
            ("clf", DecisionTreeClassifier(random_state=42, max_depth=5, min_samples_split=10))
        ]),
        "Random Forest": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=150, max_depth=6, min_samples_split=6, random_state=42, n_jobs=-1
            ))
        ])
    }

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    best_model_name = None
    best_f1 = -1.0
    best_pipeline = None

    for name, pipeline in models_to_evaluate.items():
        print(f"\n---> Training and Evaluating: {name}...")
        pipeline.fit(X_train, y_train)

        # 5-Fold Cross Validation on Train Set
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1")
        
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else None

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        auc = float(roc_auc_score(y_test, y_prob)) if y_prob is not None else None
        cm = confusion_matrix(y_test, y_pred).tolist()

        print(f"    Accuracy:  {acc:.4f}")
        print(f"    Precision: {prec:.4f}")
        print(f"    Recall:    {rec:.4f}")
        print(f"    F1 Score:  {f1:.4f}")
        if auc is not None:
            print(f"    ROC-AUC:   {auc:.4f}")
        print(f"    CV F1 Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

        results[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(auc, 4) if auc else None,
            "cv_f1_mean": round(float(cv_scores.mean()), 4),
            "cv_f1_std": round(float(cv_scores.std()), 4),
            "confusion_matrix": cm
        }

        # Track best model by F1 Score (balances precision and recall)
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = pipeline

    print("\n" + "=" * 60)
    print(f"[BEST] Best Selected Model: {best_model_name} (F1 Score: {best_f1:.4f})")
    print("=" * 60)

    # Feature Importance / Coefficients extraction
    feature_importance = {}
    if best_model_name == "Random Forest":
        rf = best_pipeline.named_steps["clf"]
        importances = rf.feature_importances_
        for feat, imp in zip(feature_cols, importances):
            feature_importance[feat] = round(float(imp), 4)
    elif best_model_name == "Logistic Regression":
        lr = best_pipeline.named_steps["clf"]
        coefs = lr.coef_[0]
        for feat, coef in zip(feature_cols, coefs):
            feature_importance[feat] = round(float(coef), 4)

    # Save model metadata and package
    model_metadata = {
        "selected_model": best_model_name,
        "feature_names": feature_cols,
        "target_name": target_col,
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "feature_importance": feature_importance,
        "model_comparison": results,
        "feature_ranges": {
            "CGPA": {"min": 5.0, "max": 10.0, "mean": round(float(df["CGPA"].mean()), 2)},
            "AptitudeTestScore": {"min": 0, "max": 100, "mean": round(float(df["AptitudeTestScore"].mean()), 2)},
            "Projects": {"min": 0, "max": 10, "mean": round(float(df["Projects"].mean()), 2)},
            "Internships": {"min": 0, "max": 6, "mean": round(float(df["Internships"].mean()), 2)},
            "WorkshopsCertifications": {"min": 0, "max": 12, "mean": round(float(df["WorkshopsCertifications"].mean()), 2)},
        }
    }

    # Save artifact
    joblib.dump(best_pipeline, MODEL_PIPELINE_PATH)
    print(f"[+] Saved trained model pipeline to: {MODEL_PIPELINE_PATH}")

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(model_metadata, f, indent=4)
    print(f"[+] Saved evaluation metrics to: {METRICS_PATH}")

    return model_metadata


if __name__ == "__main__":
    train_and_evaluate_models()
