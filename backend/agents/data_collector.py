import openai
import requests
from config import Config
from utils.cache import Cache
from datetime import datetime, timedelta
from agents.social_agent import SocialSentimentAnalyst
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import os

class DataCollector:

    def __init__(self):
        self.cache = Cache(ttl=Config.CACHE_TTL)
        self.headers = {'X-CMC_PRO_API_KEY': Config.COINMARKETCAP_API_KEY}
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.news_api_key= Config.NEWS_API_KEY
        self.news_api_url = 'https://newsapi.org/v2/everything'
        self.social_analyst = SocialSentimentAnalyst()
        

    def fetch_news(self, query):
        try:
            # Calculate date range (last 7 days)
            to_date = datetime.utcnow()
            from_date = to_date - timedelta(days=7)
            
            params = {
                'q': query,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 5,  # Get top 5 articles
                'apiKey': self.news_api_key
            }
            
            response = requests.get(self.news_api_url, params=params)
            response.raise_for_status()
            
            articles = response.json().get('articles', [])
            
            if not articles:
                return "No recent news articles found"
            
            formatted_news = []
            for article in articles:
                source = article.get('source', {}).get('name', 'Unknown source')
                published_at = article.get('publishedAt', 'Unknown date')
                title = article.get('title', 'No title')
                description = article.get('description', 'No description')
                url = article.get('url', '#')
                
                formatted_news.append({
                    'source': source,
                    'published_at': published_at,
                    'title': title,
                    'description': description,
                    'url': url
                })
            
            return formatted_news
            
        except requests.exceptions.RequestException as e:
            print(f"News API request failed: {e}")
            return "News service unavailable"
        except Exception as e:
            print(f"Error processing news: {e}")
            return "Error fetching news"

    def get_crypto_data(self, symbol):
        try:
            price_params = {'symbol': symbol, 'convert': 'USD'}
            price_res = requests.get(
                Config.PRICE_API_URL,
                headers=self.headers,
                params=price_params
            )
            price_data = price_res.json().get('data', {}).get(symbol, {})
            
            # Example: Fetch historical data via API (adjust based on actual API)
            historical_prices = pd.read_csv(rf"C:\Users\deepak.c.agrawal\Projects\crypto\backend\historical_data\{symbol.upper()}_historical.csv")
            
            news = self.fetch_news(f"{symbol} cryptocurrency")

            reddit_posts = self.social_analyst.fetch_reddit_posts(symbol)
            processed_data = {
                'symbol': symbol,
                'current_price': price_data.get('quote', {}).get('USD', {}),
                'news': news,
                'historical_prices': historical_prices,
                'reddit_posts': reddit_posts,
                'social_sentiment': self.social_analyst.analyze_reddit_sentiment(reddit_posts),
                'timestamp': datetime.now().isoformat()
            }
            self.cache.set(f'{symbol}_data', processed_data)
            return processed_data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def _process_historical_data(self, data):
        # Process API response into DataFrame (adjust based on actual API structure)
        df = pd.DataFrame(data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        return df
    
    def fetch_html(self,url):
        """
        Fetch HTML content from the provided URL.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def fetch_projects(self,url="https://www.movementnetwork.xyz/ecosystem"):
        """
        Scrape the projects from the Ecosystem page.

        This function locates the container with id 'projects_results' and then iterates over each
        project (each <div> with class 'grid__item'), extracting the project name, link, description,
        categories, and languages.
        """
        html = self.fetch_html(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        projects = []

        # Locate the main container holding all projects
        projects_div = soup.find("div", id="projects_results")
        if not projects_div:
            print("Could not find the projects results container.")
            return projects

        # Each project is within a div with class "grid__item"
        grid_items = projects_div.find_all("div", class_="grid__item")
        for item in grid_items:
            # --- Extract project link from the <picture> tag (if available)
            project_link = None
            picture = item.find("picture")
            if picture:
                a_tag = picture.find("a")
                if a_tag and a_tag.get("href"):
                    project_link = a_tag.get("href")

            # --- Extract project name and description from the content block
            project_name = None
            project_description = None
            content_div = item.find("div", class_="content")
            if content_div:
                a_content = content_div.find("a")
                if a_content:
                    h3_tag = a_content.find("h3")
                    if h3_tag:
                        project_name = h3_tag.get_text(strip=True)
                    p_tag = a_content.find("p")
                    if p_tag:
                        project_description = p_tag.get_text(strip=True)
                # Fallback in case description isn't inside the <a> tag:
                if not project_description:
                    p_tag = content_div.find("p")
                    if p_tag:
                        project_description = p_tag.get_text(strip=True)

            # --- Extract tags (categories and languages)
            project_categories = []
            project_languages = []
            tags_ul = item.find("ul", class_="tags")
            if tags_ul:
                for li in tags_ul.find_all("li"):
                    classes = li.get("class", [])
                    text = li.get_text(strip=True)
                    if "tag__cat" in classes:
                        project_categories.append(text)
                    elif "tag__lang" in classes:
                        project_languages.append(text)

            projects.append({
                "name": project_name,
                "link": project_link,
                "description": project_description,
                "categories": project_categories,
                "languages": project_languages,
            })
        return projects

    def group_projects_by_category(self,projects):
        """
        Group the list of projects by their category tags.

        Returns a dictionary where each key is a category name and the value is a list of projects.
        """
        category_groups = {}
        for project in projects:
            for cat in project.get("categories", []):
                if cat not in category_groups:
                    category_groups[cat] = []
                category_groups[cat].append(project)
        return category_groups

    # --- End of your scraping code ---
    def fetch_application_data(self):
        cache_key = f"application_data"
        cached = self.cache.get(cache_key)
        if cached:
            print(f"Using cached application data")
            return cached
        
        # Fetch and group the projects
        projects = self.fetch_projects()
        if not projects:
            print("No projects found. Please verify the page structure.")
        grouped_projects = self.group_projects_by_category(projects)

        # Convert the grouped projects dictionary into a JSON-formatted string.
        # This will serve as the context for our AI agent.
        available_projects_str = json.dumps(grouped_projects, indent=2)
        self.cache.set(cache_key, available_projects_str, 864000)
        #print("Available Projects by Category:")
        #print(available_projects_str)
        return available_projects_str