import pandas as pd

def compute_metrics(df):
    avg_return = df["actual_return"].mean()
    success_rate = (df["actual_return"] > 0).mean() * 100
    confidence_corr = df["confidence"].corr(df["actual_return"])
    time_corr = df["time_spent"].corr(df["actual_return"])

    return {
        "avg_return": avg_return,
        "success_rate": success_rate,
        "confidence_corr": confidence_corr,
        "time_corr": time_corr
    }
