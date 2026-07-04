from .broker.alpaca import Alpaca

if __name__ == "__main__":
    # TODO: Make it so that arguments are parsed (api keys, etc) 
    alpaca_broker = Alpaca("aaa", "bbb")
        