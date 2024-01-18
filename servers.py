#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List
from abc import ABC, abstractmethod
import re

class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)

    def __init__(self, name: str, price: int | float) -> None:
        if not isinstance(name, str) or not isinstance(price, (int, float)):
            raise ValueError
        elif re.fullmatch(r"\b[a-zA-Z]+[0-9]+\b", name) is None:
            raise ValueError
        else:
            self.name = name
            self.price = price

    def get_price(self) -> float:
        return self.price

    def get_name(self) -> str:
        return self.name

    def __eq__(self, other):
        return self.price == other.price and self.name == other.name  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, msg=None):
        if msg is None:
        # Ustaw domys´lny uz˙yteczny (!) komunikat
            msg = f"Too many products"
        super().__init__(msg) # wywołanie konstruktora klasy 'Exception'

class Serwer(ABC):

    @abstractmethod
    def get_products(self) -> List[Product]:
        pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer:
    n_max_returned_entries = 5

    def __init__(self, product_list: List[Product]) -> None:
        self.products = product_list

    def get_entries(self,n_letters=1) -> List[Product]:
        ret_list = [prod for prod in self.products if re.fullmatch('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), prod.get_name())]
        if len(ret_list) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(ret_list, key=lambda prod: prod.get_price())



class MapServer:
    n_max_returned_entries = 5

    def __init__(self, product_list: List[Product]) -> None:
        self.products = {elem.get_name():elem.get_price() for elem in product_list}

    def get_entries(self,n_letters=1) -> List[Product]:
        ret_list = [Product(name, price) for name, price in self.products.items() if re.fullmatch('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), name)]
        if len(ret_list) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(ret_list, key=lambda prod: prod.get_price())


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server: ListServer | MapServer) -> None:
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
       try:
            list_of_entries = [prod.get_price() for prod in self.server.get_entries(n_letters)]
            if not list_of_entries:
                raise Exception("Empty list")
            else:
             return sum(list_of_entries)
       except:
           return None

