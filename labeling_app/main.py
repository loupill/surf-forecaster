
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from labeling_app.db import get_db

app = FastAPI()

@app.get("/rate/{token}")
def get_rating_form(token: str, db: Session=Depends(get_db)):
    result = db.execute(
        text("select * from gold.labeling_sessions where token = :token"), 
        {"token": token}
    )
    session_row = result.fetchone()
    
    if session_row is None:
            raise HTTPException(status_code=404, detail='No token found')
    return {"break_id": session_row.break_id}