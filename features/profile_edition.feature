
Feature: User Profile Edition
    In order to update my personal information
    As an User
    I want to be able to edit my profile

    Background:
        Given I am logged in as "john"

    Scenario: Edit profile without required information
        When I open the user menu
        When I click in "My Profile"
        When I click in "Edit Profile"
        When I fill " " in "id_first_name" field
        When I fill " " in "id_last_name" field
        When I click in "Update" button
        Then The field "id_first_name" should have an error
        Then The field "id_last_name" should have an error

    Scenario: Edit profile with valid information
        When I open the user menu
        When I click in "My Profile"
        When I click in "Edit Profile"
        When I fill "John" in "id_first_name" field
        When I fill "McClaine" in "id_last_name" field
        When I fill "Die Hard" in "id_institution" field
        When I fill "police officer" in "id_role" field
        When I fill "diehard.com" in "id_webpage" field
        When I fill "I am tough." in "id_bio" field
        When I click in "Update" button
        Then I should see "John McClaine" in "user-profile"
        Then I should see "Die Hard" in "user-profile"
        Then I should see "police officer" in "user-profile"
        Then I should see "I am tough." in "user-profile"
        When I click in "Edit Profile"
        Then I should see "diehard.com" in "id_webpage"

    Scenario: Change password with wrong current password
        When I open the user menu
        When I click in "My Profile"
        When I click in "Edit Profile"
        When I click in "Change Password"
        When I fill "wrong" in "id_old_password" field
        When I fill "newpassword" in "id_new_password1" field
        When I fill "newpassword" in "id_new_password2" field
        When I click in "Change my password" button
        Then The field "id_old_password" should have an error

    Scenario: Change password with wrong password confirmation
        When I open the user menu
        When I click in "My Profile"
        When I click in "Edit Profile"
        When I click in "Change Password"
        When I fill "john" in "id_old_password" field
        When I fill "newpassword" in "id_new_password1" field
        When I fill "differentpassword" in "id_new_password2" field
        When I click in "Change my password" button
        Then The field "id_new_password2" should have an error

    Scenario: Change password with success
        When I open the user menu
        When I click in "My Profile"
        When I click in "Edit Profile"
        When I click in "Change Password"
        When I fill "john" in "id_old_password" field
        When I fill "newpassword" in "id_new_password1" field
        When I fill "newpassword" in "id_new_password2" field
        When I click in "Change my password" button
        When I open the user menu
        When I click in "My Profile"
        When I open the user menu
        When I click in "Logout"
        When I click in "Acesso "
        When I click in "Login"
        When I fill "john" in "id_username" field
        When I fill "newpassword" in "id_password" field
        When I click in "Acesso "
        When I click in "Login" button
        Then The browser URL should be "/dashboard"
