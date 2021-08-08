# Created by emils at 8/8/2021
Feature: # Enter feature name here
  # Enter feature description here

  Scenario: Test product count update after buying 1
    Given A Stocked Vending Machine
    When user inserts a coin with nominal "2.0"
    And user buys a product with name "snickers"
    Then there should be 1 less snickers product in product stock