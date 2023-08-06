__author__ = 'kmadac'

import os
import bitstamp.client

try:
    bc = bitstamp.client.Trading(username=os.environ['bs_user'],
                             key=os.environ['bs_key'],
                             secret=os.environ['bs_secret'])
except bitstamp.client.BitstampError:
    pass

print(bc.account_balance())

