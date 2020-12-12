import math
from unittest import mock


class VendingMachine:
    def __init__(self):
        self.products = {
            "snickers": 1.2,
            "mars": 1.3,
            "twix": 1
        }
        self.deposit = []
        self.accepted_coins = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0]

    def insert_coin(self, coin):

        if coin in self.accepted_coins:
            self.deposit.append(coin)
        else:
            print("Coin type not accepted")
            return coin

    def get_deposit_back(self):

        requested_sum = self.deposit
        self.deposit = []
        return requested_sum

    def buy_product(self, product):

        product = product.lower()
        if self.products.get(product, None) is not None:
            if (sum(self.deposit) - self.products[product]) >= 0:
                change_sum = self.truncate((sum(self.deposit) - self.products[product]))
                change = self._calc_change(change_sum, list())
                return change, product
        else:
            print(f"'{product}' is not available")
            return self.deposit, None

    def _calc_change(self, remainder, change):
        for coin in reversed(self.accepted_coins):
            if (remainder - coin) >= 0:
                remainder = self.truncate(remainder - coin)
                change.append(coin)
        if remainder > 0:
            self._calc_change(remainder, change)
        return change

    @staticmethod
    def truncate(n, decimals=2):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier + 0.5) / multiplier

    def add_product_to_list(self, new_product_name, price):
        new_product_name = new_product_name.lower()
        self.products.update({new_product_name: price})

        return self.products

    def remove_product_from_list(self, product_name):
        """

        :param product_name:
        :return:
        """

        product_name = product_name.lower()
        if product_name in self.products:
            del self.products[product_name]
        else:
            raise Exception(f"No product found with name '{product_name}'")

