from behave import *
from features.pages.wikipedia_sample.home_page import HomePage


home_page = HomePage(object)


@given('that app is open at Home page')
def step_given_that_app_is_open_at_home_page(context):
    # Add any preparation code for the app here
    pass


@when('user types "{text_to_search}"')
def step_when_user_types_text_to_search(context, text_to_search):
    home_page.type_input_search(text_to_search)


@then('the content related is found')
def step_then_the_content_related_is_found(context):
    # Add any validation for the app here
    pass
