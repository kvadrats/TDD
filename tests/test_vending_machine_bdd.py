import pytest
from pytest_bdd import when, given, then
from pytest_bdd.parsers import re
from pytest_bdd import scenario
from vending.machine import VendingMachine


@scenario("test_vending_machine_bdd.feature", "Test product count update after buying 1")
def test_product_count_change():
    pass

@pytest.fixture
def context_obj():
    return VendingMachine()


@given(re(r'A Stocked Vending Machine'))
def stock_vending_machine(context_obj):
    return context_obj


@when(re(r'user inserts a coin with nominal "(?P<nominal>.*)"'))
def insert_coin_n(context_obj, nominal):
    context_obj.insert_coin(float(nominal))
    return nominal


@when(re('user buys a product with name "(?P<product>\w*)"'))
def buy_p_product(context_obj, product):
    context_obj.buy_product(product)
    return product

@then(re('there should be (?P<amount>\d*) less snickers product in product stock'))
def relative_product_count_checkup(context_obj, amount):
    prev_amount = 10  # TODO: Make this relativeness work with proper data preparation in the given step.

    amount = int(amount)
    assert context_obj.products.get("snickers")[-1] == prev_amount-amount

