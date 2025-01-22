import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from assets.data import data

def create_conversation_metrics_dashboard():
    """Create a combined dashboard with multiple metrics visualized."""
    
    # Initialize subplots layout
    fig = make_subplots(
        rows=2, cols=2,  # 2x2 grid for four plots
        subplot_titles=(
            "Average Response Time and Conversation Count",
            "Average Conversation Length",
            "Sentiment Analysis",
            "Closed vs Open Conversations"
        ),
        specs=[[{"secondary_y": True}, {"type": "bar"}],
               [{"type": "pie"}, {"type": "pie"}]],
        vertical_spacing=0.2,
        horizontal_spacing=0.15
    )
    
    # === Plot 1: Average Response Time and Conversation Count ===
    conversation_metric_df = data.load_conversation_metric()
    conversation_metric_df['first_response_time'] = pd.to_numeric(
        conversation_metric_df['first_response_time'], errors='coerce'
    )
    conversation_metric_df['conversation_date'] = pd.to_datetime(
        conversation_metric_df['created_at'], errors='coerce'
    ).dt.date
    avg_response_time_df = conversation_metric_df.groupby('conversation_date').agg(
        avg_response_time=('first_response_time', 'mean'),
        conversation_count=('conversation_id', 'count')
    ).reset_index()
    avg_response_time_df = avg_response_time_df[
        (avg_response_time_df['avg_response_time'] > 0) &
        (avg_response_time_df['avg_response_time'] < 5000)
    ]
    # Add line for average response time
    fig.add_trace(
        go.Scatter(
            x=avg_response_time_df['conversation_date'],
            y=avg_response_time_df['avg_response_time'],
            mode='lines+markers',
            name='Avg Response Time (s)',
            line=dict(color="#1f77b4")
        ),
        row=1, col=1, secondary_y=False
    )
    # Add bar for conversation count
    fig.add_trace(
        go.Bar(
            x=avg_response_time_df['conversation_date'],
            y=avg_response_time_df['conversation_count'],
            name='Conversation Count',
            marker=dict(opacity=0.7, color="#ff7f0e")
        ),
        row=1, col=1, secondary_y=True
    )

    # === Plot 2: Average Conversation Length ===
    avg_length = {
        "Public Messages": conversation_metric_df['public_message_count'].mean(),
        "Private Messages": conversation_metric_df['private_message_count'].mean(),
        "Public Characters": conversation_metric_df['public_mean_character_count'].mean(),
    }
    fig.add_trace(
        go.Bar(
            x=list(avg_length.keys()),
            y=list(avg_length.values()),
            marker=dict(color=["#2ca02c", "#d62728", "#9467bd"]),
            name="Average Length"
        ),
        row=1, col=2
    )

    # === Plot 3: Sentiment Analysis ===
    sentiment_counts = conversation_metric_df['klaus_sentiment'].value_counts(normalize=True) * 100
    fig.add_trace(
        go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.4,
            name="Sentiment"
        ),
        row=2, col=1
    )

    # === Plot 4: Closed vs Open Conversations ===
    closed_counts = conversation_metric_df['is_closed'].value_counts(normalize=True) * 100
    closed_counts.index = ["Closed", "Open"]
    fig.add_trace(
        go.Pie(
            labels=closed_counts.index,
            values=closed_counts.values,
            hole=0.4,
            name="Closed vs Open"
        ),
        row=2, col=2
    )

    # Update layout
    fig.update_layout(
        height=800,
        title_text="Customer Conversation Metrics Dashboard",
        title_x=0.5,
        showlegend=True,
        template="plotly_white"
    )

    # Update y-axis titles for dual-axis in the first plot
    fig.update_yaxes(title_text="Avg Response Time (s)", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Conversation Count", row=1, col=1, secondary_y=True)
    
    fig.show()
