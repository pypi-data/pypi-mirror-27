import logging
import click
from itertools import chain
from collections import namedtuple
import asyncio

from tornado.platform.asyncio import AsyncIOMainLoop
from streamz import Stream, union, combine_latest, zip_latest
import attr

from .events import PriceUpdate
from .collectors import Collector
from .feeds import Feed
from .config import config

logger = logging.getLogger(__name__)

AsyncIOMainLoop().install()


ENVVAR_PREFIX = 'NUMISMATIC'


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


pass_state = click.make_pass_decorator(dict, ensure=True)

@click.group(cls=AliasedGroup, chain=True)
@click.option('--cache-dir', '-d', default=None)
@click.option('--requester', '-r', default='base',
              type=click.Choice(['base', 'caching']))
@click.option('--log-level', '-l', default='info', 
              type=click.Choice(['debug', 'info', 'warning', 'error',
                                 'critical']))
@pass_state
def coin(state, cache_dir, requester, log_level):
    '''Numismatic Command Line Interface

    Examples:

        coin list

        coin info

        coin info -a ETH

        coin prices

        coin prices -a XMR,ZEC -c EUR,ZAR
        
        coin prices --raw

        coin prices -f luno

        coin tickers -f cryptocompare

        coin tickers -f cryptocompare --raw

        coin history

        coin history -a ETH -c BTC -o ETH-BTH-history.json

        coin subscribe collect run

        coin subscribe -a BTC,ETH,XMR,ZEC collect -t Trade run -t 30

        coin subscribe -f bitfinex -f gdax collect run

        coin subscribe -f bitfinex -f gdax collect --raw run

        coin subscribe -f cryptocompare collect run

        coin subscribe -f cryptocompare -e kraken collect run

        coin subscribe -f bitfinex -f gdax compare run

        coin sub -f cryptocompare -C tickers -e cexio sub -f \\
            cryptocompare -C prices -e kraken sub -f bitfinex sub -f gdax \\
            sub -f poloniex compare run
    '''
    logging.basicConfig(level=getattr(logging, log_level.upper()))
    state['cache_dir'] = cache_dir
    state['requester'] = requester
    state['output_stream'] = Stream()
    state['subscriptions'] = {}

@coin.command(name='list')
@click.option('--feed', '-f', default=config['DEFAULT']['Feed'],
              type=click.Choice(Feed._get_subclasses().keys()))
@click.option('--output', '-o', type=click.File('wt'), default='-')
@pass_state
def list_all(state, feed, output):
    "List all available assets"
    feed_client = Feed.factory(feed, cache_dir=state['cache_dir'],
                               requester=state['requester'])
    assets_list = feed_client.get_list()
    write(assets_list, output, sep=' ')

@coin.command()
@click.option('--feed', '-f', default=config['DEFAULT']['Feed'],
              type=click.Choice(Feed._get_subclasses().keys()))
@click.option('--assets', '-a', multiple=True,
              envvar=f'{ENVVAR_PREFIX}_ASSETS')
@click.option('--output', '-o', type=click.File('wt'), default='-')
@pass_state
def info(state, feed, assets, output):
    "Info about the requested assets"
    feed_client = Feed.factory(feed, cache_dir=state['cache_dir'],
                               requester=state['requester'])
    assets_info = feed_client.get_info(assets)
    write(assets_info, output)


@coin.command()
@click.option('--feed', '-f', default=config['DEFAULT']['Feed'],
              type=click.Choice(Feed._get_subclasses().keys()))
@click.option('--exchange', '-e', default=None)
@click.option('--assets', '-a', multiple=True,
              envvar=f'{ENVVAR_PREFIX}_ASSETS')
@click.option('--currencies', '-c', multiple=True,
              envvar=f'{ENVVAR_PREFIX}_CURRENCIES')
@click.option('--raw', is_flag=True)
@click.option('--output', '-o', type=click.File('wt'), default='-')
@pass_state
def prices(state, feed, exchange, assets, currencies, raw, output):
    'Latest asset prices'
    feed_client = Feed.factory(feed, cache_dir=state['cache_dir'],
                               requester=state['requester'])
    prices = feed_client.get_prices(assets=assets, currencies=currencies,
                                    exchange=exchange, raw=raw)
    write(prices, output)


@coin.command()
@click.option('--feed', '-f', default=config['DEFAULT']['Feed'],
              type=click.Choice(Feed._get_subclasses().keys()))
@click.option('--exchange', '-e', default=None)
@click.option('--assets', '-a', multiple=True,
              envvar=f'{ENVVAR_PREFIX}_ASSETS')
@click.option('--currencies', '-c', multiple=True,
              envvar=f'{ENVVAR_PREFIX}_CURRENCIES')
@click.option('--raw', is_flag=True)
@click.option('--output', '-o', type=click.File('wt'), default='-')
@pass_state
def tickers(state, feed, exchange, assets, currencies, raw, output):
    'Latest asset tickers'
    feed_client = Feed.factory(feed, cache_dir=state['cache_dir'],
                               requester=state['requester'])
    tickers = feed_client.get_tickers(assets=assets, currencies=currencies,
                                      exchange=exchange, raw=raw)
    write(tickers, output)


@coin.command()
@click.option('--feed', '-f', default=config['DEFAULT']['Feed'],
              type=click.Choice(Feed._get_subclasses().keys()))
@click.option('--exchange', '-e', default=None)
@click.option('--freq', default='d', type=click.Choice(list('dhms')))
@click.option('--start-date', '-s', default=-30)
@click.option('--end-date', '-e', default=None)
@click.option('--assets', '-a', multiple=True,
              envvar=f'{ENVVAR_PREFIX}_ASSETS')
@click.option('--currencies', '-c', multiple=True,
              envvar=f'{ENVVAR_PREFIX}_CURRENCIES')
@click.option('--output', '-o', type=click.File('wt'), default='-')
@pass_state
def history(state, feed, exchange, assets, currencies, freq, start_date,
            end_date, output):
    'Historic asset prices and volumes'
    feed_client = Feed.factory(feed, cache_dir=state['cache_dir'],
                               requester=state['requester'])
    data = feed_client.get_historical_data(assets, currencies, freq=freq,
                                           start_date=start_date,
                                           end_date=end_date, 
                                           exchange=exchange)
    write(data, output)


# FIXME: Do we still want this?
def tabulate(data):
    if isinstance(data, dict):
        data_iter = data.values()
    elif isinstance(data, list):
        data_iter = data
    else:
        raise TypeError(f'data: {data}')
    headers = set(chain(*map(lambda v: v.keys(), data_iter)))
    DataTuple = namedtuple('DataTuple', ' '.join(headers))
    DataTuple.__new__.__defaults__ = (None,) * len(headers)
    return map(lambda d: DataTuple(**d), data_iter)


@coin.command()
@click.option('--feed', '-f', default='bitfinex',
              type=click.Choice(Feed._get_subclasses().keys()))
@click.option('--exchange', '-e', default=None)
@click.option('--assets', '-a', multiple=True,
              envvar=f'{ENVVAR_PREFIX}_ASSETS')
@click.option('--currencies', '-c', multiple=True,
              envvar=f'{ENVVAR_PREFIX}_CURRENCIES')
@click.option('--interval', '-i', default=1.0, type=float,
              help='Interval between requests for RestClient subscriptions')
@click.option('--channels', '-C', multiple=True)
@pass_state
def subscribe(state, feed, exchange, assets, currencies, interval, channels):
    'Subscribe to live events from a feed'
    feed_client = Feed.factory(feed) 
    subscriptions = feed_client.subscribe(assets, currencies, channels,
                                          exchange=exchange, interval=interval)
    state['subscriptions'].update(subscriptions)


@coin.command()
@click.option('--market', '-m', default='all')
@click.option('--event', 'stream', flag_value='event', default=True)
@click.option('--raw', 'stream', flag_value='raw')
@click.option('--collector', '-c', default='file', 
              type=click.Choice(Collector._get_subclasses().keys()))
@click.option('--output', '-o', default='-', type=click.Path())
@click.option('--filter', '-f', default='', type=str, multiple=True)
@click.option('--type', '-t', default=None, multiple=True,
              type=click.Choice(['None', 'Trade', 'Heartbeat', 'LimitOrder',
                                 'CancelOrder']))
@click.option('--text', 'format', flag_value='text', default=True)
@click.option('--json', 'format', flag_value='json')
@click.option('--interval', '-i', default=None, type=float)
@pass_state
def collect(state, market, stream, collector, filter, type, output, format, interval):
    'Collect events and write them to an output sink'
    subscriptions = state['subscriptions']
    if stream=='event':
        stream_name = 'event_stream'
    elif stream=='raw':
        stream_name = 'raw_stream'
    else:
        raise ValueError(stream)
    if market=='all':
        all_streams = [getattr(sub, stream_name) for sub in
                       subscriptions.values()]
        collect_stream = union(*all_streams)
    else:
        collect_stream = getattr(subscriptions[market], stream_name)
    collector_name = collector
    collector = Collector.factory(collector_name, event_stream=collect_stream,
                                  path=output, format=format, types=type,
                                  filters=filter, interval=interval)


@coin.command()
@click.option('--collector', '-c', default='file', 
              type=click.Choice(Collector._get_subclasses().keys()))
@click.option('--output', '-o', default='-', type=click.Path())
@click.option('--interval', '-i', default=None, type=float)
@pass_state
def compare(state, collector, output, interval):
    'Compare prices events and write them to an output sink'
    subscriptions = state['subscriptions']
    streams = [sub.event_stream.filter(lambda ev: isinstance(ev, PriceUpdate)) 
               for sub in subscriptions.values()]
    compare_stream = combine_latest(*streams).map(
        lambda trades: {(t.exchange+'--'+t.asset+'/'+t.currency):t.price for t in trades})
    collector_name = collector
    collector = Collector.factory(collector_name, event_stream=compare_stream,
                                  path=output, interval=interval)


@coin.command()
@click.option('--timeout', '-t', default=0)
@pass_state
def run(state, timeout):
    """
    Run the asyncio event loop for a set amount of time. Set to 0 to run 
    indefinitely.  Default is no-timeout."""
    if not timeout:
        # Allow to run indefinitely if timeout==0
        timeout = None
    loop = asyncio.get_event_loop()
    logger.debug('starting ...')
    tasks = asyncio.Task.all_tasks()
    try:
        if tasks:
            logger.info(f'Running {len(tasks)} tasks ...')
            completed, pending = \
                loop.run_until_complete(asyncio.wait(tasks, timeout=timeout))
        else:
            logger.info(f'Running forever ...')
            loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        logger.debug('Cancelling ...')
        tasks = asyncio.Task.all_tasks()
        pending = {task for task in tasks if not task.done()}
        for task in pending:
            logger.debug(f'Cancelling pending task {id(task)} ...')
            task.cancel()
        logger.debug('Done')


def write(data, file, sep='\n'):
    for record in data:
        file.write(str(record)+sep)


if __name__ == '__main__':
    coin()
