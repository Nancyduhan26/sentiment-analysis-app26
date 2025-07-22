# app.py
# app.py
import streamlit as st
import pandas as pd
import re
from textblob import TextBlob
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# YouTube API key (self-made, hidden from ngrok now!)
API_KEY = "YOUR_API_KEY_HERE"
youtube = build("youtube", "v3", developerKey=API_KEY)

# ====== Styling ======
st.set_page_config(page_title="YouTube Sentiment Analyzer 🎥", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #fdf6f0; padding: 20px; border-radius: 10px; }
        h1, h2, h3 { color: #2b2d42; }
        .stButton>button {
            background-color: #4caf50;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
        .stTextInput>div>input, .stTextArea>div>textarea {
            background-color: #fff;
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# ====== Helper Functions ======

def clean_comment(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower()
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

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

def plot_sentiment_chart(df):
    count = df["Sentiment"].value_counts()
    st.subheader("📊 Sentiment Distribution")
    fig, ax = plt.subplots()
    sns.barplot(x=count.index, y=count.values, palette="pastel", ax=ax)
    ax.set_ylabel("No. of Comments")
    ax.set_xlabel("Sentiment")
    st.pyplot(fig)

# ====== UI Starts ======
st.markdown('<div class="main">', unsafe_allow_html=True)

st.title("💬 YouTube Sentiment Analyzer")
st.markdown("Get a quick look into how people feel about a video — or test your own comment!")

# ========== YouTube Comments Section ==========
st.header("🔗 Analyze YouTube Video Comments")
video_id = st.text_input("Enter YouTube Video ID (e.g. RxmaWPGGJH4)")

if st.button("🎥 Analyze Comments"):
    if video_id.strip() == "":
        st.warning("Please enter a valid YouTube video ID.")
    else:
        try:
            raw_comments = get_youtube_comments(video_id)
            df = analyze_sentiment(raw_comments)
            st.success(f"✅ Analyzed {len(df)} comments!")
            st.dataframe(df)
            plot_sentiment_chart(df)
        except Exception as e:
            st.error(f"❌ Failed to fetch comments: {e}")

# ========== Personal Comment Section ==========
st.markdown("---")
st.header("📝 Analyze Your Own Comment")

custom_comment = st.text_area("Type your comment below 👇")

if st.button("💡 Analyze My Comment"):
    if custom_comment.strip() == "":
        st.warning("Type a comment before analyzing.")
    else:
        cleaned = clean_comment(custom_comment)
        blob = TextBlob(cleaned)
        polarity = blob.sentiment.polarity
        sentiment = "Positive 😊" if polarity > 0 else "Negative 😞" if polarity < 0 else "Neutral 😐"

        st.markdown(f"""
        **🧼 Cleaned Comment:** `{cleaned}`  
        **📈 Polarity Score:** `{polarity}`  
        **🔍 Sentiment:** **{sentiment}**
        """)

# ====== Close UI Styling ======
st.markdown('</div>', unsafe_allow_html=True)
