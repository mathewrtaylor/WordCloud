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
import logging
import os
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def check_nltk_resource(resource_name: str) -> None:
    """
    Checks if a specific NLTK resource is installed.
    If not, it downloads it.
    """
    try:
        nltk.data.find(f'tokenizers/{resource_name}.zip')  # Check for the zip file first
        logger.info(f"NLTK resource '{resource_name}' is installed.")
    except LookupError:
        logger.info(f"NLTK resource '{resource_name}' not found. Downloading...")
        nltk.download(resource_name)
    except Exception:
        # Sometimes the path pointer is found but not a simple zip file; handle general lookup errors
        try:
            nltk.data.find(f'tokenizers/{resource_name}')
            logger.info(f"NLTK resource '{resource_name}' is installed.")
        except LookupError:
            logger.info(f"NLTK resource '{resource_name}' not found. Downloading...")
            nltk.download(resource_name)


def collect_news_articles(feeds_yaml_path: str, today: datetime.date) -> pd.DataFrame:
    """
    Loads RSS feeds from a YAML config, scrapes article URLs, downloads and parses
    each article using newspaper3k, saves results to a date-stamped CSV, and returns
    a DataFrame.

    Args:
        feeds_yaml_path: Path to the YAML file containing the list of RSS feed URLs.
        today: Date used to timestamp the output CSV filename.

    Returns:
        DataFrame with columns: URL, Keywords, Text.
    """
    with open(feeds_yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    feeds = config['feeds']

    articles = []
    for feed in feeds:
        try:
            response = requests.get(feed, timeout=10)
            soup = BeautifulSoup(response.content, features='xml')
            for item in soup.find_all('item'):
                link = item.find('link')
                if link:
                    articles.append(link.text)
        except Exception:
            logger.warning(f"Failed to fetch feed: {feed}")

    logger.info(f"Articles pulled down: {len(articles)}")

    data = []
    for url in articles:
        info = Article(url)
        try:
            info.download()
            info.parse()
            info.nlp()
            data.append([url, info.keywords, info.text])
        except Exception:
            continue

    if not data:
        logger.warning("No article data collected.")
        return pd.DataFrame(columns=['URL', 'Keywords', 'Text'])

    df = pd.DataFrame(data, columns=['URL', 'Keywords', 'Text'])
    csv_path = f"news_articles_{today}.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"Saved {len(df)} articles to {csv_path}")
    return df


def generate_wordcloud(
    text: str,
    output_prefix: str,
    today: datetime.date,
    stopwords: set,
    figsize: tuple = (20, 20),
    mask_image: str = None,
    recolor_from_mask: bool = False,
    colormap: str = None,
    random_state: int = None,
) -> None:
    """
    Generates and saves a wordcloud PNG image.

    Args:
        text: Space-separated keywords to render in the wordcloud.
        output_prefix: Base name for the output PNG file.
        today: Date used to timestamp the output filename.
        stopwords: Set of words to exclude from the wordcloud.
        figsize: Matplotlib figure size tuple (width, height).
        mask_image: Optional filename of an image to use as a mask shape.
        recolor_from_mask: If True, recolors the wordcloud using the mask image's colors.
        colormap: Optional matplotlib colormap name (e.g. 'rainbow').
        random_state: Optional random seed for reproducible layouts.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    wc_kwargs = {
        'stopwords': stopwords,
        'collocations': False,
        'background_color': 'white',
    }

    frame = None
    if mask_image:
        mask_path = os.path.join(script_dir, mask_image)
        frame = np.array(Image.open(mask_path))
        wc_kwargs['mask'] = frame

    if colormap:
        wc_kwargs['colormap'] = colormap

    if random_state is not None:
        wc_kwargs['random_state'] = random_state

    wc = WordCloud(**wc_kwargs).generate(text)

    plt.figure(figsize=figsize)
    if recolor_from_mask and frame is not None:
        image_colors = ImageColorGenerator(frame)
        plt.imshow(wc.recolor(color_func=image_colors))
    else:
        plt.imshow(wc)

    plt.axis('off')
    output_path = os.path.join(script_dir, f"{output_prefix}_{today}.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved wordcloud to {output_path}")


def main() -> None:
    check_nltk_resource('punkt_tab')
    today = datetime.date.today()

    try:
        df = collect_news_articles(feeds_yaml_path="feeds.yaml", today=today)
    except Exception:
        logger.exception("Failed to collect news articles.")
        return

    stopwords = set(STOPWORDS)
    stopwords.update(['globalnews', 'guardian', 'abc', 'nbc', 'cbs', 'nytimes', 'state'])

    if not df.empty:
        keywords = [j for i in df.Keywords for j in i]
        text = ' '.join(keywords)

        # Unmasked wordcloud
        generate_wordcloud(text=text, output_prefix="original_wordcloud", today=today,
                           stopwords=stopwords, figsize=(20, 20))

        # US Flag mask
        generate_wordcloud(text=text, output_prefix="us_flag_wordcloud", today=today,
                           stopwords=stopwords, mask_image="Flag.jpg",
                           figsize=(30, 30), recolor_from_mask=True)

        # Tree mask
        generate_wordcloud(text=text, output_prefix="tree_wordcloud", today=today,
                           stopwords=stopwords, mask_image="Tree.jpg",
                           figsize=(20, 20), recolor_from_mask=True)

        # Modern look (comment bubble mask)
        generate_wordcloud(text=text, output_prefix="wordcloud", today=today,
                           stopwords=STOPWORDS, mask_image="comment.png",
                           figsize=(50, 50), colormap="rainbow", random_state=1)
    else:
        logger.warning("No articles collected; skipping wordcloud generation.")


if __name__ == '__main__':
    main()
