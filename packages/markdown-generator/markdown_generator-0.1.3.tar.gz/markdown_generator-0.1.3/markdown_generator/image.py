class Image(object):
    def __init__(self, img_url, alt_text=None):
        self.img_url = img_url
        self.alt_text = alt_text

    def __str__(self):
        if not self.img_url:
            return ''
        return '![{}]({})'.format(('' if self.alt_text is None
                                   else self.alt_text),
                                  self.img_url)
