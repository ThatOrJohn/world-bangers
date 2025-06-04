# LastFM Globe Tracks

A fun, interactive Streamlit app that visualizes the top 5 tracks from Last.fm by country on a 3D globe. Spin the globe, hover for tooltips with track details, and select a country to see its most popular tracks from the past week, as reported by Last.fm's `geo.getTopTracks` API. Features flashy colors, cached data, and a vibrant, music-driven experience!

## Features

- **Interactive 3D Globe**: Built with Plotly, spin and zoom to explore countries.
- **Top Tracks by Country**: Displays the top 5 tracks (track name, artist, listeners) for a selected country.
- **Hover Tooltips**: Hover over a country on the globe to see its top tracks and listener counts.
- **Flashy Colors**: Vibrant `Plasma` color scale highlights countries by total listeners.
- **Data Caching**: API responses cached for 24 hours to respect Last.fm’s weekly data cycle and avoid rate limits.
- **Secure Config**: Uses `python-dotenv` to load the Last.fm API key from a `.env` file.

## Prerequisites

- Python 3.8 or higher
- A Last.fm API key (get one at [Last.fm API](https://www.last.fm/api))
- A `.env` file with your API key

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/lastfm-globe-tracks.git
   cd lastfm-globe-track
   ```
2. **Set Up a Virtual Environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ``bash
   pip install -r requirements.txt
   ```

   ```
4. **Configure the API Key**

- Create a `.env` file in the project root.
- Add your Last.fm API key:
  ```
  LASTFM_API_KEY=your_api_key_here
  ```
- Get your API key from [Last.fm API.](https://www.last.fm/api)

## Usage

1. **Run the App Locally**
   ```bash
   streamlit run app.py
   ```
   - Open your browser to `http://localhost:8501`.
   - Select a country from the dropdown to see its top 5 tracks.
   - Hover over the globe to view tooltips with track details for any country.
2. **Explore the Globe**
   - Spin and zoom the 3D globe to explore countries.
   - Colors reflect total listeners for the top tracks, with a vibrant Plasma scale.
   - Data is cached for 24 hours to improve performance and respect API limits.
