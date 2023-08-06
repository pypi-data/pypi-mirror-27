import csv

from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import Statement, StatementLine, BankAccount, recalculate_balance


class TriodosBePlugin(Plugin):
    """Belgian Triodos plugin for ofxstatement
    """

    def get_parser(self, filename):
        f = open(filename, 'r', encoding=self.settings.get("charset", "ISO-8859-1"))
        parser = TriodosBeParser(f)
        return parser


class TriodosBeParser(CsvStatementParser):
    date_format = "%d-%m-%Y"
    mappings = {
        'date': 0,
        'payee': 5,
        'memo': 8,
        'amount': 2
    }

    def __init__(self, filename):
        self.statement = Statement('TRIOBEBB', None,'EUR')
        self.fin = filename
        self.statement.currency = 'EUR'

    def parse(self):
        """Main entry point for parsers

        super() implementation will call to split_records and parse_record to
        process the file.
        """
        stmt = super(TriodosBeParser, self).parse()
        recalculate_balance(stmt)
        return stmt

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """
        reader = csv.reader(self.fin)
        next(reader, None)
        return reader

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """
        if (self.statement.account_id == None):
            self.statement.account_id =  line[1]
        stmtline = super(TriodosBeParser, self).parse_record(line)
        stmtline.trntype = 'DEBIT' if stmtline.amount < 0 else 'CREDIT'
        stmtline.bank_account_to = BankAccount(line[4], line[3])
        return stmtline

    def parse_float(self, value):
        """Return a float from a string with ',' as decimal mark.
         ex. 1.234,56 -> 1234.56
        """
        return float(value.replace('.','').replace(',', '.'))
