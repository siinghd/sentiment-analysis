from django.core.exceptions import ImproperlyConfigured
import os

# This function is used to get environment variables
def get_env_variable(var_name, default=None):
    try:
        return os.environ[var_name]
    except KeyError:
        if default is None:
            error_msg = f"Set the {var_name} environment variable"
            raise ImproperlyConfigured(error_msg)
        return default