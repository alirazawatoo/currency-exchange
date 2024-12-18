from xml.etree import ElementTree as ET

import requests
from sqlalchemy import desc
from sqlalchemy.orm import Session

from database import get_db
from models.exchange_rate import ExchangeRate

from .constants import ECB_API_URL


def fetch_and_store_exchange_rates():
    rates = fetch_exchange_rates()
    insert_into_db(get_db(), rates)


def fetch_exchange_rates() -> dict:
    '''
    Fetches exchange rates from API and returns in dict form
    '''
    response = requests.get(ECB_API_URL)
    if response.status_code != 200:
        raise Exception('Failed to fetch data from ECB')

    root = ET.fromstring(response.content)
    rates = {}

    for cube in root.findall('.//{*}Cube[@time]'):
        for currency in cube.findall('.//{*}Cube[@currency]'):
            rates[currency.attrib['currency']] = float(currency.attrib['rate'])

    return rates


def insert_into_db(db: Session, rates: dict):
    db = next(db)
    for currency, rate in rates.items():
        latest_exchange_rate = (
            db.query(ExchangeRate)
            .filter_by(currency=currency)
            .order_by(desc(ExchangeRate.created_at))
            .first()
        )
        change = (
            rate - latest_exchange_rate.rate if latest_exchange_rate else None
        )
        exchange_rate = ExchangeRate(
            currency=currency, rate=rate, change=change
        )
        db.add(exchange_rate)
        db.commit()
