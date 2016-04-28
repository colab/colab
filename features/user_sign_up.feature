
Feature: User Sign Up
    In order to use the system
    As an User
    I want to be able to sign up

    Scenario: Sign up with no information
        When I access the URL "/"
        When I click in "Acesso "
        When I click in "Register"
        When I click in "Register" button
        Then The field "id_username" should have an error
        Then The field "id_first_name" should have an error
        Then The field "id_last_name" should have an error
        Then The field "id_email" should have an error
        Then The field "id_password1" should have an error
        Then The field "id_password2" should have an error

    Scenario: Sign up with all required information
        When I access the URL "/"
        When I click in "Acesso "
        When I click in "Register"
        When I fill "johndiehard" in "id_username" field
        When I fill "John" in "id_first_name" field
        When I fill "McClane" in "id_last_name" field
        When I fill "john@email.com" in "id_email" field
        When I fill "100guns100" in "id_password1" field
        When I fill "100guns100" in "id_password2" field
        When I click in "Register" button
        Then The browser URL should be "/account/johndiehard"
        Then I should see "John McClane" in "user-profile"

    Scenario: Sign up with invalid email
        When I access the URL "/"
        When I click in "Acesso "
        When I click in "Register"
        When I fill "johndiehard" in "id_username" field
        When I fill "John" in "id_first_name" field
        When I fill "McClane" in "id_last_name" field
        When I fill "john@email" in "id_email" field
        When I fill "100guns100" in "id_password1" field
        When I fill "100guns100" in "id_password2" field
        When I click in "Register" button
        Then The field "id_email" should have an error

    Scenario: Sign up with different passwords
        When I access the URL "/"
        When I click in "Acesso "
        When I click in "Register"
        When I fill "johndiehard" in "id_username" field
        When I fill "John" in "id_first_name" field
        When I fill "McClane" in "id_last_name" field
        When I fill "john@email.com" in "id_email" field
        When I fill "100guns100" in "id_password1" field
        When I fill "100guns999" in "id_password2" field
        When I click in "Register" button
        Then The field "id_password2" should have an error
