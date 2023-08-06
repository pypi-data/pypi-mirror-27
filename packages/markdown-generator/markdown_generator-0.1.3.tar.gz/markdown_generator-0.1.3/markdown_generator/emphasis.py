def wrap(text, tag):
    return tag + str(text) + tag if text else ''


def emphasis(text):
    return wrap(text, '*')


def strong(text):
    return wrap(text, '**')


def strikethrough(text):
    return wrap(text, '~~')
