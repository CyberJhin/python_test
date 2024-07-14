def create_tables(cursor):
    create_tables_queries = [
        """
        CREATE TABLE IF NOT EXISTS credit_products (
            product_id SERIAL PRIMARY KEY,
            product_name TEXT,
            product_description TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            inn VARCHAR(12) UNIQUE,
            segment TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS credit_offers (
            offer_id SERIAL PRIMARY KEY,
            product_id INT,
            interest_rate FLOAT,
            conditions TEXT,
            FOREIGN KEY (product_id) REFERENCES credit_products(product_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS client_offers (
            client_id INT,
            product_id INT,
            offer_id INT,
            PRIMARY KEY (client_id, product_id),
            FOREIGN KEY (client_id) REFERENCES clients(client_id),
            FOREIGN KEY (product_id) REFERENCES credit_products(product_id),
            FOREIGN KEY (offer_id) REFERENCES credit_offers(offer_id)
        )
        """
    ]

    for query in create_tables_queries:
        cursor.execute(query)

def drop_tables(cursor):
    drop_tables_queries = [
        "DROP TABLE IF EXISTS client_offers",
        "DROP TABLE IF EXISTS clients",
        "DROP TABLE IF EXISTS credit_offers",
        "DROP TABLE IF EXISTS credit_products"
    ]
    for query in drop_tables_queries:
        cursor.execute(query)
