print("Running file")

YOUTUBE_API_KEY = "AIzaSyA2edYXczcyXe_ob5z46V53AHZomDHwmZI"
print("Using API key:", YOUTUBE_API_KEY)

# Install dependencies first:
# pip install google-api-python-client textblob pandas matplotlib serpapi

from googleapiclient.discovery import build
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
from serpapi import GoogleSearch

# ========== CONFIG ==========
SERPAPI_KEY = "2ae642aec5b933096dba8b38bbd2b0edd1b22f7fd529762d2b0f430fffe67cee"
SEARCH_QUERY = "smart fan"
BRANDS = ["Atomberg", "Orient", "Crompton", "Havells","LG","Usha","Bajaj","V-Guard"]
N_RESULTS = 50  # top N results to analyze

# ========== YOUTUBE ==========
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

yt_search = youtube.search().list(
    q=SEARCH_QUERY,
    part='snippet',
    type='video',
    maxResults=N_RESULTS
).execute()

yt_data = []
for item in yt_search['items']:
    video_id = item['id']['videoId']
    title = item['snippet']['title']
    description = item['snippet']['description']

    stats = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()

    views = int(stats['items'][0]['statistics'].get('viewCount', 0))
    likes = int(stats['items'][0]['statistics'].get('likeCount', 0))
    comments = int(stats['items'][0]['statistics'].get('commentCount', 0))

    mentions = {brand: 0 for brand in BRANDS}
    for brand in BRANDS:
        if brand.lower() in (title + description).lower():
            mentions[brand] += 1

    polarity = TextBlob(title + " " + description).sentiment.polarity
    sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"

    yt_data.append({
        "Platform": "YouTube",
        "Title": title,
        "URL": f"https://www.youtube.com/watch?v={video_id}",
        "Views": views,
        "Likes": likes,
        "Comments": comments,
        "Mentions": mentions,
        "Sentiment": sentiment
    })

# ========== GOOGLE SEARCH ==========
params = {
    "q": SEARCH_QUERY,
    "api_key": SERPAPI_KEY,
    "num": N_RESULTS
}
search = GoogleSearch(params)
results = search.get_dict()

google_data = []
for res in results.get("organic_results", []):
    title = res.get("title", "")
    snippet = res.get("snippet", "")
    link = res.get("link", "")

    mentions = {brand: 0 for brand in BRANDS}
    for brand in BRANDS:
        if brand.lower() in (title + snippet).lower():
            mentions[brand] += 1

    polarity = TextBlob(title + " " + snippet).sentiment.polarity
    sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"

    google_data.append({
        "Platform": "Google",
        "Title": title,
        "URL": link,
        "Views": None,
        "Likes": None,
        "Comments": None,
        "Mentions": mentions,
        "Sentiment": sentiment
    })

# ========== COMBINE DATA ==========
all_data = yt_data + google_data
df = pd.DataFrame(all_data)

# Flatten mentions for analysis
for brand in BRANDS:
    df[brand + " Mentions"] = df["Mentions"].apply(lambda x: x[brand])
df.drop(columns=["Mentions"], inplace=True)

# SoV calculation
total_mentions = {brand: df[brand + " Mentions"].sum() for brand in BRANDS}
total_mentions_df = pd.DataFrame(list(total_mentions.items()), columns=["Brand", "Mentions"])
total_mentions_df["SoV %"] = (total_mentions_df["Mentions"] / total_mentions_df["Mentions"].sum()) * 100

# ========== PLOTS ==========
# ========== PLOTS ==========

# Improved function to create neat pie charts with legend and less clutter
# Improved function to create neat pie charts with legend and less clutter
def create_pie_chart(df_source, title, filename):
    total_mentions = {brand: df_source[brand + " Mentions"].sum() for brand in BRANDS}
    total_mentions_df = pd.DataFrame(list(total_mentions.items()), columns=["Brand", "Mentions"])
    
    # Filter out brands with zero mentions to avoid clutter
    total_mentions_df = total_mentions_df[total_mentions_df["Mentions"] > 0]
    
    if total_mentions_df.empty:
        print(f"No mentions data to plot for {title}")
        return
    
    total_mentions_df["SoV %"] = (total_mentions_df["Mentions"] / total_mentions_df["Mentions"].sum()) * 100

    plt.figure(figsize=(7,7))
    wedges, texts, autotexts = plt.pie(
        total_mentions_df["SoV %"],
        labels=None,  # Hide labels on slices for clarity
        autopct='%1.1f%%',
        startangle=140,
        pctdistance=0.85,
        wedgeprops=dict(width=0.5, edgecolor='w')
    )
    
    # Create legend with brand name and counts outside the pie chart
    labels = [f"{b}: {m}" for b, m in zip(total_mentions_df["Brand"], total_mentions_df["Mentions"])]
    plt.legend(wedges, labels, title="Brands", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()


# Combined Google + YouTube SoV pie chart
create_pie_chart(df, f"Share of Voice for '{SEARCH_QUERY}' (Google + YouTube)", "combined_sov.png")

# YouTube only SoV pie chart
df_youtube = df[df["Platform"] == "YouTube"]
create_pie_chart(df_youtube, f"Share of Voice for '{SEARCH_QUERY}' (YouTube Only)", "youtube_sov.png")

# Google only SoV pie chart
df_google = df[df["Platform"] == "Google"]
create_pie_chart(df_google, f"Share of Voice for '{SEARCH_QUERY}' (Google Only)", "google_sov.png")


# Sentiment distribution bar plot (unchanged, but you can add tight_layout)
sentiment_counts = df["Sentiment"].value_counts()
sentiment_counts.plot(kind="bar", color=["green", "red", "gray"])
plt.title("Sentiment Distribution Across Platforms")
plt.tight_layout()
plt.savefig("sentiment_distribution.png", dpi=300, bbox_inches='tight')
plt.show()




