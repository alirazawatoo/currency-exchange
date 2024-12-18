from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import ExchangeRate
from schemas.exchange_rates import ExchangeRateResponse

router = APIRouter()


@router.get(
    '/exchange-rates/',
    status_code=status.HTTP_200_OK,
    response_model=ExchangeRateResponse,
)
async def get_exchange_rates(db: Session = Depends(get_db)):
    '''
    Will return all stored rates
    '''

    today = datetime.combine(datetime.today().date(), datetime.min.time())

    exchange_rates = (
        db.query(ExchangeRate).filter(ExchangeRate.created_at > today).all()
    )

    return ExchangeRateResponse(rates=exchange_rates)
