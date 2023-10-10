from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json, settings

app = FastAPI()
with open(settings.SRC_DIR / "score.json", "r") as f:
    scores = json.load(f)["scores"]

class Score(BaseModel):
    id: Optional[int] = None
    player: str
    score: str

@app.get('/')
def scoreboard():
    return scores

@app.post('/addScore', status_code=201)
def post_score(score: Score):
    s_id = max([s['id'] for s in scores]) + 1
    new_score = {
        "id": s_id,
        "player": score.player,
        "score": score.score
    }

    scores.append(new_score)

    with open(settings.SRC_DIR / "score.json", "w") as f:
        json.dump(scores, f)

    return new_score
