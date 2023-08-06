#!/bin/python

import argparse
import sys

from bitfeeds.exchange import ExchangeGateway
from bitfeeds.broker.bitmex import ExchGwBitmex
from bitfeeds.broker.btcc import ExchGwBtccSpot, ExchGwBtccFuture
from bitfeeds.broker.bitfinex import ExchGwBitfinex
from bitfeeds.broker.okcoin import ExchGwOkCoin
from bitfeeds.broker.kraken import ExchGwKraken
from bitfeeds.broker.gdax import ExchGwGdax
from bitfeeds.broker.bitstamp import ExchGwBitstamp
from bitfeeds.broker.gatecoin import ExchGwGatecoin
from bitfeeds.broker.quoine import ExchGwQuoine
from bitfeeds.broker.poloniex import ExchGwPoloniex
from bitfeeds.broker.bittrex import ExchGwBittrex
from bitfeeds.broker.yunbi import ExchGwYunbi
from bitfeeds.broker.liqui import ExchGwLiqui
from bitfeeds.broker.binance import ExchGwBinance
from bitfeeds.broker.cryptopia import ExchGwCryptopia
# from bitfeeds.broker.cryptopia import CryptopiaBroker

from bitfeeds.client.kdbplus import KdbPlusClient
from bitfeeds.client.sqlite import SqliteClient
from bitfeeds.client.zeromq import ZmqClient
from bitfeeds.client.mysql import MysqlClient
from bitfeeds.client.file import FileClient

from bitfeeds.subscription import SubscriptionManager
from bitfeeds.util import Logger


def main():
    parser = argparse.ArgumentParser(description='Bitcoin exchange market data feed handler.')
    parser.add_argument('-instmts', action='store', help='Instrument subscription file.', default='subscriptions.ini')
    parser.add_argument('-exchtime', action='store_true', help='Use exchange timestamp.')
    parser.add_argument('-kdb', action='store_true', help='Use Kdb+ as database.')
    parser.add_argument('-csv', action='store_true', help='Use csv file as database.')
    parser.add_argument('-sqlite', action='store_true', help='Use SQLite database.')
    parser.add_argument('-mysql', action='store_true', help='Use MySQL.')
    parser.add_argument('-zmq', action='store_true', help='Use zmq publisher.')
    parser.add_argument('-mysqldest', action='store', dest='mysqldest',
                        help='MySQL destination. Formatted as <name:pwd@host:port>',
                        default='')
    parser.add_argument('-mysqlschema', action='store', dest='mysqlschema',
                        help='MySQL schema.',
                        default='')
    parser.add_argument('-kdbdest', action='store', dest='kdbdest',
                        help='Kdb+ destination. Formatted as <host:port>',
                        default='')
    parser.add_argument('-zmqdest', action='store', dest='zmqdest',
                        help='Zmq destination. For example \"tcp://127.0.0.1:3306\"',
                        default='')
    parser.add_argument('-sqlitepath', action='store', dest='sqlitepath',
                        help='SQLite database path',
                        default='')
    parser.add_argument('-csvpath', action='store', dest='csvpath',
                        help='Csv file path',
                        default='')
    parser.add_argument('-output', action='store', dest='output',
                        help='Verbose output file path')
    args = parser.parse_args()

    Logger.init_log(args.output)

    db_clients = []
    is_database_defined = False
    
    if args.sqlite:
        db_client = SqliteClient()
        db_client.connect(path=args.sqlitepath)
        db_clients.append(db_client)
        is_database_defined = True

    if args.mysql:
        db_client = MysqlClient()
        mysqldest = args.mysqldest
        logon_credential = mysqldest.split('@')[0]
        connection = mysqldest.split('@')[1]
        
        db_client.connect(host=connection.split(':')[0],
                          port=int(connection.split(':')[1]),
                          user=logon_credential.split(':')[0],
                          pwd=logon_credential.split(':')[1],
                          schema=args.mysqlschema)
        
        db_clients.append(db_client)
        is_database_defined = True

    if args.csv:
        if args.csvpath != '':
            db_client = FileClient(dir=args.csvpath)
        else:
            db_client = FileClient()

        db_clients.append(db_client)
        is_database_defined = True
    
    if args.kdb:
        db_client = KdbPlusClient()
        db_client.connect(host=args.kdbdest.split(':')[0], port=int(args.kdbdest.split(':')[1]))
        db_clients.append(db_client)
        is_database_defined = True

    if args.zmq:
        db_client = ZmqClient()
        db_client.connect(addr=args.zmqdest)
        db_clients.append(db_client)
        is_database_defined = True

    if not is_database_defined:
        print('Error: Please define which database is used.')
        parser.print_help()
        sys.exit(1)

    # Subscription instruments
    if args.instmts is None or len(args.instmts) == 0:
        print('Error: Please define the instrument subscription list. You can refer to subscriptions.ini.')
        parser.print_help()
        sys.exit(1)
        
    # Use exchange timestamp rather than local timestamp
    if args.exchtime:
        ExchangeGateway.is_local_timestamp = False
    
    # Initialize subscriptions
    subscription_instmts = SubscriptionManager(args.instmts).get_subscriptions()
    
    if len(subscription_instmts) == 0:
        print('Error: No instrument is found in the subscription file. ' +
              'Please check the file path and the content of the subscription file.')
        
        parser.print_help()
        sys.exit(1)        
    
    # Initialize snapshot destination
    ExchangeGateway.init_snapshot_table(db_clients)

    Logger.info(__name__, 'Subscription file = %s' % args.instmts)
    log_str = 'Exchange/Instrument/InstrumentCode:\n'
    
    for instmt in subscription_instmts:
        log_str += '%s/%s/%s\n' % (instmt.exchange_name, instmt.instmt_name, instmt.instmt_code)
    
    Logger.info(__name__, log_str)
    
    gateways = []
    gateways.append(ExchGwBtccSpot(db_clients))
    gateways.append(ExchGwBtccFuture(db_clients))
    gateways.append(ExchGwBitmex(db_clients))
    gateways.append(ExchGwBitfinex(db_clients))
    gateways.append(ExchGwOkCoin(db_clients))
    gateways.append(ExchGwKraken(db_clients))
    gateways.append(ExchGwGdax(db_clients))
    gateways.append(ExchGwBitstamp(db_clients))
    gateways.append(ExchGwGatecoin(db_clients))
    gateways.append(ExchGwQuoine(db_clients))
    gateways.append(ExchGwPoloniex(db_clients))
    gateways.append(ExchGwBittrex(db_clients))
    gateways.append(ExchGwYunbi(db_clients))
    gateways.append(ExchGwLiqui(db_clients))
    gateways.append(ExchGwBinance(db_clients))
    gateways.append(ExchGwCryptopia(db_clients))

    threads = []

    for item in gateways:
        for instmt in subscription_instmts:
            if instmt.get_exchange_name() == item.get_exchange_name():
                Logger.info(__name__, "Starting instrument %s-%s..." % \
                    (instmt.get_exchange_name(), instmt.get_instmt_name()))
                threads += item.start(instmt)

if __name__ == '__main__':
    main()
