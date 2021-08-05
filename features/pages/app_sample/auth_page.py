from driver_wrappers.appium.native_app_wrapper import BaseAppPage
from appium.webdriver.common.mobileby import MobileBy as MBy


class AuthPage(BaseAppPage):
    loc_txt_username = (MBy.ID, 'com.dgotlieb.automationsample:id/userName')
    loc_txt_password = (MBy.ID, 'com.dgotlieb.automationsample:id/userPassword')
    loc_btn_login = (MBy.ID, 'com.dgotlieb.automationsample:id/loginButton')
    loc_lbl_error_message = (MBy.ID, 'com.dgotlieb.automationsample:id/errorTV')
        
    def type_input_username(self, input_value):
        self.wait_for_element(*self.loc_txt_username)
        self.click_on(*self.loc_txt_username)
        self.type_text(input_value, *self.loc_txt_username)
        return self

    def type_input_password(self, input_value):
        self.wait_for_element(*self.loc_txt_password)
        self.click_on(*self.loc_txt_password)
        self.type_text(input_value, *self.loc_txt_password)
        return self

    def click_on_login(self):
        self.click_on(*self.loc_btn_login)
        return self

    def validate_error_message(self, message):
        message_found = self.get_element_text(*self.loc_lbl_error_message)
        self.assert_that(message_found).contains_the(value_expected=message, optional_description="Login validation message")
        return self
