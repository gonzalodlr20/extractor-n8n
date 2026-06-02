import urllib.request
import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/ideas")
def obtener_ideas():
    # URL de búsqueda de Reddit (formato JSON directo)
    url = "https://www.reddit.com/r/Journaling/search.json?q=prompts&restrict_sr=1&sort=top&t=month&limit=20"
    
    # Camuflaje: Nos identificamos honestamente para que Reddit no nos bloquee
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "windows:extractor_reflexiones:v1.0 (by /u/Gonzalo_R)"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        ideas = []
        # Buceamos en la estructura del JSON que devuelve Reddit
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            titulo = post.get("title", "")
            texto = post.get("selftext", "")
            
            if len(titulo) > 10 and not post.get("over_18"):
                ideas.append({
                    "titulo": titulo,
                    "texto": texto[:300], # Solo los primeros 300 caracteres
                    "url": post.get("url", ""),
                    "score": post.get("score", 0)
                })
                
        return {"status": "success", "data": ideas}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
