@demo-wikipedia
Feature: Wikipedia content searching

	Scenario: Searching in the Wikipedia
		Given that app is open at Home page
		When user types "Software Testing"
		Then the content related is found