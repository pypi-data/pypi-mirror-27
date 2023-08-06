from dictutils import AttrDict


class Exchange(AttrDict):
    def __init__(self, code=None, name=None, **kwargs):
        super(Exchange, self).__init__(**kwargs)
        self.code = code
        self.name = name


class Currency(AttrDict):

    def __init__(self, code=None, name=None, symbol=None, decimals=None, type=None, **kwargs):
        super(Currency, self).__init__(**kwargs)
        self.code = code
        self.name = name
        self.symbol = symbol
        self.decimals = decimals
        self.type = type
        self.address = None


class Market(AttrDict):
    def __init__(self, code=None, name=None, base=None, quote=None, **kwargs):
        super(Market, self).__init__(**kwargs)
        self.code = code
        self.name = name
        self.base = base
        self.quote = quote


class Ticker(AttrDict):
    def __init__(self, bid=None, ask=None, last=None, low=None, high=None, **kwargs):
        super(Ticker, self).__init__(**kwargs)
        self.bid = bid
        self.ask = ask
        self.last = last
        self.low = low
        self.high = high

# {
#     "mid": "244.755",
#     "bid": "244.75",
#     "ask": "244.76",
#     "last_price": "244.82",
#     "low": "244.2",
#     "high": "248.19",
#     "volume": "7842.11542563",
#     "timestamp": "1444253422.348340958"
# }
