# WordCloud

A news aggregation and visualization project that uses web scraping, natural language processing (NLP), and matplotlib to generate insightful word clouds from current news articles.

The project supports:

- RSS-based news ingestion
- Article parsing and keyword extraction via NLP
- Archival datasets (CSV)
- Multiple wordcloud visual styles, including image masks and recoloring

Originally built as a **Jupyter Notebook**, the project now also supports **script-based execution** for repeatable and automated runs.

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
### Jupyter Notebook (Original Workflow)

This project was originally designed to run as a Jupyter Notebook.

Open a terminal and navigate to the directory where you want to install the project, then run:

```bash
git clone https://github.com/mathewrtaylor/WordCloud.git
 WordCloud
cd WordCloud
conda env create -f environment.yml
```

Activate the environment and install dependencies:

```bash
source activate WordCloud
conda install --force-reinstall -y -q --name WordCloud -c conda-forge --file requirements.txt
jupyter lab
```

---

## Usage
### Jupyter Notebook

1. Launch Jupyter Lab
2. Open the notebook in the project directory
3. Run cells top-to-bottom to:
    - Load RSS feeds
    - Download and parse articles
    - Generate datasets
    - Render wordclouds

This is the best way to explore and tweak visual styles interactively.

---

### Python Script (Automated / Repeatable)

The core logic has been refactored into reusable functions so the workflow can also be run as a standard Python script.

Example execution:

```bash
python wordcloud_pipeline.py
```

Script execution:

- Loads RSS feeds from feeds.yaml
- Downloads and parses articles
- Exports a date-stamped CSV file
- Generates one or more wordcloud images

This mode is ideal for:

- Scheduled runs (cron, Task Scheduler)
- Headless environments
- Batch experimentation

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