# app.py
pip install streamlit textblob google-api-python-client matplotlib seaborn nltk
import streamlit as st
import pandas as pd
import re
from textblob import TextBlob
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords

# ============================
# ✅ Add Background Image CSS
# ============================
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/7/75/YouTube_social_white_square_(2017).svg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# YouTube API key
API_KEY = "AIzaSyBbuNNk6sx7nH0E7MflQYEFJei89qAwdvw"
youtube = build("youtube", "v3", developerKey=API_KEY)

# Function to clean text
def clean_comment(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower()
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

# Function to fetch comments
def get_youtube_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet", videoId=video_id, maxResults=100
    )
    response = request.execute()
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)
    return comments

# Sentiment analyzer
def analyze_sentiment(comments):
    results = []
    for comment in comments:
        cleaned = clean_comment(comment)
        blob = TextBlob(cleaned)
        polarity = blob.sentiment.polarity
        sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
        results.append({
            "Original": comment,
            "Cleaned": cleaned,
            "Polarity": polarity,
            "Sentiment": sentiment
        })
    return pd.DataFrame(results)

# Plot chart
def plot_sentiment_chart(df):
    count = df["Sentiment"].value_counts()
    st.subheader("📊 Sentiment Chart")
    fig, ax = plt.subplots()
    sns.barplot(x=count.index, y=count.values, palette="coolwarm", ax=ax)
    ax.set_ylabel("Number of Comments")
    ax.set_xlabel("Sentiment")
    st.pyplot(fig)

# ========== UI ==========

st.title("💬 YouTube Sentiment Analyzer")
st.markdown("Analyze sentiment of YouTube video comments or your own comment!")

# Section 1: YouTube comments
st.header("🔗 YouTube Video Analysis")
video_id = st.text_input("RxmaWPGGJH4")

if st.button("Analyze YouTube Comments"):
    if video_id.strip() == "":
        st.warning("Please enter a valid ID.")
    else:
        try:
            raw_comments = get_youtube_comments(video_id)
            df = analyze_sentiment(raw_comments)
            st.success(f"✅ Analyzed {len(df)} comments.")
            
            # ✅ Separated and styled comment section
            st.markdown("---")
            st.subheader("🧠 Analyzed Comments")
            with st.container():
                for _, row in df.iterrows():
                    st.markdown(
                        f"""
                        <div style='background-color: rgba(255, 255, 255, 0.85); 
                                    padding: 15px; 
                                    border-radius: 10px; 
                                    margin-bottom: 10px;'>
                            <strong>Comment:</strong> {row['Original']}<br>
                            <strong>Sentiment:</strong> {row['Sentiment']}<br>
                            <strong>Polarity:</strong> {row['Polarity']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Show chart
            plot_sentiment_chart(df)

        except Exception as e:
            st.error(f"❌ Error: {e}")

# Section 2: Single comment
st.markdown("---")
st.header("📝 Analyze Your Own Comment")

custom_comment = st.text_area("Enter a comment to analyze:")

if st.button("Analyze My Comment"):
    if custom_comment.strip() == "":
        st.warning("Please type something.")
    else:
        blob = TextBlob(custom_comment)
        polarity = blob.sentiment.polarity
        sentiment = "Positive 😊" if polarity > 0 else "Negative 😞" if polarity < 0 else "Neutral 😐"
        st.write(f"**Polarity:** {polarity}")
        st.success(f"Sentiment: **{sentiment}**")
