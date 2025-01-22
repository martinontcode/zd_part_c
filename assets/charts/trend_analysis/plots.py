import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from assets.data import data

def create_trend_analysis_dashboard():
    """Create a dashboard visualizing trend analysis metrics."""
    
    # Load datasets
    conversation_metric_df = data.load_conversation_metric()
    conversation_detail_df = data.load_conversation_detail()

    # === Data Preparation ===
    # Sentiment Over Time
    conversation_metric_df['created_at_date'] = pd.to_datetime(conversation_metric_df['created_at']).dt.date
    sentiment_trends = (
        conversation_metric_df.groupby(['created_at_date', 'klaus_sentiment'])
        .size()
        .unstack(fill_value=0)
    )

    # Resolution Time Trends
    resolution_time_trends = (
        conversation_metric_df.groupby('created_at_date')['full_resolution_time_seconds']
        .mean()
        .dropna()
    )

    # Volume Trends by Channel
    conversation_detail_df['updated_at_date'] = pd.to_datetime(conversation_detail_df['updated_at']).dt.date
    volume_trends = (
        conversation_detail_df.groupby(['updated_at_date', 'channel'])
        .size()
        .unstack(fill_value=0)
    )

    # === Create Subplots ===
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Sentiment Trends Over Time",
            "Resolution Time Trends",
            "Conversation Volume by Channel",
            "Channel Performance Distribution"
        ),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"type": "bar"}, {"type": "pie"}]],
        vertical_spacing=0.2,
        horizontal_spacing=0.15
    )

    # === Plot 1: Sentiment Trends Over Time ===
    for sentiment in sentiment_trends.columns:
        fig.add_trace(
            go.Scatter(
                x=sentiment_trends.index,
                y=sentiment_trends[sentiment],
                mode='lines+markers',
                name=f"Sentiment: {sentiment}"
            ),
            row=1, col=1
        )

    # === Plot 2: Resolution Time Trends ===
    fig.add_trace(
        go.Scatter(
            x=resolution_time_trends.index,
            y=resolution_time_trends.values,
            mode='lines+markers',
            name="Resolution Time",
            line=dict(color="#EF553B")
        ),
        row=1, col=2
    )

    # === Plot 3: Volume Trends by Channel ===
    for channel in volume_trends.columns:
        fig.add_trace(
            go.Bar(
                x=volume_trends.index,
                y=volume_trends[channel],
                name=f"Channel: {channel}"
            ),
            row=2, col=1
        )

    # === Plot 4: Channel Performance Distribution ===
    total_volumes = volume_trends.sum()
    fig.add_trace(
        go.Pie(
            labels=total_volumes.index,
            values=total_volumes.values,
            hole=0.4,
            name="Channel Distribution"
        ),
        row=2, col=2
    )

    # === Update Layout ===
    fig.update_layout(
        height=800,
        title_text="Trend Analysis Dashboard",
        title_x=0.5,
        showlegend=True,
        template="plotly_white"
    )

    fig.show()
