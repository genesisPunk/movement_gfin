import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.data_collector import DataCollector
from agents.news_analyst import NewsAnalyst
from agents.action_recommender import ActionRecommender
from utils.message_bus import MessageBus
from agents.market_analyst import MarketAnalyst
import uvicorn

app = FastAPI(
    title="Movement Token Analysis",
    description="API for analyzing movement tokens and smart contracts using multiple specialized agents",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global dependency placeholders (initialized in startup_event)
bus = None
collector = None
news_analyst = None
recommender = None
market_analyst = None

@app.on_event("startup")
async def startup_event():
    """ Initializes dependencies when the server starts. """
    global bus, collector, news_analyst, recommender, market_analyst
    print("🚀 Server is starting...")

    try:
        # Initialize dependencies inside startup to prevent execution during import
        bus = MessageBus()
        collector = DataCollector()
        news_analyst = NewsAnalyst()
        recommender = ActionRecommender()
        market_analyst = MarketAnalyst()
        
        print("✅ Dependencies initialized successfully")
    except Exception as e:
        print(f"❌ ERROR during startup: {e}")

@app.get("/")
async def root():
    return {"message": "Movement Agent API is running"}

class GoalRequest(BaseModel):
    user_goal: str

@app.post("/submit_goal")
async def handle_goal(request: GoalRequest):
    """ Handles goal submission, fetches market data, and analyzes sentiment. """
    global collector, news_analyst, market_analyst, recommender

    if not collector or not news_analyst or not market_analyst or not recommender:
        return {"error": "Server not initialized properly"}

    all_analyses = []
    symbols = ['MOVE', 'WBTC', 'WETH', 'USDT', 'USDC']
    
    try:
        application_data = collector.fetch_application_data()

        for symbol in symbols:
            crypto_data = collector.get_crypto_data(symbol)
            if not crypto_data:
                continue  # Skip if no data available

            market_analysis = market_analyst.analyze_trends(crypto_data['historical_prices'])
            sentiment_analysis = news_analyst.analyze_sentiment(crypto_data['news'])
            social_sentiment = crypto_data.get('social_sentiment', {})

            all_analyses.append({
                'symbol': symbol,
                'market': market_analysis,
                'sentiment': sentiment_analysis,
                'social_sentiment': social_sentiment,
                'applications': application_data
            })

        recommendations = recommender.get_recommendations(request, all_analyses)
        bus.publish('recommendations', {
            "goal": request.user_goal,
            "actions": recommendations,
            "analysis": all_analyses
        })

        return {"goal": request.user_goal, "recommendations": recommendations, "analysis": all_analyses}
    
    except Exception as e:
        print(f"❌ Error in /submit_goal: {e}")
        return {"error": str(e)}

@app.post("/confirm_action")
async def execute_action(action: str):
    """ Executes an action via ExecutionAgent. """
    from agents.execution_agent import ExecutionAgent
    try:
        executor = ExecutionAgent()
        return executor.execute_action(action)
    except Exception as e:
        return {"error": f"Failed to execute action: {e}"}

@app.get("/health")
async def health_check():
    """ Health check endpoint. """
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Use Render's PORT variable
    uvicorn.run("main:app", host="0.0.0.0", port=port)
