## Utility Classes
A modular set of Python utility classes for automating common workflows across data science, web scraping, and API integration projects.

Includes reusable components for Notion API, Serp API, web scraping, and document handling, with clean examples and helper functions.

---

### 🐍 Python Version
Code tested for Python version 3.10

---

### 🌏 Venv
- Create environment: `python -m venv venv`
- Activate environment: `venv\Scripts\activate.bat`
- Install from file: `pip install -r requirements.txt`
- Freeze to file: `pip freeze > requirements.txt`
- Deactivate: `exit`

--- 

### 📘 Repository Structure
- Each folder is dedicated to a specialized functionality, e.g., dealing with [Notion](https://www.notion.so/) or [Serp API](https://serpapi.com/).
- Within each folder:
  - `Class.py` holds the class.
  - `Helpers.py` contains any helper functions.
  - `Example.py` demonstrates how the Class and its methods are used.
- Specifics:
  - Webscraper Class: Test URLs and output from a performance test are provided.
  - Notion Class: A 'Page_Content.xls' file is available to be populated with desired page content.

---

## 📌 Features

### ✅ Implemented
- **Document Handling**: Functions for reading/writing `.csv`, `.xls`, `.json`, and `.npy`; lightweight metadata operations.
- **Notion API Integration** *(partially redacted)*: Authenticate, retrieve, and populate content in Notion databases via structured page templates.

### 🚧 In Progress
- **Web Scraping Utilities**: Automated scraping with user-agent rotation, page load checks, and error logging.
- **Serp API Tools**: Wrapper classes for programmatic search queries and structured result parsing.

### 🔮 Upcoming
- **Vector Database Tools**: Planned utilities for chunking, storing, and querying documents via FAISS or other vector DBs.

---
## 🚀 Example Usage

```python
from Notion.Class import NotionClient

notion = NotionClient(api_key="your-key")
notion.update_page(page_id="abc123", content="This is updated page content")
```
📁 More examples can be found in /Notion/Example.py
