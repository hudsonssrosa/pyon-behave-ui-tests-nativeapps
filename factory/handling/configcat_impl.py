import configcatclient
from configcatclient.user import User
from factory.base_context import BaseContext as Bctx
from factory.handling.base_logging import BaseLogging as Log


class ConfigCat:
    @staticmethod
    def get_runtime_sdk_key():
        environment = Bctx.flag_environment.get()
        sdk_keys_switcher = {
            "dev": Bctx.configcat_sdk_key_ff_dev.get(),
            "staging": Bctx.configcat_sdk_key_ff_staging.get(),
            "production": Bctx.configcat_sdk_key_ff_production.get(),
        }
        ff_environment_set = sdk_keys_switcher.get(
            environment, lambda: "Invalid environment SDK Key"
        )
        return ff_environment_set

    @staticmethod
    def create_client(sdk_key=""):
        return configcatclient.create_client(str(sdk_key))

    @staticmethod
    def get_feature_flag(fflag_name="", fflag_state=False, email_address=None):
        user = f"pyon-ff-{Bctx.random_data.get()}"
        configcat_client_environment = ConfigCat.create_client(
            sdk_key=ConfigCat.get_runtime_sdk_key()
        )
        cc_tuple = (
            (fflag_name, fflag_state, User(user, email=email_address))
            if email_address is not None
            else (fflag_name, fflag_state)
        )
        fflag_read = configcat_client_environment.get_value(*cc_tuple)
        Log.info(
            f"ConfigCat's Feature Flag '{fflag_name}' expected as '{fflag_state}' for user '{email_address}' returned '{str(fflag_read).upper()}'"
        )
        return fflag_read
