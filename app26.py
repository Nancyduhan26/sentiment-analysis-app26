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

# Download stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# YouTube API key
API_KEY = "AIzaSyBbuNNk6sx7nH0E7MflQYEFJei89qAwdvw"
youtube = build("youtube", "v3", developerKey=API_KEY)

# Sidebar Navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Predict"])

# ========= HOME PAGE =========
if page == "Home":
    st.title("🏠 Welcome to YouTube Sentiment Analyzer")
    st.markdown("""
        <h4>This project helps you analyze the sentiment of YouTube comments using Natural Language Processing (NLP).</h4>
        <ul>
            <li>✅ Enter a YouTube video ID to analyze public comments</li>
            <li>✅ Or, analyze your own custom comment</li>
            <li>✅ Visualize results with sentiment bar chart</li>
        </ul>
        <p>Scroll to the 'Predict' section to try it out!</p>
    """, unsafe_allow_html=True)

# ========= ABOUT PAGE =========
elif page == "About":
    st.title("ℹ️ About This Project")
    st.markdown("""
        <h4>Project Title:</h4> <p>YouTube Comment Sentiment Analysis</p>
        <h4>Submitted to:</h4>
        <ul>
            <li><strong>Company:</strong> Solitaire Infosys</li>
            <li><strong>Class Teacher:</strong> Anchal Mittal</li>
            <li><strong>Head of Department:</strong> Dr. Arvind Kumar</li>
        </ul>
        <h4>Technologies Used:</h4>
        <ul>
            <li>Python</li>
            <li>Streamlit</li>
            <li>TextBlob</li>
            <li>YouTube Data API</li>
            <li>NLTK</li>
            <li>Pandas, Matplotlib, Seaborn</li>
        </ul>
        <p>This tool extracts comments from YouTube and determines whether they are Positive, Negative, or Neutral.</p>
    """, unsafe_allow_html=True)

# ========= PREDICT PAGE =========
elif page == "Predict":
    st.title("💬 YouTube Sentiment Analyzer")
    st.markdown("Analyze sentiment of YouTube video comments or your own comment!")

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
            part="snippet", videoId=video_id, maxResults=10
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
    def plot_sentiment_chart_as_pie(df):
        count = df["Sentiment"].value_counts()
        st.subheader("📊 Sentiment pie Chart")
        fig, ax = plt.subplots()
        # Plot the pie chart
        ax.pie(
        count.values,
        labels=count.index,
        autopct='%1.1f%%',  # Display the percentage for each slice
        startangle=90,      # Start the first slice at 90 degrees (top of the circle)
    )
    
    # Ensure the pie chart is a circle and not an ellipse
        ax.axis('equal')
    
    # Add a title
        ax.set_title('Sentiment Distribution')
    
    # Use st.pyplot to display the chart in your Streamlit app
        st.pyplot(fig)
    # YouTube Analysis
    st.header("🔗 YouTube Video Analysis")
    video_id = st.text_input("Enter YouTube Video ID")

    if st.button("Analyze YouTube Comments"):
        if video_id.strip() == "":
            st.warning("Please enter a valid video ID.")
        else:
            try:
                raw_comments = get_youtube_comments(video_id)
                df = analyze_sentiment(raw_comments)
                st.success(f"✅ Analyzed {len(df)} comments.")
                
                # Show comments with sentiment
                st.markdown("---")
                st.subheader("🧠 Analyzed Comments")
                with st.container():
                    for _, row in df.iterrows():
                        st.markdown(
                            f"""
                            <div style='background-color: #000000; padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                                <strong>Comment:</strong> {row['Original']}<br>
                                <strong>Sentiment:</strong> {row['Sentiment']}<br>
                                <strong>Polarity:</strong> {row['Polarity']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                # Show sentiment chart
                plot_sentiment_chart_as_pie(df)

            except Exception as e:
                st.error(f"❌ Error: {e}")

    # Custom comment analysis
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
