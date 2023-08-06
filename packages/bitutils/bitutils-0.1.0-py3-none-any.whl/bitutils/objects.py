from dictutils import AttrDict


class Exchange(AttrDict):
    def __init__(self, name=None, **kwargs):
        super(Exchange, self).__init__(**kwargs)
        self.name = name


class Currency(AttrDict):

    def __init__(self, code=None, name=None, symbol=None, decimals=None, type=None, **kwargs):
        super(Currency, self).__init__(**kwargs)
        self.code = code
        self.name = name
        self.symbol = symbol
        self.decimals = decimals
        self.type = type
        self.exchanges = []


class Market(AttrDict):
    def __init__(self, code=None, name=None, base=None, quote=None, **kwargs):
        super(Market, self).__init__(**kwargs)
        self.code = code
        self.name = name
        self.base = base
        self.quote = quote
        self.exchanges = []
