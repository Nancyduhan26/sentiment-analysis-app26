No# app.py
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
video_id = st.text_input("Enter YouTube Video ID (e.g., RxmaWPGGJH4):")

if st.button("Analyze YouTube Comments"):
    if video_id.strip() == "":
        st.warning("Please enter a valid ID.")
    else:
        try:
            raw_comments = get_youtube_comments(video_id)
            df = analyze_sentiment(raw_comments)
            st.success(f"✅ Analyzed {len(df)} comments.")
            st.dataframe(df)
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
        st.write(f"**Polarity:** `{polarity}`")
        st.success(f"Sentiment: **{sentiment}**")
tepad++ v8.8.3 vulnerability-fixes & new enhancement:

 1. Use self-signed certificate to sign new release binaries.
 2. Fix uninstaller security issue (CVE-2025-49144).
 3. Enhance security for DLL loading.


Notepad++ v8.8.2 regression-fixes, bug-fixes & new features:

 1. Fix regression of folding state not being remembered through sessions.
 2. Fix "Go To Settings" links in Style Configurator regression (from v8.8).
 3. Fix small regression of tab background (hovered) highlighting issue after drag&drop.
 4. Fix an unresponsive (hang) issue due to hide lines.
 5. Fix installer security issue by using absolute path instead of unspecified path (CVE-2025-49144).
 6. Installer component "WinGUp": update cURL to 8.13.0 for fixing cURL's security issue CVE-2025-0167.
 7. Update to scintilla 5.5.7 & Lexilla 5.4.5.
 8. Add feature to update Notepad++ on exit.
 9. Add `/relaunchNppAfterSilentInstall` command argument for installer.
10. Add feature to set read-only attribute on file so user can toggle (set/remove) read-only attribute of a file.
11. Add new plugin API: NPPM_GETTOOLBARICONSETMODE & NPPN_TOOLBARICONSETCHANGED to get toolbar icon set choice.
12. Deprecate 3 APIs: Deprecate NPPM_GETOPENFILENAMES, NPPM_GETOPENFILENAMESPRIMARY & NPPM_GETOPENFILENAMESSECOND.
13. Add new feature of using first line of untitled document for its tab name.
14. Enhance NPPM_DARKMODESUBCLASSANDTHEME: Enable darkmode progress bar for plugins.
15. Various dark mode enhancements.
16. Fix right click on caption bar unhidding main menu.
17. Fix rename tab error message when tab name is unchanged.
18. Fix Python FunctionList absorbing next function issue if space after colon.
19. Remove .log from errorlist lexer's default extensions.
20. Make raw string syntax highlighting work for Golang.
21. Fix Notepad++ tray icon lost after Windows Taskbar crashing & being relaunched.
22. Fix changing toolbar icon set not updating to matching panel icon set.
23. Fix Windows dialog file list not react with keystroke (character match).
24. Add "*" mark on modified file entries in "Windows" dropdown menu.


Get more info on
https://notepad-plus-plus.org/downloads/v8.8.3/


Included plugins:

1.  NppExport v0.4
2.  Converter v4.6
3.  Mime Tool v3.1


Updater (Installer only):

* WinGUp (for Notepad++) v5.3.3
