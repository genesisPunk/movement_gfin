from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import json
import logging
from textblob import TextBlob
from collections import defaultdict

logger = logging.getLogger(__name__)

class NewsAnalyst:
    def __init__(self):
        # Initialize sentiment analyzer
        pass

    def _analyze_single_article(self, text):
        """Analyze sentiment of a single news article."""
        analysis = TextBlob(text)
        # Polarity ranges from -1 (negative) to 1 (positive)
        return analysis.sentiment.polarity

    def _categorize_sentiment(self, score):
        """Convert sentiment score to bullish/bearish/neutral."""
        if score > 0.1:
            return "bullish"
        elif score < -0.1:
            return "bearish"
        else:
            return "neutral"

    def analyze_sentiment(self, news_items):
        try:
            if not news_items or not isinstance(news_items, list):
                return {"error": "Invalid news data"}

            sentiment_scores = []
            key_events = []
            source_sentiments = defaultdict(list)

            # Analyze each news item
            for item in news_items:
                title = item.get('title', '')
                description = item.get('description', '')
                source = item.get('source', 'Unknown')

                # Combine title and description for analysis
                text = f"{title}. {description}"
                if not text.strip():
                    continue

                # Get sentiment score
                score = self._analyze_single_article(text)
                sentiment_scores.append(score)
                source_sentiments[source].append(score)

                # Identify key events
                if abs(score) >= 0.3:  # Significant sentiment
                    key_events.append({
                        "title": title,
                        "source": source,
                        "sentiment": self._categorize_sentiment(score),
                        "confidence": abs(score) * 100
                    })

            if not sentiment_scores:
                return {"error": "No valid news items to analyze"}

            # Calculate overall sentiment
            avg_score = sum(sentiment_scores) / len(sentiment_scores)
            overall_sentiment = self._categorize_sentiment(avg_score)
            confidence = abs(avg_score) * 100  # Scale to 0-100

            # Source-wise sentiment breakdown
            source_analysis = {
                source: {
                    "sentiment": self._categorize_sentiment(sum(scores) / len(scores)),
                    "confidence": abs(sum(scores) / len(scores)) * 100
                }
                for source, scores in source_sentiments.items()
            }

            return {
                "sentiment": overall_sentiment,
                "confidence": round(confidence, 2),
                "key_events": key_events,
                "source_analysis": source_analysis
            }

        except Exception as e:
            return {"error": str(e)}