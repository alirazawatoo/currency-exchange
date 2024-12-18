from utils.exchange_rate import fetch_and_store_exchange_rates

def seed_data():
    print('====Seeding Data======')
    fetch_and_store_exchange_rates()
    print('====Data Seeded=======')


if __name__ == '__main__':
    seed_data()