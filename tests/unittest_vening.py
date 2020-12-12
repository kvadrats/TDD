import unittest
from vending.machine import VendingMachine


class TestVendingMachine(unittest.TestCase):
    def test_insert_coin(self):
        self.machine = VendingMachine()
        input_output = [1, 2, 3]

        for coin in input_output:
            self.machine.insert_coin(coin)

        self.assertEqual(self.machine.deposit, input_output)

        assert self.machine.deposit == input_output

    def test_product_refill(self):
        self.machine = VendingMachine()
        self.machine.remove_product_from_list("snickers")
        with self.assertRaises(Exception):
            self.machine.remove_product_from_list("jkhsejkhf sjdhf")

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
