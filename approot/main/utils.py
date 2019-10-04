from flask import url_for, current_app

def get_symbol(value):
    if value == True:
        symbol_value = u'\u2714'
    else:
        symbol_value = u'\u2717'
    return symbol_value
