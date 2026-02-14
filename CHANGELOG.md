# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-02-14

### Changed
- Refactored `word_cloud.py` to encapsulate main execution logic within a `main()` function, called under `if __name__ == '__main__':`, enhancing modularity and reusability.
- Modified `check_nltk_resource` in `word_cloud.py` to automatically download missing NLTK 'punkt_tab' data, improving script robustness.
- Updated `README.md` to clarify the independent nature of `word_cloud.py` and `Word Cloud.ipynb`.
- Revised `README.md` installation instructions to use `pip install -r requirements.txt` and a Python virtual environment.
- Updated `README.md` usage sections for both the Python script and Jupyter Notebook to reflect changes and emphasize independence.
- Updated `llms.txt` to accurately reflect the architectural changes and emphasize the independence of the script and notebook.