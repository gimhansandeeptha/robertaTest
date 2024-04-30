from fastapi import APIRouter
from datetime import date, timedelta
from src.database.main import Database

router = APIRouter()

@router.get("/get_comments",tags=['api'])
async def get_comments_with_sentiment(start: date|None=None, end: date|None=None):
    start_date=start
    end_date=end

    if start_date is None:
        start_date = date.today()-timedelta(days=1)
    if end_date is None:
        end_date = date.today()-timedelta(days=1)

    db = Database()
    cases = db.get_cases_by_date(start_date=start_date, end_date=end_date)
    return cases
