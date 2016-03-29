
@selenium
Feature: Home redirect
  In order to be able to choose the home page
  As a developer
  I want to be able to set a custom redirect when the user access the home page

  Scenario: default configuration for home page
    When I access the URL "/"
    Then The browser URL should be "/dashboard"
