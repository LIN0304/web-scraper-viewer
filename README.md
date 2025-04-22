# Web Scraper and Viewer

A simple but powerful web scraper that crawls websites and converts their content to structured Markdown, along with a Flask-based viewer to browse the captured content.

## Features

- **BFS Website Crawling**: Efficiently crawls websites using breadth-first search
- **Markdown Generation**: Converts web content to well-formatted Markdown
- **JSON Storage**: Preserves all scraped data in original JSON format
- **Web Viewer**: Browse and read scraped content through a clean web interface
- **Download Options**: Access raw Markdown or JSON data for each page

## Project Structure

```
web-scraper-viewer/
├─ main.py               # Web scraper script
├─ app.py                # Flask viewer app
├─ requirements.txt      # Dependencies
├─ .gitignore            # Ignore scraped files & virtual env
├─ scraped_data/         # Scraper output (auto-generated)
├─ templates/            # Flask HTML templates
│   ├─ base.html
│   ├─ index.html
│   └─ view.html
└─ static/               # Static assets
    └─ style.css
```

## Setup and Usage

### Installation

```bash
# 1) Clone this repository
git clone https://github.com/LIN0304/web-scraper-viewer.git
cd web-scraper-viewer

# 2) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt
```

### Running the Scraper

```bash
# Scrape a website (example)
python main.py --url https://example.com --max-pages 50
```

This will:
- Crawl the website starting at the URL provided
- Generate Markdown files in `scraped_data/page_0.md`, etc.
- Save raw data as JSON files in `scraped_data/page_0_original.json`, etc.

### Viewing the Results

```bash
# Start the Flask web app
python app.py
```

Then open your browser to http://127.0.0.1:5000/ to browse the scraped content.

## Customization

- Modify `main.py` to adjust scraping behavior or content formatting
- Edit templates in `templates/` to change the viewer appearance
- Update `static/style.css` to customize the styling

## License

This project is available under the MIT License.
