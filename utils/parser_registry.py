from parsers.tinkoff_parser import TinkoffParser
from parsers.moex_parser import MoexParser

PARSERS = {
    'TINKOFF': TinkoffParser,
    'MOEX': MoexParser,
}