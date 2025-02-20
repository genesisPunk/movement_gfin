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

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define routes FIRST
@app.get("/health")
async def health_check():
    return {"status": "ok"}

class GoalRequest(BaseModel):
    user_goal: str

@app.post("/submit_goal")
async def handle_goal(request: GoalRequest):
    all_analyses = []
    symbols = ['MOVE', 'WBTC', 'WETH', 'USDT', 'USDC']
    application_data = collector.fetch_application_data()
    
    for symbol in symbols:
        crypto_data = collector.get_crypto_data(symbol)
        if not crypto_data:
            return {"error": "No market data available"}
        
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
    print(recommendations)
    
    bus.publish('recommendations', {
        "goal": request.user_goal,
        "actions": recommendations,
        "analysis": all_analyses
    })
    print(all_analyses)

    return {"goal": request.user_goal, "recommendations": recommendations, "analysis": all_analyses}

@app.post("/confirm_action")
async def execute_action(action: str):
    from agents.execution_agent import ExecutionAgent
    executor = ExecutionAgent()
    return executor.execute_action(action)

# Initialize dependencies AFTER routes
bus = MessageBus()
collector = DataCollector()
news_analyst = NewsAnalyst()
recommender = ActionRecommender()
market_analyst = MarketAnalyst()

# Startup logging for debugging
@app.on_event("startup")
async def startup_event():
    print("Server starting...")
    try:
        # Test a dependency
        test_data = collector.get_crypto_data("MOVE")
        print("Dependencies initialized:", test_data)
    except Exception as e:
        print("ERROR on startup:", e)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Use Render's PORT variable
    uvicorn.run("main:app", host="0.0.0.0", port=port)
