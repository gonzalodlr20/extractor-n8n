from fastapi import FastAPI
import praw

app = FastAPI()

# Configura tus credenciales (puedes usar variables de entorno)
reddit = praw.Reddit(
    client_id=None,
    client_secret=None,
    user_agent="windows:extractor_reflexiones:v1.0 (by /u/TU_USUARIO_REDDIT)"
)

@app.get("/ideas")
def obtener_ideas():
    subreddit = reddit.subreddit("Journaling")
    ideas = []
    
    # Buscamos los "prompts" más populares del mes
    for post in subreddit.search("prompts", sort="top", time_filter="month", limit=20):
        if len(post.title) > 10 and not post.over_18:
            ideas.append({
                "titulo": post.title,
                "texto": post.selftext[:300],
                "url": post.url,
                "score": post.score
            })
            
    return {"status": "success", "data": ideas}
