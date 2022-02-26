from django.db.models import CharField, TextField

"""
set of utilities to use in apps
"""

maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))


def normalize_text(input_str):
    """
    function to change farsi charecters to standard form.
    :param input_str
    :return: a standard string
    """
    translation = maketrans(u'٤٥٦كي؛٪۱١۲٢۳٣۴۵۶۷٧۸٨۹٩۰٠', u'456کی;%11223345677889900')
    try:
        return input_str.strip().translate(translation)
    except:
        return input_str


def normalize_num(input_str):
    """
    function to change farsi charecters to standard form.
    :param input_str
    :return: a standard string
    """
    translation = maketrans(u'٤٥٦۱١۲٢۳٣۴۵۶۷٧۸٨۹٩۰٠', u'45611223345677889900')
    try:
        return input_str.strip().translate(translation)
    except:
        return input_str


'''
set of custom filed to use in apps
'''


class FarsiCharField(CharField):
    """
    Farsi character field to change multi form characters reform to standard
    """

    def to_python(self, value):
        return super(FarsiCharField, self).to_python(normalize_text(value))


class FarsiTextField(TextField):
    """
        Farsi text field to change multi form characters reform to standard
    """

    def to_python(self, value):
        return super(FarsiTextField, self).to_python(normalize_text(value))



