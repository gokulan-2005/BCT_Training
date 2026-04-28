# AI News

`AI News` is a small CrewAI-based Python project that researches a topic, scrapes recent news articles, and generates a markdown news brief using Gemini.

## Features

- Searches recent news links for a topic
- Scrapes article content from direct URLs
- Generates a markdown summary with sources
- Saves the result to the `outputs/` folder

## Project Structure

```text
ai_news/
├── .env
├── .env.template
├── .gitignore
├── README.md
├── requiremnts.txt
├── outputs/
└── src/
    └── ai_news/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        ├── tools.py
        └── config/
            ├── agents.yaml
            └── tasks.yaml
```

## Requirements

- Python 3.10+
- A Google API key for Gemini

## Setup

Install dependencies:

```powershell
pip install -r requiremnts.txt
```

Create your environment file from the template:

```powershell
copy .env.template .env
```

Update `.env` with your key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

## Run

Run interactively:

```powershell
python -m src.ai_news.main
```

Or run directly with a topic:

```powershell
'usa vs iran war' | python -m src.ai_news.main
```

If `python` is not available on your machine, try:

```powershell
py -m src.ai_news.main
```

## Output

Generated articles are saved in the `outputs/` folder.

Example:

```text
outputs/usa-vs-iran-war.md
```

## How It Works

The project uses a two-step CrewAI workflow:

1. A research agent searches recent news and scrapes article pages.
2. A writer agent turns the scraped notes into a markdown article.
3. The article is saved automatically to the `outputs/` folder.

## Notes

- Some websites may block scraping or return partial content.
- The workflow uses `gemini-2.5-flash-lite`.
- Generated content should be reviewed before publishing or sharing.

## GitHub Safety

The repo includes:

- `.gitignore` to exclude secrets, Python cache files, and generated outputs
- `.env.template` so you can share the project without exposing your real API key

