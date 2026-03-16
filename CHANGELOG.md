# Changelog

All notable changes to this project will be documented in this file.

## [1.0.2] - 2026-03-16

### Fixed
- Defined `collect_news_articles` and `generate_wordcloud` functions in `word_cloud.py`; the script was previously non-functional due to these missing definitions.
- Added `try/except` around `collect_news_articles` call in `main()` for graceful failure on network errors.
- Added `import os` and used `os.path` for mask image paths, so the script works regardless of working directory.
- Replaced bare `except:` with `except Exception:` in the Jupyter notebook article-parsing cell.
- Removed duplicate `'globalnews'` entry from stopwords list.
- Fixed unused exception variable `as e` in `check_nltk_resource`.

### Changed
- Replaced `print()` calls with `logging` throughout `word_cloud.py` for better batch-run observability.
- Updated Jupyter notebook to load RSS feeds from `feeds.yaml` instead of hardcoding them.
- Added type hints to all functions in `word_cloud.py`.
- Removed unused packages (`duckdb`, `pdfplumber`, `pdfminer.six`, `PyMuPDF`, `pypdfium2`) from `requirements.txt`.

## [1.0.1] - 2026-02-14

### Changed
- Refactored `word_cloud.py` to encapsulate main execution logic within a `main()` function, called under `if __name__ == '__main__':`, enhancing modularity and reusability.
- Modified `check_nltk_resource` in `word_cloud.py` to automatically download missing NLTK 'punkt_tab' data, improving script robustness.
- Updated `README.md` to clarify the independent nature of `word_cloud.py` and `Word Cloud.ipynb`.
- Revised `README.md` installation instructions to use `pip install -r requirements.txt` and a Python virtual environment.
- Updated `README.md` usage sections for both the Python script and Jupyter Notebook to reflect changes and emphasize independence.
- Updated `llms.txt` to accurately reflect the architectural changes and emphasize the independence of the script and notebook.