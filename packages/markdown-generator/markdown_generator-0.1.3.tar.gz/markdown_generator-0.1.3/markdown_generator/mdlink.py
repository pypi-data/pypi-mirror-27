def link(url, text=None):
    if url:
        if text:
            return '[{}]({})'.format(text, url)
        return url
    return ''
