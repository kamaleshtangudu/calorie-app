# Error Code Mapping
# Note: message and code both are compulsory
ERROR_MAPPING = {
    'DEFAULT_ERROR': {
        'message': 'Something went wrong! Please try again later.',
        'code': 8999
    }
}


def get_error_message_and_code(key):
    return ERROR_MAPPING.get(key, ERROR_MAPPING['DEFAULT_ERROR'])


def get_error_message(key):
    error = get_error_message_and_code(key)
    return error['message']


def get_error_code(key):
    error = get_error_message_and_code(key)
    return error['code']
