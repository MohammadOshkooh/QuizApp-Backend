from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import get_categories
from database import get_db
from schemas import CategoryOut

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)
