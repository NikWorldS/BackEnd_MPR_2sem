VALID_TICKERS = [
    'GLDRUB_TOM', 'SLVRUB_TOM', 'PLDRUB_TOM', 'PLTRUB_TOM'
]

def is_valid_ticker(ticker):
    return ticker in VALID_TICKERS
