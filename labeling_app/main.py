
from fastapi import FastAPI, Depends, HTTPException, Request, Form
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


@app.post("/rate/{token}")
def post_rating(
    token: str,
    request: Request,    
    morning_rating: int = Form(...),
    morning_comment: str = Form(""),
    midday_rating: int = Form(...),
    midday_comment: str = Form(""),
    evening_rating: int = Form(...),
    evening_comment: str = Form(""),
    db: Session = Depends(get_db),

):    

    result = db.execute(
        text("select id from gold.labeling_sessions where token = :token"),
        {"token": token}
    )

    session_id_row = result.fetchone()

    if session_id_row is None:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"token": token}
        )

    # UPDATE INSERT STATEMENTS - NEED ONE PER SESSION (MORNING MIDDAY EVENING)

    
    insert_morning = db.execute(
        text("insert into gold.human_labels (session_id, time_block, rating, comment) values (:session_id, 'morning', :rating, :comments)"),
        {"session_id": session_id_row.id, "rating": morning_rating, "comments": morning_comment}
    ) 


    insert_midday = db.execute(
        text("insert into gold.human_labels (session_id, time_block, rating, comment) values (:session_id, 'midday', :rating, :comments)"),
        {"session_id": session_id_row.id, "rating": midday_rating, "comments": midday_comment}
    ) 

    insert_evening = db.execute(
        text("insert into gold.human_labels (session_id, time_block, rating, comment) values (:session_id, 'evening', :rating, :comments)"),
        {"session_id": session_id_row.id, "rating": evening_rating, "comments": evening_comment}
    ) 

    db.execute(
        text("update gold.labeling_sessions set responded_at = now() where id = :session_id"),
        {"session_id": session_id_row.id}
    )

    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={}
    )