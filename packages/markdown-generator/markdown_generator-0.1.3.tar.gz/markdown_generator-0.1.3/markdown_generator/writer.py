from os import linesep


class Writer(object):
    def __init__(self, stdout):
        self.stdout = stdout

    def write(self, text=''):
        self.stdout.write(str(text))

    def writeline(self, text=''):
        self.write(str(text) + linesep)

    def writelines(self, lines):
        for line in lines:
            self.writeline(str(line))

    def write_heading(self, text, level=1):
        self.writeline(''.ljust(level, '#') + ' ' + str(text))

    def write_hrule(self):
        self.writeline('---')
