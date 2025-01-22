import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from assets.data import data

def create_customer_satisfaction_dashboard():
    """Create a dashboard visualizing customer satisfaction metrics."""

    # Load datasets
    manual_review_metric_df = data.load_manual_review_metric()
    conversation_metric_df = data.load_conversation_metric()
    conversation_detail_df = data.load_conversation_detail()

    # === Data Preparation ===
    # Sentiment Distribution (Correlation with Review Scores)
    sentiment_scores = (
        conversation_metric_df.groupby('klaus_sentiment')
        .agg(avg_public_messages=('public_message_count', 'mean'))
        .reset_index()
    )
    review_scores = (
        manual_review_metric_df.groupby('review_id')
        .agg(avg_score=('score', 'mean'))
        .reset_index()
    )
    sentiment_correlation = pd.merge(
        sentiment_scores, review_scores, how="inner", left_index=True, right_index=True
    )

    # Resolution Rates by Channel
    resolution_rates = (
        conversation_detail_df.groupby('channel')
        .agg(resolved=('external_ticket_id', 'count'))
        .reset_index()
    )

    # Average Resolution Time
    resolution_times = conversation_metric_df['full_resolution_time_seconds'].mean()

    # Resolution Efficiency by Channel
    resolution_efficiency = (
        conversation_detail_df.groupby('channel')
        .agg(resolution_time=('external_ticket_id', 'count'))  # Placeholder
        .reset_index()
    )

    # === Create Subplots ===
    fig = make_subplots(
        rows=2, cols=2,  # 2x2 grid
        subplot_titles=(
            "Sentiment Correlation with Review Scores",
            "Resolution Rates by Channel",
            "Average Resolution Time",
            "Resolution Efficiency by Channel"
        ),
        specs=[[{"secondary_y": False}, {"type": "bar"}],
               [{"type": "indicator"}, {"type": "pie"}]],
        vertical_spacing=0.2,
        horizontal_spacing=0.15
    )

    # === Plot 1: Sentiment Correlation with Review Scores ===
    fig.add_trace(
        go.Scatter(
            x=sentiment_correlation['klaus_sentiment'],
            y=sentiment_correlation['avg_score'],
            mode='lines+markers',
            name="Sentiment Correlation",
            line=dict(color="#636EFA")
        ),
        row=1, col=1
    )

    # === Plot 2: Resolution Rates by Channel ===
    fig.add_trace(
        go.Bar(
            x=resolution_rates['channel'],
            y=resolution_rates['resolved'],
            name="Resolution Rates",
            marker=dict(color="#EF553B")
        ),
        row=1, col=2
    )

    # === Plot 3: Average Resolution Time ===
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=resolution_times,
            title={"text": "Avg Resolution Time (seconds)"}
        ),
        row=2, col=1
    )

    # === Plot 4: Resolution Efficiency by Channel ===
    fig.add_trace(
        go.Pie(
            labels=resolution_efficiency['channel'],
            values=resolution_efficiency['resolution_time'],
            hole=0.4,
            name="Resolution Efficiency"
        ),
        row=2, col=2
    )

    # === Update Layout ===
    fig.update_layout(
        height=800,
        title_text="Customer Satisfaction Dashboard",
        title_x=0.5,
        showlegend=True,
        template="plotly_white"
    )

    fig.show()
