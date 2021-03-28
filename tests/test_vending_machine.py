from vending.machine import VendingMachine, fake_function, get_any_joke, get_joke
import pytest
from unittest.mock import patch, MagicMock


STATIC_JOKE = {
    "error": False,
    "category": "Pun",
    "type": "single",
    "joke": "How do you make holy water? You freeze it and drill holes in it.",
    "flags": {
        "nsfw": False,
        "religious": True,
        "political": False,
        "racist": False,
        "sexist": False,
        "explicit": False
    },
    "id": 203,
    "safe": False,
    "lang": "en"
}


def test_joke_api():
    static_joke_mock = MagicMock()
    static_joke_mock.return_value = STATIC_JOKE

    with patch("vending.machine.get_any_joke", static_joke_mock):
        joke_list = list()
        for i in range(10):
            joke = get_joke()
            joke_list.append(joke)

        for joke in joke_list:
            for joke_to_compare in joke_list:
                assert joke == joke_to_compare


def test_mocking_of_available_coins():
    new_available_coin_values = 3

    fake_coin_values = MagicMock()
    fake_coin_values.return_value = new_available_coin_values

    with patch('vending.machine.function_to_call', fake_coin_values):
        result = fake_function()
        assert result == new_available_coin_values


def test_product_count_change_after_buying():
    machine = VendingMachine()
    machine.insert_coin(2.0)
    machine.buy_product("snickers")

    assert machine.products.get("snickers")[-1] == 9


def test_buying_of_last_product_then_buying_again(capfd):
    product_count = 1
    machine = VendingMachine()
    machine.insert_coin(2)
    machine.insert_coin(2)
    machine.add_product_to_list("coke", product_count, 1.5)

    machine.buy_product("coke")
    out, err = capfd.readouterr()
    assert "'coke' is not available" not in out

    machine.buy_product("coke")
    out, err = capfd.readouterr()
    assert "'coke' is not available" in out


def test_add_a_product_with_no_price():
    machine = VendingMachine()
    with pytest.raises(Exception, match="You are trying to set the price of product to 0, which is not allowed"):
        machine.add_product_to_list("blabla", 5, 0.0)


def test_add_new_product_without_price():
    machine = VendingMachine()
    with pytest.raises(Exception, match="You are trying to add a new product, but not passing it's supposed price"):
        machine.add_product_to_list("blabla", 5)


def test_buying_of_nonexistant_product(capfd):
    machine = VendingMachine()
    machine.insert_coin(2)
    machine.buy_product("coke")

    out, err = capfd.readouterr()
    assert "'coke' is not available" in out


def test_restocking_of_existing_product():
    machine = VendingMachine()
    machine.add_product_to_list("mars", 5)

    # check if price remains the same as before restocking
    assert machine.products.get("mars")[0] == 1.3
    # check if 5 products have been added to existing 5 product stock
    assert machine.products.get("mars")[1] == 5+5


def test_restocking_of_existing_product_and_update_price():
    machine = VendingMachine()
    machine.add_product_to_list("mars", 5, 1.2)

    # check if price has been set to the new one: 1.2
    assert machine.products.get("mars")[0] == 1.2
    # check if 5 products have been added to existing 5 product stock
    assert machine.products.get("mars")[1] == 5+5


def test_update_product_list():
    machine = VendingMachine()
    # test standard adding the product to the list
    machine.add_product_to_list("coke", 5, 100)
    assert "coke" in machine.products

    # test removal of an existing product from the list
    machine.remove_product_from_list("coke")
    assert "coke" not in machine.products

    # test adding a product that is already in the list (expected overwrite)
    machine.add_product_to_list("snickers", 5, 1.5)
    assert machine.products["snickers"][0] == 1.5

    # test removing of product that doesn't exist
    with pytest.raises(Exception, match="No product found with name 'you'"):
        machine.remove_product_from_list("you")


def test_fake_coin(capfd):
    machine = VendingMachine()
    assert machine.insert_coin(5) == 5
    out, err = capfd.readouterr()
    assert "Coin type not accepted" in out


def test_buy_product_and_get_remainder():
    # snickers price = 1.2
    machine = VendingMachine()
    machine.insert_coin(1)
    machine.insert_coin(0.05)
    machine.insert_coin(0.5)

    money, product = machine.buy_product("snickers")
    assert machine.truncate(sum(money)) == 0.35
    assert product == "snickers"


def test_buy_nonexisting_product(capfd):
    machine = VendingMachine()
    machine.insert_coin(1)
    machine.insert_coin(0.05)
    machine.insert_coin(0.5)

    money, product = machine.buy_product("machine itself")
    assert 1.55 == sum(money)
    out, err = capfd.readouterr()
    assert product is None
    assert "'machine itself' is not available" in out


def test_get_money_back():
    machine = VendingMachine()
    machine.insert_coin(1)
    machine.insert_coin(0.05)
    machine.insert_coin(0.5)
    deposit = machine.get_deposit_back()

    assert len(deposit) == 3
    assert set(deposit) == set([1, 0.05, 0.5])

