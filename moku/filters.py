from emoji import demojize


def unemoji(txt: str):
    """Turn emoji in the given string into plain text."""
    return demojize(txt, delimiters=("", ""))
