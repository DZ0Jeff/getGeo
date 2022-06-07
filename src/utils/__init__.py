import string


def strip_ponctuation(stringname):
    """
    Strip punctuation from a string
    """
    pass
    return stringname.translate(str.maketrans('', '', string.punctuation))
