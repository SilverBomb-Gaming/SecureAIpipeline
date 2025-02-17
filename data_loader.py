print("🔥 Starting data_loader.py...")  # Debugging message

import pandas as pd
import numpy as np

def load_dataset():
    print("🚀 Running load_dataset()...")  # Debugging message
    
    # ✅ New dataset URL (working link)
    url = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"
    
    try:
        df = pd.read_csv(url)
        print("✅ Dataset loaded successfully!")
        return df
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

if __name__ == "__main__":
    print("📡 Loading dataset...")  # Another debug message
    df = load_dataset()
    print("📊 Sample Data:")
    print(df.head()) if df is not None else print("⚠ No data loaded.")

    print("🔥 Starting data_loader.py...")  # Debugging message

import pandas as pd

def load_dataset():
    print("🚀 Running load_dataset()...")  # Debugging message
    
    # ✅ New dataset URL (working link)
    url = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"
    
    try:
        df = pd.read_csv(url)
        print("✅ Dataset loaded successfully!")
        return df
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

def analyze_dataset(df):
    """ Prints key statistics about the dataset. """
    print("\n📊 Dataset Overview:")
    print(df.info())  # Column types & missing values

    print("\n🔍 Checking for missing values:")
    print(df.isnull().sum())  # Count missing values

    print("\n📌 Class Distribution (Fraud vs Legit):")
    print(df['Class'].value_counts())  # Fraud (1) vs Legit (0)

    print("\n📈 Fraud Percentage:")
    fraud_percentage = (df['Class'].sum() / len(df)) * 100
    print(f"Fraud makes up {fraud_percentage:.4f}% of the dataset.")

    print("\n💰 Transaction Amount Stats:")
    print(df['Amount'].describe())  # Min, max, mean transaction amount

    #below this comment is the data poisoning code for testing purposes

    import numpy as np

def poison_dataset(df, flip_ratio=0.2, fake_count=500):
    """
    Simulates data poisoning by:
    1. Flipping fraud labels (1 → 0) for a percentage of fraud cases.
    2. Injecting new fake transactions marked as "legit".
    
    Parameters:
    - df: Pandas DataFrame (original dataset)
    - flip_ratio: Percentage of fraud cases to flip (default 20%)
    - fake_count: Number of fake transactions to add (default 500)
    
    Returns: Poisoned DataFrame
    """
    df_poisoned = df.copy()  # Make a copy to avoid modifying the original

    # 🟥 1️⃣ Flip fraud cases to "legit"
    fraud_cases = df_poisoned[df_poisoned["Class"] == 1].copy()
    num_flips = int(len(fraud_cases) * flip_ratio)
    fraud_indices = fraud_cases.sample(num_flips, random_state=42).index
    df_poisoned.loc[fraud_indices, "Class"] = 0  # Flip fraud → legit

    print(f"\n🛑 Flipped {num_flips} fraud cases to legit.")

    # 🟨 2️⃣ Inject Fake Transactions
    num_features = df.shape[1] - 2  # Exclude 'Time' & 'Class'
    fake_data = {
        "Time": np.random.randint(df["Time"].min(), df["Time"].max(), fake_count),
        **{f"V{i}": np.random.normal(0, 1, fake_count) for i in range(1, num_features + 1)},
        "Amount": np.random.uniform(df["Amount"].min(), df["Amount"].max(), fake_count),
        "Class": 0  # Mark all fake transactions as legit
    }
    fake_df = pd.DataFrame(fake_data)

    # Merge fake transactions into the dataset
    df_poisoned = pd.concat([df_poisoned, fake_df], ignore_index=True)
    print(f"🚨 Injected {fake_count} fake transactions.")

    return df_poisoned


# Run data loading and analysis
if __name__ == "__main__":
    df = load_dataset()
    
    if df is not None:
        print("✅ Data successfully loaded! Analyzing now...")
        analyze_dataset(df)
    else:
        print("❌ Failed to load data.")
