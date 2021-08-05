@login-sample
Feature: Automation Sample App

	Scenario: Login the user with its credentials
		Given that app is open at Login page
		When user provides their wrong credentials
		Then user sees "Wrong username or password"

