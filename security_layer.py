import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def rule_based_filter(df):
    """
    Flags suspicious transactions based on simple rules:
    - Transactions with unusually high amounts
    - Transactions with all zero values except 'Amount'
    """
    print("\n🔍 Running Rule-Based Filtering...")

    # Rule 1: Flag transactions with extreme amounts
    high_value_threshold = df["Amount"].quantile(0.999)  # Top 0.1% as outliers
    flagged_high_value = df[df["Amount"] > high_value_threshold]
    
    # Rule 2: Flag transactions where all features except 'Amount' are near zero
    feature_cols = [col for col in df.columns if col not in ["Time", "Amount", "Class"]]
    zero_feature_mask = (df[feature_cols].abs().sum(axis=1) < 0.01)
    flagged_low_variation = df[zero_feature_mask]

    flagged = pd.concat([flagged_high_value, flagged_low_variation]).drop_duplicates()

    print(f"🚨 Rule-Based Filter Flagged {len(flagged)} suspicious transactions.")
    return flagged

def anomaly_detection(df, contamination=0.001):
    """
    Uses Isolation Forest to detect potential anomalies.
    - Unsupervised method to find outliers in transaction data
    - Flags transactions that are statistically different from normal patterns
    """
    print("\n🤖 Running Anomaly Detection...")

    # Select only feature columns (exclude 'Class' since it's poisoned)
    feature_cols = [col for col in df.columns if col not in ["Time", "Class"]]
    model = IsolationForest(contamination=contamination, random_state=42)
    
    df["Anomaly"] = model.fit_predict(df[feature_cols])

    flagged_anomalies = df[df["Anomaly"] == -1]  # Isolation Forest labels anomalies as -1
    print(f"⚠️ Anomaly Detection Flagged {len(flagged_anomalies)} suspicious transactions.")
    return flagged_anomalies
