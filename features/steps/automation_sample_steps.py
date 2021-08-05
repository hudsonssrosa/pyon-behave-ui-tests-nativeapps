from behave import *
from features.pages.app_sample.auth_page import AuthPage


login_page = AuthPage(object)


@given('that app is open at Login page')
def step_given_that_app_is_open_at_login_page(context):
    pass


@when('user provides their wrong credentials')
def step_when_user_types_text_to_search(context):
    (
        login_page.type_input_username("wrong_user_name")
        .type_input_password("wrong_pass_123")
    )


@then('user sees "{error}"')
def step_then_the_content_related_is_found(context, error):
    login_page.validate_error_message(message=error)
