class List(object):
    def __init__(self, ordered=False):
        self.items = []
        self.ordered = ordered

    def append(self, item):
        self.items.append(item)

    def __str__(self):
        if self.items:
            def prepend(item, marker):
                return '{} {}\n'.format(marker, item)
            if self.ordered:
                result = ''.join(prepend(x, '{}.'.format(i + 1))
                                 for i, x in enumerate(self.items))
            else:
                result = ''.join(prepend(x, '*') for x in self.items)
            return result + '\n'
        return ''


class CheckList(object):
    def __init__(self):
        self.items = []

    def append(self, item, done=False):
        self.items.append((item, done))

    def __str__(self):
        if self.items:
            lines = []
            for item, done in self.items:
                mark = 'x' if done else ' '
                lines.append('- [{}] {}\n'.format(mark, item))
            return ''.join(lines) + '\n'
        return ''
