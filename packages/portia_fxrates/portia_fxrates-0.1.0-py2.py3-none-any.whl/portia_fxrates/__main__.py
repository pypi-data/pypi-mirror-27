import sys


import logging
logger = logging.getLogger(__name__)

import argparse
import ast

from .openfxrates import getFX


#entry point from the command line
def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(description="FX Rates from OpenExchangerates.org")
    parser.add_argument("-curr", "--currlist", help="Currencylist in list format ['EUR', 'CHF']", type=ast.literal_eval)
    parser.add_argument("-cob", "--cobdate", help="Cobdate for historical rates", type=int)
    args = parser.parse_args()
    fx = getFX(args.currlist, args.cobdate)
    fx.to_clipboard(index=False)
    print(fx.to_string(index=False))

    
if __name__ == "__main__":
    main()