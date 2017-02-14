# -*- coding: utf-8 -*-


def encode(text):
    """encode text to CP1252"""
    if not isinstance(text, unicode):
        try:
            u = text.decode('utf8')
        except UnicodeDecodeError:
            u = text.decode('latin1')
        except UnicodeDecodeError:
            u = text.decode('CP1252')
    else:
        u = text
    text_cp1252 = u.encode('CP1252')
    return text_cp1252

def language(datatype):

    import ctypes
    import locale
    windll = ctypes.windll.kernel32
    language = str(windll.GetUserDefaultUILanguage())

    if datatype == 'string':
        if language == 'de_DE':
            return u'Zeichenfolge'
        else:
            return u'String'


    if datatype == 'boolean':
        if language == 'de_DE':
            return u'Boolesch'
        else:
            return u'Boolean'
        if datatype == 'Zeichenfolge':
            return 'String'

