from vending.machine import VendingMachine
import pytest


def test_product_count_change_after_buying():
    machine = VendingMachine()
    machine.insert_coin(2.0)
    machine.buy_product("snickers")

    assert machine.products.get("snickers")[-1] == 9


def test_buying_of_last_product_then_buying_again(capfd):
    product_count = 1
    machine = VendingMachine()
    machine.insert_coin(2)
    machine.add_product_to_list("coke", 1.5, product_count)
    machine.buy_product("coke")
    out, err = capfd.readouterr()
    assert "'coke' is not available" not in out

    machine.buy_product("coke")
    out, err = capfd.readouterr()
    assert "'coke' is not available" in out


def test_buying_of_nonexistant_product(capfd):
    machine = VendingMachine()
    machine.insert_coin(2)
    machine.buy_product("coke")

    out, err = capfd.readouterr()
    assert "'coke' is not available" in out


def test_update_product_list():
    machine = VendingMachine()
    # test standard adding the product to the list
    machine.add_product_to_list("coke", 100)
    assert "coke" in machine.products

    # test removal of an existing product from the list
    machine.remove_product_from_list("coke")
    assert "coke" not in machine.products

    # test adding a product that is already in the list (expected overwrite)
    machine.add_product_to_list("snickers", 1.5)
    assert machine.products["snickers"] == 1.5

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

