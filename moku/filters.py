from emoji import demojize


def unemoji(txt: str):
    return demojize(txt, delimiters=("", ""))
