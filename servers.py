#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List
from abc import ABC, abstractmethod

class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)

    def __init__(self, name: str, price: float):
        letter = False
        number = False
        for sign in name:
            try:
                int(sign)
                if not letter:
                    raise ValueError()
                number = True
            except ValueError:
                if number:
                    raise ValueError()
                letter = True
        if letter and number:
            self.name = name
            self.price = price
        else:
            raise ValueError()

    def __eq__(self, other):
        return isinstance(self, other) and self.price == other.price and self.name == other.name  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass

class Serwer(ABC):

    @abstractmethod
    def get_products(self) -> List[Product]:
        pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer:
    def __int__(self, products: List[Product]):
        super().__init__()
        self.products = products

    def get_products(self) -> List[Product]:
        return self.products



class MapServer:
    def __init__(self, products: List[Product]):
        dict_products = {}
        for product in products:
            dict_products[product.name] = product
        self.products = dict_products

    def get_products(self) -> List[Product]:
        list_of_products = []
        for product in self.products.values():
            list_of_products.append(product)
        return list_of_products


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()

