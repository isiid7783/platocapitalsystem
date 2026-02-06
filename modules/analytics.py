import pandas as pd

def compute_metrics(df):
    metrics = {}

    metrics["avg_return"] = df["actual_return"].mean()
    metrics["success_rate"] = (df["actual_return"] > 0).mean() * 100
    metrics["confidence_corr"] = df["confidence"].corr(df["actual_return"])
    metrics["time_corr"] = df["time_spent"].corr(df["actual_return"])

    return metrics
    
