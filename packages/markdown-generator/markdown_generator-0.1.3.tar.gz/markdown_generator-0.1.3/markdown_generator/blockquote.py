class BlockQuote(object):
    def __init__(self, level=1):
        self.lines = []
        self.level = level

    def append(self, text):
        self.lines.append(text)

    def __str__(self):
        if not self.lines:
            return ''
        lines = ['{} {}\n'.format(''.ljust(self.level, '>'), line)
                 for line in self.lines]
        return ''.join(lines) + '\n'
