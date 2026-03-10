# Video Game Sales Explorer

An interactive Dash application for exploring global video game sales data from 1980 to 2016.

## Overview

This app allows users to explore trends in video game sales across regions, genres, platforms, and publishers using a dataset of over 16,000 titles.

## How to Run

1. Clone this repository or download the files.

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Make sure `vgsales.csv` is in the same directory as `app.py`.

4. Run the app:
```
python app.py
```

5. Open your browser and go to `http://127.0.0.1:8050/`

## Dataset

`vgsales.csv` — Video Game Sales dataset sourced from Kaggle (https://www.kaggle.com/datasets/gregorut/videogamesales). Contains 16,000+ games with sales figures broken down by region (North America, Europe, Japan, Other, Global), along with genre, platform, publisher, and release year.

## Controls

- **Region** — Select which regional sales figure to display across all charts
- **Genre** — Filter all charts to a specific game genre or view all genres
- **Top Games Chart Style** — Toggle between vertical and horizontal bar chart for the top 10 games view
- **Year Range** — Slide to filter all charts to a specific range of release years

## Charts

1. **Top 10 Games by Sales** — Bar chart showing the highest selling individual titles for the selected filters
2. **Sales Trend Over Time by Genre** — Line chart showing how sales have changed year over year across genres
3. **Sales by Genre** — Bar chart comparing total sales across all 12 genres
4. **Top 10 Publishers by Sales** — Horizontal bar chart showing the highest selling publishers

## Files

- `app.py` — Main Dash application
- `vgsales.csv` — Dataset
- `requirements.txt` — Python dependencies
- `README.md` — This file
