def populate_tables(cursor):
    credit_products_data = [
        ("Бизнес-кредит", "Кредит для бизнеса с гибкими условиями"),
        ("Микрокредит", "Кредит для малого бизнеса"),
        ("Ипотека", "Кредит на покупку недвижимости")
    ]

    clients_data = [
        ("123456789012", "Крупный бизнес"),
        ("987654321098", "Малый бизнес"),
        ("456789123456", "Средний бизнес")
    ]

    credit_offers_data = [
        (1, 10.5, "Годовая ставка 10.5% на срок 5 лет"),
        (1, 9.0, "Годовая ставка 9.0% на срок 3 года"),
        (2, 15.0, "Годовая ставка 15.0% на срок 1 год"),
        (2, 12.5, "Годовая ставка 12.5% на срок 2 года"),
        (3, 7.0, "Годовая ставка 7.0% на срок 10 лет")
    ]

    insert_credit_products_query = """
        INSERT INTO credit_products (product_name, product_description)
        VALUES (%s, %s)
    """
    cursor.executemany(insert_credit_products_query, credit_products_data)

    insert_clients_query = """
        INSERT INTO clients (inn, segment)
        VALUES (%s, %s)
    """
    cursor.executemany(insert_clients_query, clients_data)

    insert_credit_offers_query = """
        INSERT INTO credit_offers (product_id, interest_rate, conditions)
        VALUES (%s, %s, %s)
    """
    cursor.executemany(insert_credit_offers_query, credit_offers_data)
