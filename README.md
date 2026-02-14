# WordCloud

A news aggregation and visualization project that uses web scraping, natural language processing (NLP), and matplotlib to generate insightful word clouds from current news articles. This project offers two independent tools, a Python script and a Jupyter Notebook, each fully capable of executing the core functionality.

The project supports:

- RSS-based news ingestion
- Article parsing and keyword extraction via NLP
- Archival datasets (CSV)
- Multiple wordcloud visual styles, including image masks and recoloring

---

## Features

- Aggregate articles from multiple configurable RSS feeds
- Robust parsing with graceful handling of malformed or blocked sources
- NLP keyword extraction using newspaper3k
- CSV export for analysis and archival
- Wordcloud generation with:
    - Custom masks (e.g., flags, shapes)
    - Image-based recoloring
    - Multiple styles and layouts
- YAML-based configuration for feed management

---

## Installation

This project can be set up using a Python virtual environment and `pip`.

Open a terminal and navigate to your desired project directory, then clone the repository:

```bash
git clone https://github.com/mathewrtaylor/WordCloud.git
cd WordCloud
```

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

To run the Jupyter Notebook, ensure Jupyter Lab is installed within your virtual environment:

```bash
pip install jupyterlab
jupyter lab
```

---

## Usage
### Jupyter Notebook

1.  Launch Jupyter Lab from your activated virtual environment (`jupyter lab`).
2.  Open the `Word Cloud.ipynb` notebook in the project directory.
3.  Run cells top-to-bottom. The notebook handles its own NLTK data download within its cells. This will:
    -   Load RSS feeds
    -   Download and parse articles
    -   Generate datasets
    -   Render wordclouds

This is the best way to explore and tweak visual styles interactively.

---

### Python Script (Automated / Repeatable)



The `word_cloud.py` script provides the core functionality for news aggregation and word cloud generation. It is designed for command-line execution and automated runs.



**Key features:**

-   Encapsulated logic within functions for clarity.

-   Main execution logic runs when the script is executed directly (`if __name__ == '__main__': main()`).

-   Automatically checks for and downloads the necessary NLTK 'punkt_tab' resource if not found, eliminating manual intervention.



**Example execution:**



```bash

python word_cloud.py

```



Script execution:



-   Loads RSS feeds from `feeds.yaml`

-   Downloads and parses articles

-   Exports a date-stamped CSV file

-   Generates multiple wordcloud images based on the configuration within the script.



This mode is ideal for:



-   Scheduled runs (cron, Task Scheduler)

-   Headless environments

-   Batch experimentation

---

## Configuration
### RSS Feeds

RSS sources are defined in `feeds.yaml`.

Example structure:

```bash
feeds:

https://feeds.bbci.co.uk/news/world/rss.xml

https://www.aljazeera.com/xml/rss/all.xml

```

Adding or removing sources requires **no code changes**.

## Outputs
### CSV

MM_DD_YY_news.csv
Contains:
- URL
- Extracted keywords
- Full article text

### Wordcloud Images

PNG files with date-stamped filenames, optionally masked and recolored.

---

## Design Notes

- The pipeline is intentionally tolerant of:
    - Broken RSS feeds
    - Invalid article URLs
    - Sites that block scraping
- Network timeouts prevent hanging processes
- Wordcloud styles are modular and reusable
- Designed for batch execution rather than real-time analysis

---

## Credits

Original inspiration by Craig Helstowski with Finxter
[Newspaper3k – How to Generate a Word Cloud in Python](https://blog.finxter.com/how-to-generate-a-word-cloud-with-newspaper3k-and-python/)

---

## License

MIT License