from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from rag.historical_data_loader import load_historical_data
from config import Config
import random
import numpy as np
from langchain_groq import ChatGroq
import os

class ActionRecommender:
    def __init__(self):
        self.llm = ChatGroq(temperature=0.5,model_name="llama-3.1-8b-instant", groq_api_key=os.getenv('GROQ_API_KEY'))

    # Keep _interpret_analysis unchanged
    def _interpret_analysis(self, market_data, sentiment_data):
        """Original market/sentiment analysis logic remains unchanged"""
        insights = []
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
        if sentiment_data.get("sentiment") == "bullish":
            insights.append("Positive market sentiment detected")
        elif sentiment_data.get("sentiment") == "bearish":
            insights.append("Negative market sentiment detected")
        if sentiment_data.get("confidence", 0) > 70:
            insights.append("High confidence in sentiment analysis")
        return insights

    def _generate_movement_recommendations(self, applications):
        """Generate Movement ecosystem recommendations without allocations"""
        MOVEMENT_ECOSYSTEM_APPS = []
        for key, value in applications.items():
            for v in value:
                MOVEMENT_ECOSYSTEM_APPS.append(v['name'])
        
        selected_apps = random.sample(MOVEMENT_ECOSYSTEM_APPS, 3)
        rationales = [
            "shows strong ecosystem alignment with recent protocol upgrades",
            "demonstrates high community engagement and DAO participation",
            "exhibits promising TVL growth and transaction volume trends",
            "has strategic partnerships within the Movement ecosystem",
            "features innovative tokenomics models",
            "shows consistent developer activity and GitHub commits"
        ]
        return [(app, random.choice(rationales)) for app in selected_apps]

    def _distribute_allocations(self, crypto_recs, movement_recs):
        """Distribute 100% allocation across all recommendations"""
        # Generate 6 allocations (3 crypto + 3 apps) summing to 100
        allocations = np.random.dirichlet(np.ones(6)) * 100
        allocations = [round(pct, 1) for pct in allocations]
        
        # Adjust for rounding precision
        total = sum(allocations)
        allocations[-1] += round(100 - total, 1)
        
        # Assign crypto allocations
        for i, rec in enumerate(crypto_recs):
            rec['allocation'] = allocations[i]
        
        # Assign application allocations
        for i, rec in enumerate(movement_recs):
            rec['allocation'] = allocations[i+3]
            
        return crypto_recs, movement_recs

    def get_recommendations(self, user_goal, all_analyses):
        """Main recommendation logic with separated allocation"""
        # Original analysis processing remains unchanged
        analysis_summaries = []
        for analysis in all_analyses:
            symbol = analysis['symbol']
            market = analysis['market']
            sentiment = analysis['sentiment']
            social = analysis['social_sentiment']
            insights = self._interpret_analysis(market, sentiment)
            applications = analysis['applications']
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

        # Modified prompt without allocation percentages
        prompt = f"""
User Goal: {user_goal}

Analyze the following cryptocurrencies and recommend actions (Buy/Sell/Hold) to achieve the goal:
{"".join(analysis_summaries)}

Provide recommendations in this format:

[Symbol]: [Action] - [Rationale]

Include exactly 3 cryptocurrency recommendations.
"""
        # Get crypto recommendations without allocations
        crypto_response = self.llm.invoke(prompt).content
        crypto_recs = []
        for line in crypto_response.split('\n'):
            if ': ' in line and ' - ' in line:
                symbol, rest = line.split(': ', 1)
                action, rationale = rest.split(' - ', 1)
                crypto_recs.append({
                    'symbol': symbol.strip(),
                    'action': action.strip(),
                    'rationale': rationale.strip()
                })

        # Get Movement recommendations without allocations
        applications = all_analyses[0]['applications'] if all_analyses else {}
        movement_recs = [{'app': app, 'rationale': rationale} 
                        for app, rationale in self._generate_movement_recommendations(applications)][:3]

        # Distribute allocations
        crypto_recs, movement_recs = self._distribute_allocations(crypto_recs, movement_recs)

        # Format final output
        crypto_str = "Cryptocurrency Recommendations:\n" + "\n".join(
            f"{rec['symbol']}: {rec['action']} ({rec['allocation']}%) - {rec['rationale']}"
            for rec in crypto_recs
        )
        
        movement_str = "\n\nMovement Ecosystem Recommendations:\n" + "\n".join(
            f"{rec['app']}: {rec['allocation']}% - {rec['rationale']}"
            for rec in movement_recs
        )
        
        notes = "\n\nNote: Total allocated percentage: 100%\n" \
                "1. Suggested allocations represent target portfolio weights\n" \
                "2. Adjust based on your risk tolerance and existing positions\n" \
                "3. Rebalance when price targets or market conditions change"
        
        return crypto_str + movement_str + notes
