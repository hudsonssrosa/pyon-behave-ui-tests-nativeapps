from driver_wrappers.appium.native_app_wrapper import BaseAppPage
from appium.webdriver.common.mobileby import MobileBy as MBy


class HomePage(BaseAppPage):
    loc_input_search_on_click = (MBy.ID, 'org.wikipedia.alpha:id/search_container')
    loc_input_search = (MBy.ID, 'org.wikipedia.alpha:id/search_src_text')

    def type_input_search(self, text_to_search):
        self.wait_for_element(*self.loc_input_search_on_click)
        self.click_on(*self.loc_input_search_on_click)
        self.wait_for_element(*self.loc_input_search)
        self.click_on(*self.loc_input_search)
        self.type_text(text_to_search, *self.loc_input_search)
