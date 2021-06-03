from factory.handling.base_logging import BaseLogging as Log


class RunningException:
    @staticmethod
    def raise_assertion_error(custom_message, exception):
        message = Log.show_exception("   ", custom_message, exception)
        Log.error(message)
        raise AssertionError(message)

    @staticmethod
    def raise_exception_error(custom_message, exception):
        message = Log.show_exception("EXCEPTION: ", custom_message, exception)
        Log.error(message)
        raise Exception(message)
