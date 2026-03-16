# Release Notes - Version 1.0.2

This release fixes a critical bug that prevented `word_cloud.py` from running at all, along with several code quality and consistency improvements.

## Key Changes in this Release:

### **Critical Bug Fix (`word_cloud.py`)**
- **Script now runs end-to-end:** `collect_news_articles()` and `generate_wordcloud()` — called in `main()` but never defined — have been implemented. The script was completely non-functional before this fix.
- **Robust error handling:** `main()` now catches failures in article collection and exits cleanly instead of crashing with an unhandled exception.
- **Working directory independent:** Mask image paths now resolve relative to the script file, not the shell's working directory.

### **Notebook Consistency**
- The notebook now loads feeds from `feeds.yaml` instead of a hardcoded list, keeping it in sync with the script configuration.
- Fixed a bare `except:` clause that could silently swallow `KeyboardInterrupt` and other system signals.

### **Code Quality**
- `print()` replaced with `logging` throughout `word_cloud.py` for cleaner batch-run output.
- Type hints added to all functions.
- Removed duplicate stopword entry.
- Removed 5 unused packages (`duckdb`, `pdfplumber`, `pdfminer.six`, `PyMuPDF`, `pypdfium2`) from `requirements.txt`.

---

# Release Notes - Version 1.0.1

We're excited to announce an update to the WordCloud project, focusing on improved usability, modularity, and clarity for both our Python script and Jupyter Notebook users.

## Key Enhancements in this Release:

### **Enhanced Python Script (`word_cloud.py`)**
-   **Improved Modularity:** The core logic of `word_cloud.py` has been refactored into a clear `main()` function. This means the script is now more organized and easier to integrate into other Python projects if needed.
-   **Automated Setup:** The script now automatically detects and downloads the necessary NLTK 'punkt_tab' data, eliminating manual setup steps and making automated runs smoother.

### **Clearer Documentation**
-   **Independent Tools:** The `README.md` has been updated to clearly state that both `word_cloud.py` and `Word Cloud.ipynb` are independent and fully functional tools, allowing you to choose the best approach for your workflow.
-   **Simplified Installation:** Installation instructions in `README.md` have been streamlined, now focusing on `pip` and Python virtual environments for easier setup.
-   **Detailed Usage Guides:** The `README.md` now provides more comprehensive instructions for running both the Python script and the Jupyter Notebook.

We believe these changes will make the WordCloud project more accessible and robust for all users.

Thank you for using the WordCloud project!