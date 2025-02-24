# movement_gfin
 Introducing Gfin, a personal financial AI assistant built on OpenAI LLM with customized RAG, tailored for the Movement blockchain ecosystem. Users set financial goals (e.g., 2x returns), and the AI analyzes data (news, sentiments, etc.) to provide tailored investment advice in Movement tokens and Dapps. It continuously monitors and adjusts portfolios to optimize outcomes.


# Brief Architecture
![brief_architecture](https://github.com/genesisPunk/movement_gfin/blob/31d171ea89f4784ae3a6e88538b8211211cbdd7c/brief_architecture.png) 

# Tech Stack
![tech_stack](https://github.com/genesisPunk/movement_gfin/blob/4f0ee0ff09de24f2f0a1ba845baf649bbb5a4354/techstack.png)

# Steps to Run Backend
1. Navigate to backend directory
2. Update all the secrets in Config.py
3. Create virtual environment (Windows)
    python -m venv venv
4. Activate virtual environment (Windows)
    .\venv\Scripts\activate
5. Install Python dependencies
   pip install -r requirements.txt
6.  Run FastAPI server
   uvicorn main:app --reload --port 8001

# Steps to Run Frontend
On different terminal 
1. Navigate to frontend directory
2. Run npm install
3. If you get dependency errors, try: (optional)
   npm install --force
4. npm start
