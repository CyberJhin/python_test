from db.connection import get_db_connection
from db.schema import create_tables, drop_tables
from db.data import populate_tables
from services.offers import select_best_offer

def main():
    conn = get_db_connection()
    cursor = conn.cursor()

    drop_tables(cursor)
    create_tables(cursor)
    populate_tables(cursor)
    conn.commit()

    # Пример использования функции
    client_inn = '123456789012'
    product_id = 1
    best_offer_id = select_best_offer(cursor, client_inn, product_id)
    print(f"The best offer ID for client with INN {client_inn} and product ID {product_id} is {best_offer_id}")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
