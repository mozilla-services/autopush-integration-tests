"""Module for formatting text output for Bugzilla comments and Jenkins
console output readability."""

LINE = '------------------'
LINE_LONG = '------------------------------------'
LINE_DBL = '=================================================='
NL = '\n'


class OutputHelper(object):

    @staticmethod
    def get_header(label):
        return '\n{0}\n{1}\n{2}\n'.format(LINE, label, LINE)

    @staticmethod
    def get_sub_header(label):
        return '\n{0}\n'.format(label)

    @staticmethod
    def log(msg, has_header=False, has_header_dbl=False):
        """Log activity for console monitoring"""

        if has_header:
            line = LINE_DBL if has_header_dbl else LINE_LONG
            print(u'\n{0}\n{1}\n{2}\n'.format(line, msg, line))
        else:
            print(u'{0}'.format(msg))


if __name__ == '__main__':

    out = OutputHelper()
    print(out.get_header('YOUR HEADER'))
    print(out.get_sub_header('MY_SUB_HEADER'))
