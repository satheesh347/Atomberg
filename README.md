# Atomberg
This file explains the project's purpose, how to set it up (including creating a `requirements.txt` file for easy installation), how to configure it, and what to expect as output.

---

# YouTube & Google Search Brand Analysis

This Python script performs a competitive analysis by scraping search results for a specific query from both YouTube and Google Search. It calculates the "Share of Voice" (SoV) for a predefined list of brands, analyzes the sentiment of the search results, and generates clear visualizations to present the findings.

## Features

-   Fetches top video results from YouTube based on a search query.
-   Fetches top organic search results from Google using the SerpApi service.
-   Analyzes content (titles, descriptions, snippets) for mentions of specific brands.
-   Calculates the Share of Voice (SoV) for each brand across both platforms combined and individually.
-   Performs basic sentiment analysis (Positive, Negative, Neutral) on the content.
-   Generates and saves visualizations as `.png` files:
    -   Pie charts for Share of Voice.
    -   A bar chart for sentiment distribution.

## Example Output

<p align="center">
  <img src="combined_sov.png" width="48%" alt="Combined SoV">
  <img src="youtube_sov.png" width="48%" alt="YouTube SoV">
</p>
<p align="center">
  <img src="google_sov.png" width="48%" alt="Google SoV">
  <img src="sentiment_distribution.png" width="48%" alt="Sentiment Distribution">
</p>

---

## Setup and Installation

Follow these steps to set up your environment and run the script.

### 1. Prerequisites

-   Python 3.6+
-   A YouTube Data API v3 Key
-   A SerpApi Key

### 2. Project Setup

**a. Clone or Download**

First, get the project files onto your local machine. If you are using git, you can clone the repository. Otherwise, simply download the script.

**b. Create a `requirements.txt` file**

In the same directory as your Python script, create a file named `requirements.txt` and paste the following content into it. This file lists all the necessary Python packages.

```txt
google-api-python-client
textblob
pandas
matplotlib
serpapi-python
```

**c. Create a Virtual Environment (Recommended)**

It is highly recommended to use a virtual environment to keep project dependencies isolated.

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

With your virtual environment activated, run the following command to install all the required packages from your `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

You need to add your personal API keys to the script.

**a. Get Your Keys:**

-   **YouTube API Key**:
    1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
    2.  Create a new project.
    3.  Enable the **YouTube Data API v3**.
    4.  Go to "Credentials", click "Create Credentials", and choose "API key".
    5.  Copy the generated key.
-   **SerpApi Key**:
    1.  Sign up for a free account at [SerpApi](https://serpapi.com/).
    2.  Go to your dashboard to find your API key.

**b. Add Keys to the Script:**

Open the Python script and replace the placeholder keys with your own.

```python
# ...

YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"
print("Using API key:", YOUTUBE_API_KEY)

# ...

# ========== CONFIG ==========
SERPAPI_KEY = "YOUR_SERPAPI_KEY_HERE"

# ...
```

---

## How to Run

### 1. Customize the Search

Before running, you can change the configuration variables at the top of the script to match your analysis needs.

```python
# ========== CONFIG ==========
SERPAPI_KEY = "YOUR_SERPAPI_KEY_HERE"
SEARCH_QUERY = "smart fan"
BRANDS = ["Atomberg", "Orient", "Crompton", "Havells","LG","Usha","Bajaj","V-Guard"]
N_RESULTS = 50  # top N results to analyze
```

### 2. Execute the Script

Once the dependencies are installed and the keys are configured, simply run the Python script from your terminal:

```bash
python your_script_name.py
```

The script will print its progress to the console and, upon completion, you will find four new image files in the same directory:

-   `combined_sov.png`
-   `youtube_sov.png`
-   `google_sov.png`
-   `sentiment_distribution.png`
