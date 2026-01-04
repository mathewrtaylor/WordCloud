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
    If not, it prompts the user to download it.
    """
    try:
        nltk.data.find(f'tokenizers/{resource_name}.zip') # Check for the zip file first
        print(f"'{resource_name}' is installed.")
    except LookupError:
        nltk.download('resource_name')
    except Exception as e:
        # Sometimes the path pointer is found but not a simple zip file, this handles general import errors
        try:
            nltk.data.find(f'tokenizers/{resource_name}')
            print(f"'{resource_name}' is installed.")
        except LookupError:
             nltk.download('resource_name')


def collect_news_articles(feeds_yaml_path,today,output_csv=True,timeout=15):
    """
    Collect articles from RSS feeds, download and parse article content,
    and return the results as a pandas DataFrame.

    The function:
    1. Loads RSS feed URLs from a YAML file
    2. Extracts article links from each RSS feed
    3. Downloads and parses each article using newspaper3k
    4. Extracts article text and keywords
    5. Optionally saves the results to a dated CSV file

    Parameters
    ----------
    feeds_yaml_path : str
        Path to YAML file containing RSS feeds under the key 'feeds'
    today : datetime.date or datetime.datetime
        Date used for output CSV naming
    output_csv : bool, optional
        Whether to save the resulting DataFrame to CSV (default: True)
    timeout : int, optional
        Timeout (seconds) for HTTP requests to RSS feeds (default: 15)

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns: ['URL', 'Keywords', 'Text']
    """

    articles = []

    # Load RSS feeds from YAML
    with open(feeds_yaml_path, "r") as f:
        feed_file = yaml.safe_load(f)

    # Parse RSS feeds and extract article URLs
    for feed in feed_file.get("feeds", []):
        try:
            response = requests.get(feed, timeout=timeout)
            soup = BeautifulSoup(response.content, features="xml")

            items = soup.find_all("item")
            for item in items:
                link_tag = item.find("link")
                if link_tag and link_tag.text:
                    articles.append(link_tag.text)

        except Exception:
            # Skip feeds that fail to load or parse
            continue

    data = []

    # Download and parse each article
    for url in articles:
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            data.append([
                url,
                article.keywords,
                article.text
            ])

        except Exception:
            # Some URLs are malformed, blocked, or unsupported
            continue

    # Create DataFrame
    df = pd.DataFrame(data, columns=["URL", "Keywords", "Text"])

    # Optionally save CSV for archival
    if output_csv:
        filename = f'{today.strftime("%m_%d_%y")}_news.csv'
        df.to_csv(filename, index=False)

    return df

def generate_wordcloud(text,output_prefix,today,stopwords=STOPWORDS,mask_image=None,figsize=(20, 20),background_color="white",colormap=None,
    recolor_from_mask=False,random_state=None):
    """
    Generate and save a wordcloud image.

    Parameters
    ----------
    text : str
        Text used to generate the wordcloud
    output_prefix : str
        Filename prefix (without date or extension)
    today : datetime.date or datetime.datetime
        Date used for output filename
    stopwords : set
        Stopwords to exclude
    mask_image : str or None
        Path to mask image (e.g., 'Flag.jpg'), or None
    figsize : tuple
        Matplotlib figure size
    background_color : str
        Background color for wordcloud
    colormap : str or None
        Matplotlib colormap name
    recolor_from_mask : bool
        If True, recolor wordcloud using mask image colors
    random_state : int or None
        Random seed for reproducibility
    """

    mask = None
    image_colors = None

    # If using an input image for a mask
    if mask_image:
        mask = np.array(Image.open(mask_image))
        if recolor_from_mask:
            image_colors = ImageColorGenerator(mask)

    # Generating the WordCloud
    wordcloud = WordCloud(stopwords=stopwords,collocations=False,background_color=background_color,mask=mask,colormap=colormap,
                          random_state=random_state,).generate(text)
    if image_colors:
        wordcloud = wordcloud.recolor(color_func=image_colors)
    plt.figure(figsize=figsize)
    plt.imshow(wordcloud)
    plt.axis("off")

    # Saving the file to the working directory
    filename = f"{output_prefix}_{today.strftime('%m_%d_%y')}.png"
    plt.savefig(filename, bbox_inches="tight")
    plt.close()

if __name__ == '__main__':
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