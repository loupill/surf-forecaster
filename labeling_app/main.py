
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from labeling_app.db import get_db
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Define the directory where HTML templates are stored
templates = Jinja2Templates(directory = "templates")

@app.get("/rate/{token}")
def get_rating_form(token: str, db: Session=Depends(get_db)):
    result = db.execute(
        text("select * from gold.labeling_sessions where token = :token"), 
        {"token": token}
    )
    session_row = result.fetchone()
    
    if session_row is None:
        return templates.TemplateResponse(
        request=token, 
        name="error.html", 
        context={"token": token}
    )