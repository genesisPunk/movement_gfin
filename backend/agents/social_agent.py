import praw  # Python Reddit API Wrapper
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from config import Config
from langchain_groq import ChatGroq
import os

class SocialSentimentAnalyst:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            user_agent=Config.REDDIT_USER_AGENT
        )
        self.analyzer = SentimentIntensityAnalyzer()
        self.llm = ChatGroq(temperature=0.5,model_name="llama-3.1-8b-instant", groq_api_key=os.getenv('GROQ_API_KEY'))

    def fetch_reddit_posts(self, crypto_name, limit=50):
        """Fetch recent Reddit posts about a cryptocurrency"""
        try:
            posts = []
            for submission in self.reddit.subreddit('all').search(
                f'{crypto_name} cryptocurrency',
                sort='relevance',
                time_filter='week',
                limit=limit
            ):
                posts.append({
                    'title': submission.title,
                    'content': submission.selftext,
                    'upvotes': submission.score,
                    'comments': submission.num_comments,
                    'created': submission.created_utc
                })
            return posts
        except Exception as e:
            print(f"Reddit API error: {e}")
            return []

    def analyze_reddit_sentiment(self, posts):
        """Analyze sentiment of Reddit posts using combined VADER and LLM analysis"""
        if not posts:
            return {"error": "No Reddit posts found"}
        # VADER Sentiment Analysis
        vader_scores = []
        weighted_scores = []
        
        for post in posts:
            vs = self.analyzer.polarity_scores(post['title'] + " " + post['content'])
            vader_scores.append(vs['compound'])
            # Weight by post engagement
            weight = 1 + (post['upvotes'] / 100) + (post['comments'] / 10)
            weighted_scores.append(vs['compound'] * weight)
        
        avg_vader = sum(vader_scores) / len(vader_scores)
        avg_weighted = sum(weighted_scores) / sum(1 + (p['upvotes']/100) + (p['comments']/10) for p in posts)

        # LLM Analysis for contextual understanding
        llm_analysis = self._llm_sentiment_analysis(posts)
        
        return {
            'vader_score': avg_vader,
            'weighted_score': avg_weighted,
            'llm_analysis': llm_analysis,
            'post_count': len(posts),
            'average_upvotes': sum(p['upvotes'] for p in posts) / len(posts),
            'average_comments': sum(p['comments'] for p in posts) / len(posts)
        }

    def _llm_sentiment_analysis(self, posts):
        """Use LLM for nuanced sentiment analysis"""
        sample_posts = "\n".join([p['title'] for p in posts[:5]])
        prompt = f"""
        Analyze the sentiment of these cryptocurrency-related Reddit posts:
        {sample_posts}

        Consider:
        - Overall market sentiment
        - Common themes/topics
        - Investor confidence level
        - Potential market manipulation signs

        Return analysis in this format:
        - Overall Sentiment: [bearish/neutral/bullish]
        - Confidence: [0-100]
        - Key Themes: [comma-separated list]
        - Anomalies: [notable observations]
        """
        
        response = self.llm.invoke(prompt)
        return response.content
