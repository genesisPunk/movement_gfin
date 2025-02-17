from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from rag.historical_data_loader import load_historical_data
from config import Config

class ActionRecommender:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4",api_key=Config.OPENAI_API_KEY)

    def _interpret_analysis(self, market_data, sentiment_data):
        """Interpret market and sentiment data into actionable insights."""
        insights = []
        
        # Market Analysis Insights
        if market_data.get("rsi", 50) < 30:
            insights.append("Oversold market conditions (RSI < 30)")
        elif market_data.get("rsi", 50) > 70:
            insights.append("Overbought market conditions (RSI > 70)")
        
        if market_data.get("price_change", "").endswith("%"):
            price_change = float(market_data["price_change"][:-1])
            if price_change < -10:
                insights.append("Significant price drop in recent period")
            elif price_change > 10:
                insights.append("Significant price increase in recent period")
        
        if "Bullish MACD crossover" in market_data.get("trend_strength", []):
            insights.append("Bullish momentum indicated by MACD crossover")
        
        # Sentiment Analysis Insights
        if sentiment_data.get("sentiment") == "bullish":
            insights.append("Positive market sentiment detected")
        elif sentiment_data.get("sentiment") == "bearish":
            insights.append("Negative market sentiment detected")
        
        if sentiment_data.get("confidence", 0) > 70:
            insights.append("High confidence in sentiment analysis")
        
        return insights

    def get_recommendations(self, user_goal, all_analyses):
        analysis_summaries = []
        for analysis in all_analyses:
            symbol = analysis['symbol']
            market = analysis['market']
            sentiment = analysis['sentiment']
            social = analysis['social_sentiment']
            insights = self._interpret_analysis(market, sentiment)
            summary = (
                f"Crypto: {symbol}\n"
                f"Price Change: {market.get('price_change', 'N/A')}\n"
                f"RSI: {market.get('rsi', 'N/A')}\n"
                f"Trend: {market.get('recent_trend', 'N/A')}\n"
                f"Sentiment: {sentiment.get('sentiment', 'N/A')} "
                f"(Confidence: {sentiment.get('confidence', 'N/A')}%)\n"
                f"Insights: {', '.join(insights)}\n"
                f"Social Sentiment: {social.get('llm_analysis', 'N/A')}\n"
                f"Reddit Score: {social.get('weighted_score', 'N/A')}\n"
                f"Posts Analyzed: {social.get('post_count', 0)}\n"
            )

            analysis_summaries.append(summary)
        
        prompt = f"""
        User Goal: {user_goal}

        Analyze the following cryptocurrencies and recommend actions (Buy/Sell/Hold) to achieve the goal:
        {"".join(analysis_summaries)}

        Provide recommendations in this format:
        - [Symbol]: [Action] - [Rationale]

        Consider:
        1. Market trends (RSI, MACD, moving averages)
        2. News sentiment and key events
        3. Portfolio diversification and risk management

        Consider these social sentiment factors as well:
        - Reddit sentiment scores
        - LLM analysis of discussion themes
        - Post engagement metrics
        - Anomalies detected in social posts
        """
        response = self.llm.invoke(prompt)
        return response.content
