import math


class VendingMachine:
    """
    An imaginary class to simulate the behavior of a vending machine,
    simulating all real life vending machine actions, except product count
    """

    def __init__(self):
        self.products = {
            "snickers": 1.2,
            "mars": 1.3,
            "twix": 1
        }  # TODO: add available product count for properly simulating vending machine
        self.deposit = []
        self.accepted_coins = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0]

    def insert_coin(self, coin):
        """
        This method simulates a user inserting a coin into the vending machine,
        it will add the coin to the total amount of deposited coins
        :param coin: integer or float
        :return: if coin type is not accepted, it returns the coin, else None
        """

        if coin in self.accepted_coins:
            self.deposit.append(coin)
        else:
            print("Coin type not accepted")
            return coin

    def get_deposit_back(self):
        """
        Get all your deposited coins back, usually a giant red button on vending machine
        if you have inserted your money and decide that you don't want anything from the
        vending machine
        :return: a list of coins (the total amount of money you previously inserted)
        """

        requested_sum = self.deposit
        self.deposit = []
        return requested_sum

    def buy_product(self, product):
        """
        This is a method that simulates the buying of a product, if you have inserted enough money,
        it will return the product and the reminder of money
        :param product: str, must be a product that is present in self.products
        :return: the product and reminder of money if any left over
        """

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
        """
        This is an internal helper method, to help calculating how much change
        needs to be returned after buying a product, this is calculated for
        coins instead of sum of the money, to understand what exact coins need
        to be used.
        :param remainder: value of inserted money into vending machine
        :param change: list of coins
        :return: list of coins
        """
        for coin in reversed(self.accepted_coins):
            if (remainder - coin) >= 0:
                remainder = self.truncate(remainder - coin)
                change.append(coin)
        if remainder > 0:
            self._calc_change(remainder, change)
        return change

    @staticmethod
    def truncate(n, decimals=2):
        """
        This is a helper method to help with rounding during math operations,
        this is used because python builtin float handling is approximate and will not give
        precise results, so after math operations we want to round to round numbers.
        :param n: number that we want to round
        :param decimals: how many decimal sign
        :return: rounded number
        """
        multiplier = 10 ** decimals
        return math.floor(n * multiplier + 0.5) / multiplier

    def add_product_to_list(self, new_product_name, price):
        """
        Simulating an action that a maintenance person would do on a real live
        vending machine, this action adds a product to the available products list
        and sets its price
        :param new_product_name: name as a string of the product, e.g. snickers, twix...
        :param price: price in as either float or integer
        :return: The updated products list
        """
        new_product_name = new_product_name.lower()
        self.products.update({new_product_name: price})

        return self.products

    def remove_product_from_list(self, product_name):
        """
        Remove an existing product from product list.
        :param product_name: str, a product added from VendingMachine.__init__ or has been added by add_product_to_list
        :return: None or raised Exception
        """

        product_name = product_name.lower()
        if product_name in self.products:
            del self.products[product_name]
        else:
            raise Exception(f"No product found with name '{product_name}'")
