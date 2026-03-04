import os 

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
supervisor_model="llama-3.3-70b-versatile"
WORK_Model="llama-3.1-8b-instant"