
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session
from labeling_app.db import get_db
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="labeling_app/static"), name="static")

# Define the directory where HTML templates are stored
templates = Jinja2Templates(directory = "labeling_app/templates")

@app.get("/rate/{token}")
def get_rating_form(request: Request, token: str, db: Session=Depends(get_db)):
    result = db.execute(
        text("select * from gold.labeling_sessions where token = :token"), 
        {"token": token}
    )
    session_row = result.fetchone()
    
    if session_row is None:
        return templates.TemplateResponse(
        request=request, 
        name="error.html", 
        context={"token": token}
    )

    return templates.TemplateResponse(
        request=request,
        name="rate_form.html",
        context={
            "token": token,
            "break_id": session_row.break_id,
            "session_date": session_row.session_date
        }
    )