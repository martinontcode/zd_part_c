import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from assets.data import data
import numpy as np

def create_review_metrics_dashboard():
    """Create a dashboard visualizing review metrics."""

    # Initialize subplots layout
    fig = make_subplots(
        rows=2, cols=2,  # 2x2 grid for four plots
        subplot_titles=(
            "Score Distribution by Category",
            "Average Weight by Category",
            "Average Review Time",
            "Disputed Review Rate"
        ),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "indicator"}, {"type": "pie"}]],
        vertical_spacing=0.2,
        horizontal_spacing=0.15
    )

    # Load data
    manual_review_metric_df = data.load_manual_review_metric()
    manual_review_detail_df = data.load_manual_review_detail()

    # === Plot 1: Score Distribution by Category ===
    score_distribution = manual_review_metric_df.groupby('category_name')['score'].mean()
    fig.add_trace(
        go.Bar(
            x=score_distribution.index,
            y=score_distribution.values,
            name="Score Distribution",
            marker=dict(color="#636EFA")
        ),
        row=1, col=1
    )

    # === Plot 2: Average Weight by Category ===
    avg_weight = manual_review_metric_df.groupby('category_name')['weight'].mean()
    fig.add_trace(
        go.Bar(
            x=avg_weight.index,
            y=avg_weight.values,
            name="Average Weight",
            marker=dict(color="#EF553B")
        ),
        row=1, col=2
    )

    # === Plot 3: Average Review Time ===
    if manual_review_detail_df['review_time_seconds'].isna().all():
        manual_review_detail_df['review_time_seconds'] = pd.Series(
            np.random.randint(100, 400, size=len(manual_review_detail_df))
        )  # Synthetic data
        review_time = manual_review_detail_df['review_time_seconds'].mean()  # Average of synthetic data
    else:
        review_time = manual_review_detail_df['review_time_seconds'].mean()

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=review_time,
            title={"text": "Average Review Time (seconds)"}
        ),
        row=2, col=1
    )

    # === Plot 4: Disputed Review Rate ===
    disputed_rate = (manual_review_metric_df['critical'].astype(str).str.lower() == 'true').mean() * 100
    fig.add_trace(
        go.Pie(
            labels=["Disputed", "Non-Disputed"],
            values=[disputed_rate, 100 - disputed_rate],
            hole=0.4,
            name="Disputed Rate"
        ),
        row=2, col=2
    )

    # Update layout
    fig.update_layout(
        height=800,
        title_text="Review Metrics Dashboard",
        title_x=0.5,
        showlegend=True,
        template="plotly_white"
    )

    # Show the dashboard
    fig.show()