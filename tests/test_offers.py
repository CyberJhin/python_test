import unittest
from db.connection import get_db_connection
from db.schema import create_tables, drop_tables
from db.data import populate_tables
from services.offers import select_best_offer

class TestCreditOffers(unittest.TestCase):
    def setUp(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        drop_tables(self.cursor)
        create_tables(self.cursor)
        populate_tables(self.cursor)
        self.conn.commit()

    def tearDown(self):
        self.conn.rollback()
        self.cursor.close()
        self.conn.close()

    def test_select_best_offer_no_offers(self):
        """Тест для клиента, у которого нет предложений по продукту"""
        best_offer_id = select_best_offer(self.cursor, '123456789012', 999)
        self.assertIsNone(best_offer_id, "Не должно быть предложений для несуществующего продукта")

    def test_select_best_offer_single_offer(self):
        """Тест для клиента, у которого одно предложение по продукту"""
        # Добавим одно предложение для несуществующего продукта
        self.cursor.execute("""
            INSERT INTO credit_offers (product_id, interest_rate, conditions)
            VALUES (999, 5.0, 'Годовая ставка 5.0% на срок 1 год')
        """)
        self.conn.commit()

        best_offer_id = select_best_offer(self.cursor, '123456789012', 999)
        self.assertIsNotNone(best_offer_id, "Должно быть предложение для продукта 999")

    def test_select_best_offer_multiple_offers(self):
        """Тест для клиента, у которого несколько предложений по продукту, и выбирается лучшее"""
        # Добавим несколько предложений для несуществующего продукта
        offers = [
            (999, 5.0, 'Годовая ставка 5.0% на срок 1 год'),
            (999, 4.0, 'Годовая ставка 4.0% на срок 2 года'),
            (999, 3.5, 'Годовая ставка 3.5% на срок 3 года')
        ]
        self.cursor.executemany("""
            INSERT INTO credit_offers (product_id, interest_rate, conditions)
            VALUES (%s, %s, %s)
        """, offers)
        self.conn.commit()

        best_offer_id = select_best_offer(self.cursor, '123456789012', 999)
        self.cursor.execute("SELECT interest_rate FROM credit_offers WHERE offer_id = %s", (best_offer_id,))
        best_rate = self.cursor.fetchone()[0]
        self.assertEqual(best_rate, 3.5, "Лучшее предложение должно иметь наименьшую процентную ставку")

    def test_select_best_offer_no_duplicates(self):
        """Тест для клиента, чтобы убедиться, что функция не добавляет дубликатов"""
        # Выберем лучшее предложение для клиента
        best_offer_id = select_best_offer(self.cursor, '123456789012', 1)
        self.assertEqual(best_offer_id, 2, "Лучшее предложение должно быть с offer_id 2")

        # Попробуем добавить такое же предложение снова
        duplicate_offer_id = select_best_offer(self.cursor, '123456789012', 1)
        self.assertEqual(duplicate_offer_id, 2, "Функция не должна добавлять дубликаты")

        # Проверим, что в таблице client_offers только одна запись для данного клиента и продукта
        self.cursor.execute("""
            SELECT COUNT(*) FROM client_offers
            WHERE client_id = (SELECT client_id FROM clients WHERE inn = '123456789012') AND product_id = 1
        """)
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1, "Должна быть только одна запись для клиента и продукта")

    def test_select_best_offer_multiple_products(self):
        """Тест для клиента, у которого есть несколько предложений по разным продуктам"""
        # Выберем лучшее предложение для первого продукта
        best_offer_id1 = select_best_offer(self.cursor, '123456789012', 1)
        self.assertEqual(best_offer_id1, 2, "Лучшее предложение для продукта 1 должно быть с offer_id 2")

        # Выберем лучшее предложение для второго продукта
        best_offer_id2 = select_best_offer(self.cursor, '123456789012', 2)
        self.assertEqual(best_offer_id2, 4, "Лучшее предложение для продукта 2 должно быть с offer_id 4")

        # Проверим, что оба предложения добавлены в таблицу client_offers
        self.cursor.execute("""
            SELECT offer_id FROM client_offers
            WHERE client_id = (SELECT client_id FROM clients WHERE inn = '123456789012')
        """)
        offers = self.cursor.fetchall()
        self.assertEqual(len(offers), 2, "Должны быть добавлены два предложения для клиента")
        self.assertIn((2,), offers, "Предложение с offer_id 2 должно быть добавлено")
        self.assertIn((4,), offers, "Предложение с offer_id 4 должно быть добавлено")

if __name__ == '__main__':
    unittest.main()
