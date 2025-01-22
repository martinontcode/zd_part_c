import pandas as pd

def load_autoqa_review_metric() -> pd.DataFrame:
    """Load and process the AutoQA review metric data."""
    df = pd.read_json("assets\\data\\autoqa_review_metric_cleaned.json")

    numeric_fields = ["team_id", "rating_scale_score", "score"]
    df[numeric_fields] = df[numeric_fields].apply(pd.to_numeric, errors="coerce")

    datetime_fields = ["created_at", "updated_at"]
    df[datetime_fields] = df[datetime_fields].apply(pd.to_datetime, errors="coerce", utc=True)
    
    return df

def load_conversation_detail() -> pd.DataFrame:
    """Load and process the conversation detail data."""
    df = pd.read_json("assets\\data\\conversation_detail_cleaned.json")
    numeric_fields = ["external_ticket_id", "assignee_id", "payment_id", "payment_token_id"]
    df[numeric_fields] = df[numeric_fields].apply(pd.to_numeric, errors="coerce")

    datetime_fields = ["last_reply_at", "updated_at", "deleted_at"]
    df[datetime_fields] = df[datetime_fields].apply(pd.to_datetime, errors="coerce", utc=True)
    
    return df

def load_conversation_metric() -> pd.DataFrame:
    """Load and process the conversation metric data."""
    df = pd.read_json("assets\\data\\conversation_metric_cleaned.json")
    numeric_fields = [
        "unique_public_agent_count",
        "agent_most_public_messages",
        "message_count",
        "private_message_count",
        "public_message_count",
        "public_mean_character_count",
        "public_mean_word_count",
        "first_response_time",
        "first_resolution_time_seconds",
        "full_resolution_time_seconds",
    ]
    df[numeric_fields] = df[numeric_fields].apply(pd.to_numeric, errors="coerce")

    datetime_fields = ["created_at", "closed_at"]
    df[datetime_fields] = df[datetime_fields].apply(pd.to_datetime, errors="coerce", utc=True)

    df["is_closed"] = df["is_closed"].map({"true": True, "false": False})
    
    return df

def load_manual_review_detail() -> pd.DataFrame:
    """Load and process the manual review detail data."""
    df = pd.read_json("assets\\data\\manual_review_detail_cleaned.json")
    numeric_fields = ["review_id", "team_id", "comment_id", "updated_by", "review_time_seconds"]
    df[numeric_fields] = df[numeric_fields].apply(pd.to_numeric, errors="coerce")

    datetime_fields = ["created", "updated_at", "imported_at"]
    df[datetime_fields] = df[datetime_fields].apply(pd.to_datetime, errors="coerce", utc=True)

    boolean_fields = ["assignment_review", "seen", "disputed"]
    for field in boolean_fields:
        df[field] = df[field].astype(str).str.lower() == "true"
    
    return df

def load_manual_review_metric() -> pd.DataFrame:
    """Load and process the manual review metric data."""
    df = pd.read_json("assets\\data\\manual_review_metric_cleaned.json")
    numeric_fields = [
        "review_id",
        "category_id",
        "rating",
        "rating_max",
        "weight",
        "score",
        "reviewer_id",
        "reviewee_id",
    ]
    df[numeric_fields] = df[numeric_fields].apply(pd.to_numeric, errors="coerce")

    boolean_fields = ["critical"]
    for field in boolean_fields:
        df[field] = df[field].astype(str).str.lower() == "true"
    
    return df

def load_all_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load and process all data files."""
    autoqa_review_metric_df = load_autoqa_review_metric()
    conversation_detail_df = load_conversation_detail()
    conversation_metric_df = load_conversation_metric()
    manual_review_detail_df = load_manual_review_detail()
    manual_review_metric_df = load_manual_review_metric()

    return (
        autoqa_review_metric_df,
        conversation_detail_df,
        conversation_metric_df,
        manual_review_detail_df,
        manual_review_metric_df,
    )
