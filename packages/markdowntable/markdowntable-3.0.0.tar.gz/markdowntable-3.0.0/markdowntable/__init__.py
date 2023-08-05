from __future__ import print_function, unicode_literals


class Table():
    """docstring for Table.
    This is the main class. It adds rows and columns, with data
    """
    def __init__(self,name):
        super(Table, self).__init__()
        self.rows = 0
        self.columns = 1
        self.table = '''|{}|'''.format(str(name))
        self.finalized = False

    def add_column(self, name):
        self.columns += 1
        self.table += '''{}|'''.format(name)
	
    def all_columns(self, *args):
        for value in args:
            self.add_column(str(value))

    def finalize_cols(self):
        finalizer = '\n|'
        for i in range(self.columns):
            finalizer += '---|'
        self.table += finalizer


    def add_row(self, *args):
        if not self.finalized:
            self.finalize_cols()
            self.finalized = True
        self.rows += 1
        row = '|'
        rows_made = 0
        for i in range(int(len(args))):
            row += '{}|'.format(str(args[i]))
            rows_made += 1
        if self.columns > rows_made:
            for i in range(int(self.columns-rows_made)):
                row += ' |'
        elif self.columns < rows_made:
            raise AssertionError('You entered in too many row values. Please only enter {} row names.'.format(str(self.columns)))
        self.table += '\n{}'.format(row)

    def get_table(self):
        return self.table