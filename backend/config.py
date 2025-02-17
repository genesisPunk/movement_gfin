import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    COINMARKETCAP_API_KEY = "a8168dad-bb06-4e8a-9e44-f67d98511fce"
    OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

    # CoinMarketCap API Endpoints
    CMC_BASE_URL = "https://pro-api.coinmarketcap.com/v1"
    CRYPTO_METRICS_URL = f"{CMC_BASE_URL}/cryptocurrency/quotes/latest"
    CRYPTO_NEWS_URL = f"{CMC_BASE_URL}/content/posts/latest"

    PRICE_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    HISTORICAL_API_URL = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/historical"
    # RAG Configuration
    VECTOR_STORE_PATH = r"C:\Users\deepak.c.agrawal\Projects\crypto\backend\rag\vector_store"
    HISTORICAL_DATA_PATH = r"C:\Users\deepak.c.agrawal\Projects\crypto\backend\rag\historical_data.csv"

    #News API KEY
    NEWS_API_KEY= "229f6615529444469653600821ad18c1"
    # Cache Settings
    CACHE_TTL = 300  # 5 minutes
    #Reddit APIs
    REDDIT_CLIENT_ID="NR_0JrFeYHIie4SUnA-Wew"
    REDDIT_CLIENT_SECRET="K155b6U4aMqBeLLdZiTKPLjKcBJu0g"
    REDDIT_USER_AGENT = "TradeAnalysis/1.0 by RevolutionaryEmu9147"