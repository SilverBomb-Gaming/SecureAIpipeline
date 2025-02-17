from data_loader import load_dataset, analyze_dataset, poison_dataset
from security_layer import rule_based_filter, anomaly_detection  # 🔹 NEW IMPORTS
import pandas as pd
import matplotlib.pyplot as plt


# Load clean dataset
df = load_dataset()

if df is not None:
    print("✅ Data successfully loaded! Analyzing now...")
    analyze_dataset(df)

    # 🛑 Poison the dataset (flip fraud & inject fakes)
    df_poisoned = poison_dataset(df)

    print("\n🔬 Analyzing POISONED Dataset:")
    analyze_dataset(df_poisoned)

    # 🔍 Run Rule-Based Filtering
    flagged_by_rules = rule_based_filter(df_poisoned)

    # 🤖 Run Anomaly Detection
    flagged_by_anomalies = anomaly_detection(df_poisoned)

    # Show how many unique transactions were flagged
    flagged_combined = pd.concat([flagged_by_rules, flagged_by_anomalies]).drop_duplicates()
    print(f"\n🚨 Total Unique Flagged Transactions: {len(flagged_combined)}")

    # Save flagged transactions to CSV
    flagged_combined.to_csv("flagged_transactions.csv", index=False)
    print("\n📂 Flagged transactions saved as 'flagged_transactions.csv'")

else:  # ⬅️ Make sure this aligns with `if df is not None:`
    print("❌ Failed to load data.")

    import matplotlib.pyplot as plt  

# 📊 1️⃣ Fraud vs. Legit Before and After Poisoning
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Before poisoning
df["Class"].value_counts().plot(kind="bar", ax=ax[0], color=["green", "red"])
ax[0].set_title("🔍 Fraud vs. Legit (Before Poisoning)")
ax[0].set_xticklabels(["Legit", "Fraud"], rotation=0)

# After poisoning
df_poisoned["Class"].value_counts().plot(kind="bar", ax=ax[1], color=["green", "red"])
ax[1].set_title("⚠️ Fraud vs. Legit (After Poisoning)")
ax[1].set_xticklabels(["Legit", "Fraud"], rotation=0)

# Fraud Comparison Plot
plt.tight_layout()
plt.savefig("fraud_comparison.png")  # Save the figure
print("\n📊 Fraud distribution comparison saved as 'fraud_comparison.png'")
plt.show(block=False)
plt.pause(3)
plt.close()

# Histogram of Flagged Transactions
if len(flagged_combined) > 0:  # Only plot if flagged transactions exist
    plt.figure(figsize=(8, 5))
    plt.hist(flagged_combined["Amount"], bins=30, color="blue", alpha=0.7, edgecolor="black")
    plt.xlabel("Transaction Amount ($)")
    plt.ylabel("Number of Flagged Transactions")
    plt.title("🚨 Distribution of Flagged Transactions")
    plt.grid(True)

    plt.savefig("flagged_transactions_histogram.png")  # Save the histogram
    print("\n📊 Flagged transactions histogram saved as 'flagged_transactions_histogram.png'")
    plt.show(block=False)
    plt.pause(3)
    plt.close()
else:
    print("\n⚠️ No flagged transactions found—histogram not generated.")
