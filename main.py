import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from models import create_tables, Publisher, Book, Sale, Stock, Shop


DNS = 'postgresql://postgres:12345@localhost:5432/sqlalchemy_db'
engine = sqlalchemy.create_engine(DNS)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

def filling_test_data():
    with open('test_data.json') as f:
        json_data = json.load(f)

    for data in json_data:
        if data['model'] == 'publisher':
            a = Publisher(id = data['pk'], name = data['fields']['name'])
        elif data['model'] == 'book':
            a = Book(id = data['pk'], title = data['fields']['title'], id_publisher = data['fields']['id_publisher'])
        elif data['model'] == 'shop':
            a = Shop(id = data['pk'], name = data['fields']['name'])
        elif data['model'] == 'stock':
            a = Stock(id = data['pk'], id_shop = data['fields']['id_shop'], id_book = data['fields']['id_book'], count = data['fields']['count'])
        elif data['model'] == 'sale':
            a = Sale(id = data['pk'], price = data['fields']['price'], date_sale = data['fields']['date_sale'], count = data['fields']['count'], id_stock = data['fields']['id_stock'])
        session.add(a)
        session.commit()
filling_test_data()

def get_publisher_shops(publisher):
    query = session.query(Shop)
    query = query.join(Stock)
    query = query.join(Book)
    query = query.join(Publisher)
    if publisher.isdigit():
        query = query.filter(Publisher.id == publisher).all()
    else:
        query = query.filter(Publisher.name == publisher).all()
    if query:
        for record in query:
            print(record)
    else:
        print(f'Издатель ({publisher}) не найден')

get_publisher_shops(input(f'Введите имя или id издателя: '))


session.close()