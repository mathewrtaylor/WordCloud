"""
News Aggregation, NLP Processing, and WordCloud Generation Script

This script aggregates news articles from a configurable list of RSS feeds,
downloads and parses article content, performs basic NLP keyword extraction,
and produces both archival datasets and visual wordcloud outputs.

High-level workflow:
--------------------
1. Load RSS feed URLs from a YAML configuration file
2. Parse each RSS feed to extract article URLs
3. Download and parse article content using newspaper3k
4. Extract full article text and NLP-derived keywords
5. Store results in a pandas DataFrame and export to CSV
6. Generate multiple wordcloud visualizations (optionally masked and recolored)

Configuration:
--------------
- RSS feeds are defined in an external YAML file (e.g., feeds.yaml)
- Wordcloud styles, masks, and output naming are configurable via function calls
- Output filenames are date-stamped for archival and repeatability

Outputs:
--------
- CSV file containing:
    - URL: Article source URL
    - Keywords: NLP-extracted keywords (list)
    - Text: Full parsed article text
- PNG images of wordclouds with various styles and masks

Primary dependencies:
---------------------
- requests
- PyYAML
- BeautifulSoup (bs4)
- newspaper3k
- pandas
- numpy
- Pillow (PIL)
- matplotlib
- wordcloud

Design considerations:
----------------------
- The script is tolerant of malformed feeds and broken article URLs
- Network operations include timeouts to avoid blocking execution
- Try/except blocks are intentionally used to skip unreliable sources
- Functions are written to be reusable in scripts, notebooks, or scheduled jobs

Typical use cases:
------------------
- Daily or weekly news aggregation
- Trend and keyword analysis across multiple news sources
- Generating visual summaries (wordclouds) for reporting or dashboards
- Feeding downstream NLP or OSINT analysis pipelines

Notes:
------
- This script is designed for batch execution, not real-time processing
- Newspaper3k parsing accuracy depends on site structure and may vary
- Some sources may block scraping or return incomplete content
"""

import datetime
import matplotlib.pyplot as plt
import numpy as np
import nltk
import pandas as pd
import requests
import yaml
from bs4 import BeautifulSoup
from newspaper import Article
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def check_nltk_resource(resource_name):
    """
    Checks if a specific NLTK resource is installed.
    If not, it downloads it.
    """
    try:
        nltk.data.find(f'tokenizers/{resource_name}.zip') # Check for the zip file first
        print(f"NLTK resource '{resource_name}' is installed.")
    except LookupError:
        print(f"NLTK resource '{resource_name}' not found. Downloading...")
        nltk.download(resource_name)
    except Exception as e:
        # Sometimes the path pointer is found but not a simple zip file, this handles general import errors
        try:
            nltk.data.find(f'tokenizers/{resource_name}')
            print(f"NLTK resource '{resource_name}' is installed.")
        except LookupError:
            print(f"NLTK resource '{resource_name}' not found. Downloading...")
            nltk.download(resource_name)


def main():
    # Download the tokenizer
    check_nltk_resource('punkt_tab')

    # Setting date for file outputs
    today = datetime.date.today()

    # Grabbing the data
    df = collect_news_articles(feeds_yaml_path="feeds.yaml",today=today)

    # Though there is a set of default stop words (stuff to not be included), sometimes you want to add
    stopwords = set(STOPWORDS)
    stopwords.update(['globalnews','guardian','abc','nbc','cbs','nytimes','globalnews','state'])

    # Generating Wordcloud
    if not df.empty:
        keywords = [j for i in df.Keywords for j in i]
        text = ' '.join(i for i in keywords)

        # Time to generate some WordClouds!
        # Unmasked Wordcloud
        generate_wordcloud(text=text,output_prefix="original_wordcloud",today=today,stopwords=stopwords,figsize=(20, 20))

        # US Flag Mask
        generate_wordcloud(text=text,output_prefix="us_flag_wordcloud",today=today,stopwords=stopwords,mask_image="Flag.jpg",
                           figsize=(30, 30),recolor_from_mask=True)
        
        # Tree Mask
        generate_wordcloud(text=text,output_prefix="tree_wordcloud",today=today,stopwords=stopwords,mask_image="Tree.jpg",
                           figsize=(20, 20),recolor_from_mask=True)
        
        # Modern Look Mask
        generate_wordcloud(text=text,output_prefix="wordcloud",today=today,stopwords=STOPWORDS,mask_image="comment.png",
                           figsize=(50, 50),colormap="rainbow",random_state=1)
    else:
        print("No articles collected to generate word clouds.")

if __name__ == '__main__':
    main()