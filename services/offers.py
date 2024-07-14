def select_best_offer(cursor, client_inn, product_id):
    select_client_query = """
        SELECT client_id FROM clients WHERE inn = %s
    """
    cursor.execute(select_client_query, (client_inn,))
    client_id = cursor.fetchone()[0]

    select_offers_query = """
        SELECT offer_id, interest_rate FROM credit_offers
        WHERE product_id = %s
        ORDER BY interest_rate ASC
        LIMIT 1
    """
    cursor.execute(select_offers_query, (product_id,))
    best_offer = cursor.fetchone()

    if best_offer:
        offer_id = best_offer[0]
        insert_client_offer_query = """
            INSERT INTO client_offers (client_id, product_id, offer_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (client_id, product_id) DO NOTHING
        """
        cursor.execute(insert_client_offer_query, (client_id, product_id, offer_id))
        return offer_id
    return None
