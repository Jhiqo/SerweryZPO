#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError
from collections import Counter

server_types = (ListServer, MapServer)

class ProductTests(unittest.TestCase):
    def test_create_product_with_good_parameters(self):
        product_1 = Product("TEST321", 12.34)
        product_2 = Product("Ab01", 04.55)

        self.assertEqual(Product("TEST321", 12.34), product_1)
        self.assertEqual(Product("Ab01", 04.55), product_2)

    def test_create_product_with_bad_parameters(self):

        with self.assertRaises(ValueError):
            Product("", 12.34)

        with self.assertRaises(ValueError):
            Product("123", 12.34)

        with self.assertRaises(ValueError):
            Product("abc", 12.34)

        with self.assertRaises(ValueError):
            Product("123abc", 12.34)

        # with self.assertRaises(ValueError):
        #     Product("aBc123", -1)

        # with self.assertRaises(ValueError):
        #     Product("aBc123", 0)

        with self.assertRaises(ValueError):
            Product("aBc123", "Test")

        with self.assertRaises(ValueError):
            Product(None, None)

class ClientTests(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_exception(self):
        products_1 = [Product('AB121', 1), Product('BC3', 2.2)]
        products_2 = [Product('AB12', 1), Product('BC14', 2), Product('DE171', 3), Product('YZ789', 4),
                      Product('WT23', 5), Product('AA132', 6), Product('BB222', 6), Product('CC333', 8),
                      Product('CC333', 9), Product('DD444', 10), Product('EE555', 11),]

        for server_type in server_types:
            server = server_type(products_1)
            client1 = Client(server)
            total_price = client1.get_total_price(4)
            self.assertIsNone(total_price)

        for server_type in server_types:
            server = server_type(products_2)
            client2 = Client(server)
            total_price = client2.get_total_price(2)
            self.assertIsNone(total_price)


class ServerTest(unittest.TestCase):
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_returned_list_empty(self):
        product = [Product('A123', 1)]

        for server_type in server_types:
            server = server_type(product)
            entries = server.get_entries(2)
            self.assertEqual([], entries)

    def test_returned_list_sorted(self):
        products = [Product('BB22', 3), Product('AA111', 1), Product('CC333', 5), Product('DD44', 7)]
        good_order = [Product('AA111', 1), Product('BB22', 3), Product('CC333', 5), Product('DD44', 7)]

        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(entries, good_order)

    def test_exception_max_entries(self):
        products = [Product('AA11', 1), Product('BB22', 2), Product('CC33', 3), Product('DD44', 4),
                    Product('EE55', 5), Product('FF66', 6), Product('GG77', 7), Product('HH88', 8),
                    Product('II99', 9), Product('JJ1010', 10), Product('KK1111', 11)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                entries = server.get_entries(2)


if __name__ == '__main__':
    unittest.main()

