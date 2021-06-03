from driver_wrappers.appium.native_app_wrapper import BaseAppPage
from factory.handling.configcat_impl import ConfigCat

ff_phone_number = "show_contact_phone_number"
ff_admin_jwt_auth = "admin_jwt_auth"
ff_modifying_hire_agreement_generation = "enable_modifying_hire_agreement_generation"
ff_new_agreement_generation = "enable_new_agreement_generation"
ff_new_dlg_multipliers = "enable_new_dlg_multipliers"
ff_subscription_service = "enable_subscription_service"
ff_group_durations_in_filter = "group_durations_in_filter"
ff_increase_number_of_vehicle_images = "increase_number_of_vehicle_images"
ff_max_delivery_available_days = "max_delivery_available_days"
ff_max_pickup_available_days = "max_pickup_available_days"
ff_new_shorten_and_cancel = "new_shorten_and_cancel"
ff_referral_emails_via_crm = "referral_emails_via_crm"
ff_consumer_api = "consumer_api"
ff_additional_drivers_page = "additional_drivers_page"
ff_agreement_page = "agreement_page"
ff_delivery_page = "delivery_page"
ff_insurance_page = "insurance_page"
ff_payment_page = "payment_page"
ff_sample_page = "sample_page"


class FeatureFlagStep(BaseAppPage):
    """
    Use this class in the scenario steps to separate feature flags from application reducing the complexity
    in use a same scenario to recognise when a feature flag from ConfigCat should be activated or deactivated,
    regardless if a user is informed or not. To see further information about ConfigCat client implementation,
    get this link:

        https://configcat.com/docs/sdk-reference/python/

    In this class, implement a method responsible to verify what is the implementation to be executed according the
    ConfigCat Feature Flag read. For this, consider the following implementation:

        @staticmethod
        def enable_<my_new_feature_flag_name>():
            ff_<my_new_feature_flag_name> = ConfigCat.get_feature_flag(
                    fflag_name=ConfigCat.fflag["ff_<feature_flag_name>"], fflag_state=True, email_address="ui.tests.ff"
                )
            if ff_<my_new_feature_flag_name>:
                # [IMPLEMENT THE LOGIC FOR NEW FF HERE]
            else:
                # [IMPLEMENT THE OLD LOGIC HERE]


        In the scenario steps, import this class and call the method such as the sample below:

            from features.steps.feature_flags.new_feature_flags import FeatureFlagStep as FFlagStep

            # [... Your step code ...]
            ff_<my_new_feature_flag_name>_page = FFlagStep.new_<my_new_feature_flag_name>(email_address="ui.tests.ff")

    :return:
    """

    @staticmethod
    def new_feature_page(email):
        return ConfigCat.get_feature_flag(ff_sample_page, fflag_state=True, email_address=email)
