#!/usr/bin/env python
# vim: set fileencoding=utf-8:
'''
warcprox/main.py - entrypoint for warcprox executable, parses command line
arguments, initializes components, starts controller, handles signals

Copyright (C) 2013-2017 Internet Archive

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
USA.
'''

from __future__ import absolute_import

try:
    import queue
except ImportError:
    import Queue as queue

import logging
import sys
import hashlib
import argparse
import os
import socket
import traceback
import signal
import threading
import certauth.certauth
import warcprox
import doublethink
import cryptography.hazmat.backends.openssl
import importlib

class BetterArgumentDefaultsHelpFormatter(
                argparse.ArgumentDefaultsHelpFormatter,
                argparse.RawDescriptionHelpFormatter):
    '''
    HelpFormatter with these properties:

    - formats option help like argparse.ArgumentDefaultsHelpFormatter except
      that it omits the default value for arguments with action='store_const'
    - like argparse.RawDescriptionHelpFormatter, does not reformat description
      string
    '''
    def _get_help_string(self, action):
        if isinstance(action, argparse._StoreConstAction):
            return action.help
        else:
            return argparse.ArgumentDefaultsHelpFormatter._get_help_string(self, action)

def _build_arg_parser(prog):
    arg_parser = argparse.ArgumentParser(prog=prog,
            description='warcprox - WARC writing MITM HTTP/S proxy',
            formatter_class=BetterArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-p', '--port', dest='port', default='8000',
            type=int, help='port to listen on')
    arg_parser.add_argument('-b', '--address', dest='address',
            default='localhost', help='address to listen on')
    arg_parser.add_argument('-c', '--cacert', dest='cacert',
            default='./{0}-warcprox-ca.pem'.format(socket.gethostname()),
            help='CA certificate file; if file does not exist, it will be created')
    arg_parser.add_argument('--certs-dir', dest='certs_dir',
            default='./{0}-warcprox-ca'.format(socket.gethostname()),
            help='where to store and load generated certificates')
    arg_parser.add_argument('-d', '--dir', dest='directory',
            default='./warcs', help='where to write warcs')
    arg_parser.add_argument('-z', '--gzip', dest='gzip', action='store_true',
            help='write gzip-compressed warc records')
    arg_parser.add_argument('--no-warc-open-suffix', dest='no_warc_open_suffix',
            default=False, action='store_true', help=argparse.SUPPRESS)
    arg_parser.add_argument('-n', '--prefix', dest='prefix',
            default='WARCPROX', help='WARC filename prefix')
    arg_parser.add_argument(
            '-s', '--size', dest='rollover_size', default=1000*1000*1000,
            type=int, help='WARC file rollover size threshold in bytes')
    arg_parser.add_argument('--rollover-idle-time',
            dest='rollover_idle_time', default=None, type=int,
            help="WARC file rollover idle time threshold in seconds (so that Friday's last open WARC doesn't sit there all weekend waiting for more data)")
    try:
        hash_algos = hashlib.algorithms_guaranteed
    except AttributeError:
        hash_algos = hashlib.algorithms
    arg_parser.add_argument('-g', '--digest-algorithm', dest='digest_algorithm',
            default='sha1', help='digest algorithm, one of {}'.format(', '.join(hash_algos)))
    arg_parser.add_argument('--base32', dest='base32', action='store_true',
            default=False, help='write digests in Base32 instead of hex')
    arg_parser.add_argument('--method-filter', metavar='HTTP_METHOD',
                            action='append', help='only record requests with the given http method(s) (can be used more than once)')

    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument(
            '--stats-db-file', dest='stats_db_file',
            default='./warcprox.sqlite', help=(
                'persistent statistics database file; empty string or '
                '/dev/null disables statistics tracking'))
    group.add_argument(
            '--rethinkdb-stats-url', dest='rethinkdb_stats_url', help=(
                'rethinkdb stats table url, e.g. rethinkdb://db0.foo.org,'
                'db1.foo.org:38015/my_warcprox_db/my_stats_table'))

    arg_parser.add_argument('-P', '--playback-port', dest='playback_port',
            type=int, default=None, help='port to listen on for instant playback')
    arg_parser.add_argument('--playback-index-db-file', dest='playback_index_db_file',
            default='./warcprox-playback-index.db',
            help='playback index database file (only used if --playback-port is specified)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('-j', '--dedup-db-file', dest='dedup_db_file',
            default='./warcprox.sqlite', help='persistent deduplication database file; empty string or /dev/null disables deduplication')
    group.add_argument(
            '--rethinkdb-dedup-url', dest='rethinkdb_dedup_url', help=(
                'rethinkdb dedup url, e.g. rethinkdb://db0.foo.org,'
                'db1.foo.org:38015/my_warcprox_db/my_dedup_table'))
    group.add_argument(
            '--rethinkdb-big-table-url', dest='rethinkdb_big_table_url', help=(
                'rethinkdb big table url (table will be populated with '
                'various capture information and is suitable for use as '
                'index for playback), e.g. rethinkdb://db0.foo.org,'
                'db1.foo.org:38015/my_warcprox_db/captures'))
    group.add_argument(
            '--rethinkdb-trough-db-url', dest='rethinkdb_trough_db_url', help=(
                '🐷   url pointing to trough configuration rethinkdb database, '
                'e.g. rethinkdb://db0.foo.org,db1.foo.org:38015'
                '/trough_configuration'))
    group.add_argument('--cdxserver-dedup', dest='cdxserver_dedup',
            help='use a CDX Server URL for deduplication; e.g. https://web.archive.org/cdx/search')
    arg_parser.add_argument(
            '--rethinkdb-services-url', dest='rethinkdb_services_url', help=(
                'rethinkdb service registry table url; if provided, warcprox '
                'will create and heartbeat entry for itself'))
    arg_parser.add_argument('--queue-size', dest='queue_size', type=int,
            default=500, help=argparse.SUPPRESS)
    arg_parser.add_argument('--max-threads', dest='max_threads', type=int,
            help=argparse.SUPPRESS)
    arg_parser.add_argument('--profile', action='store_true', default=False,
            help=argparse.SUPPRESS)
    arg_parser.add_argument(
            '--writer-threads', dest='writer_threads', type=int, default=None,
            help=argparse.SUPPRESS)
    arg_parser.add_argument(
            '--onion-tor-socks-proxy', dest='onion_tor_socks_proxy',
            default=None, help=(
                'host:port of tor socks proxy, used only to connect to '
                '.onion sites'))
    arg_parser.add_argument(
            '--crawl-log-dir', dest='crawl_log_dir', default=None, help=(
                'if specified, write crawl log files in the specified '
                'directory; one crawl log is written per warc filename '
                'prefix; crawl log format mimics heritrix'))
    arg_parser.add_argument(
            '--plugin', metavar='PLUGIN_CLASS', dest='plugins',
            action='append', help=(
                'Qualified name of plugin class, e.g. "mypkg.mymod.MyClass". '
                'May be used multiple times to register multiple plugins. '
                'Plugin classes are loaded from the regular python module '
                'search path. They will be instantiated with no arguments and '
                'must have a method `notify(self, recorded_url, records)` '
                'which will be called for each url, after warc records have '
                'been written.'))
    arg_parser.add_argument('--version', action='version',
            version="warcprox {}".format(warcprox.__version__))
    arg_parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    arg_parser.add_argument('--trace', dest='trace', action='store_true')
    arg_parser.add_argument('-q', '--quiet', dest='quiet', action='store_true')

    return arg_parser

def dump_state(signum=None, frame=None):
    '''
    Signal handler, logs stack traces of active threads.
    '''
    state_strs = []

    for th in threading.enumerate():
        try:
            state_strs.append(str(th))
            stack = traceback.format_stack(sys._current_frames()[th.ident])
            state_strs.append(''.join(stack))
        except Exception as e:
            state_strs.append('<n/a:%r>' % e)

    logging.warn(
            'dumping state (caught signal %s)\n%s',
            signum, '\n'.join(state_strs))

def init_controller(args):
    '''
    Creates a warcprox.controller.WarcproxController configured according to
    the supplied arguments (normally the result of parse_args(sys.argv)).
    '''
    options = warcprox.Options(**vars(args))

    try:
        hashlib.new(args.digest_algorithm)
    except Exception as e:
        logging.fatal(e)
        exit(1)

    listeners = []

    if args.rethinkdb_dedup_url:
        dedup_db = warcprox.dedup.RethinkDedupDb(options=options)
    elif args.rethinkdb_big_table_url:
        dedup_db = warcprox.bigtable.RethinkCapturesDedup(options=options)
    elif args.rethinkdb_trough_db_url:
        dedup_db = warcprox.dedup.TroughDedupDb(options)
    elif args.cdxserver_dedup:
        dedup_db = warcprox.dedup.CdxServerDedup(cdx_url=args.cdxserver_dedup)
    elif args.dedup_db_file in (None, '', '/dev/null'):
        logging.info('deduplication disabled')
        dedup_db = None
    else:
        dedup_db = warcprox.dedup.DedupDb(args.dedup_db_file, options=options)
    if dedup_db:
        listeners.append(dedup_db)

    if args.rethinkdb_stats_url:
        stats_db = warcprox.stats.RethinkStatsDb(options=options)
        listeners.append(stats_db)
    elif args.stats_db_file in (None, '', '/dev/null'):
        logging.info('statistics tracking disabled')
        stats_db = None
    else:
        stats_db = warcprox.stats.StatsDb(args.stats_db_file, options=options)
        listeners.append(stats_db)

    recorded_url_q = warcprox.TimestampedQueue(maxsize=args.queue_size)

    ca_name = 'Warcprox CA on {}'.format(socket.gethostname())[:64]
    ca = certauth.certauth.CertificateAuthority(args.cacert, args.certs_dir,
                                                ca_name=ca_name)

    proxy = warcprox.warcproxy.WarcProxy(ca=ca, recorded_url_q=recorded_url_q,
            stats_db=stats_db, options=options)

    if args.playback_port is not None:
        playback_index_db = warcprox.playback.PlaybackIndexDb(
                args.playback_index_db_file, options=options)
        playback_proxy = warcprox.playback.PlaybackProxy(
                ca=ca, playback_index_db=playback_index_db, options=options)
        listeners.append(playback_index_db)
    else:
        playback_index_db = None
        playback_proxy = None

    if args.crawl_log_dir:
        listeners.append(warcprox.crawl_log.CrawlLogger(
            args.crawl_log_dir, options=options))

    for qualname in args.plugins or []:
        try:
            (module_name, class_name) = qualname.rsplit('.', 1)
            module_ = importlib.import_module(module_name)
            class_ = getattr(module_, class_name)
            listener = class_()
            listener.notify  # make sure it has this method
            listeners.append(listener)
        except Exception as e:
            logging.fatal('problem with plugin class %r: %s', qualname, e)
            sys.exit(1)

    writer_pool = warcprox.writer.WarcWriterPool(options=options)
    # number of warc writer threads = sqrt(proxy.max_threads)
    # I came up with this out of thin air because it strikes me as reasonable
    # 1=>1 2=>1 5=>2 10=>3 50=>7 100=>10 200=>14 500=>22 1000=>32 2000=>45
    num_writer_threads = args.writer_threads or int(proxy.max_threads ** 0.5)
    logging.debug('initializing %d warc writer threads', num_writer_threads)
    warc_writer_threads = [
            warcprox.writerthread.WarcWriterThread(
                name='WarcWriterThread%03d' % i, recorded_url_q=recorded_url_q,
                writer_pool=writer_pool, dedup_db=dedup_db,
                listeners=listeners, options=options)
            for i in range(num_writer_threads)]

    if args.rethinkdb_services_url:
        parsed = doublethink.parse_rethinkdb_url(
                options.rethinkdb_services_url)
        rr = doublethink.Rethinker(servers=parsed.hosts, db=parsed.database)
        svcreg = doublethink.ServiceRegistry(rr, table=parsed.table)
    else:
        svcreg = None

    controller = warcprox.controller.WarcproxController(
            proxy, warc_writer_threads, playback_proxy,
            service_registry=svcreg, options=options)

    return controller

def parse_args(argv):
    '''
    Parses command line arguments with argparse.
    '''
    arg_parser = _build_arg_parser(prog=os.path.basename(argv[0]))
    args = arg_parser.parse_args(args=argv[1:])
    return args

def main(argv=None):
    '''
    Main method, entry point of warcprox command.
    '''
    args = parse_args(argv or sys.argv)

    if args.trace:
        loglevel = warcprox.TRACE
    elif args.verbose:
        loglevel = logging.DEBUG
    elif args.quiet:
        loglevel = logging.WARNING
    else:
        loglevel = logging.INFO

    logging.basicConfig(
            stream=sys.stdout, level=loglevel, format=(
                '%(asctime)s %(process)d %(levelname)s %(threadName)s '
                '%(name)s.%(funcName)s(%(filename)s:%(lineno)d) %(message)s'))

    # see https://github.com/pyca/cryptography/issues/2911
    cryptography.hazmat.backends.openssl.backend.activate_builtin_random()

    controller = init_controller(args)

    signal.signal(signal.SIGTERM, lambda a,b: controller.stop.set())
    signal.signal(signal.SIGINT, lambda a,b: controller.stop.set())
    try:
        signal.signal(signal.SIGQUIT, dump_state)
    except AttributeError:
        # SIGQUIT does not exist on some platforms (windows)
        pass

    controller.run_until_shutdown()

def ensure_rethinkdb_tables(argv=None):
    '''
    Creates rethinkdb tables if they don't already exist. Warcprox normally
    creates the tables it needs on demand at startup, but if multiple instances
    are starting up at the same time, you can end up with duplicate broken
    tables. So it's a good idea to use this utility at an early step when
    spinning up a cluster.
    '''
    argv = argv or sys.argv
    arg_parser = argparse.ArgumentParser(
            prog=os.path.basename(argv[0]),
            formatter_class=BetterArgumentDefaultsHelpFormatter)
    arg_parser.add_argument(
            '--rethinkdb-stats-url', dest='rethinkdb_stats_url', help=(
                'rethinkdb stats table url, e.g. rethinkdb://db0.foo.org,'
                'db1.foo.org:38015/my_warcprox_db/my_stats_table'))
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument(
            '--rethinkdb-dedup-url', dest='rethinkdb_dedup_url', help=(
                'rethinkdb dedup url, e.g. rethinkdb://db0.foo.org,'
                'db1.foo.org:38015/my_warcprox_db/my_dedup_table'))
    group.add_argument(
            '--rethinkdb-big-table-url', dest='rethinkdb_big_table_url', help=(
                'rethinkdb big table url (table will be populated with '
                'various capture information and is suitable for use as '
                'index for playback), e.g. rethinkdb://db0.foo.org,'
                'db1.foo.org:38015/my_warcprox_db/captures'))
    group.add_argument(
            '--rethinkdb-trough-db-url', dest='rethinkdb_trough_db_url', help=(
                '🐷   url pointing to trough configuration rethinkdb database, '
                'e.g. rethinkdb://db0.foo.org,db1.foo.org:38015'
                '/trough_configuration'))
    arg_parser.add_argument(
            '--rethinkdb-services-url', dest='rethinkdb_services_url', help=(
                'rethinkdb service registry table url; if provided, warcprox '
                'will create and heartbeat entry for itself'))
    arg_parser.add_argument(
            '-q', '--quiet', dest='log_level',
            action='store_const', default=logging.INFO, const=logging.WARN)
    arg_parser.add_argument(
            '-v', '--verbose', dest='log_level',
            action='store_const', default=logging.INFO, const=logging.DEBUG)
    args = arg_parser.parse_args(args=argv[1:])

    logging.basicConfig(
            stream=sys.stdout, level=args.log_level, format=(
                '%(asctime)s %(levelname)s %(name)s.%(funcName)s'
                '(%(filename)s:%(lineno)d) %(message)s'))

    options = warcprox.Options(**vars(args))

    did_something = False
    if args.rethinkdb_services_url:
        parsed = doublethink.parse_rethinkdb_url(
                options.rethinkdb_services_url)
        rr = doublethink.Rethinker(servers=parsed.hosts, db=parsed.database)
        svcreg = doublethink.ServiceRegistry(rr, table=parsed.table)
        did_something = True
    if args.rethinkdb_stats_url:
        stats_db = warcprox.stats.RethinkStatsDb(options=options)
        did_something = True
    if args.rethinkdb_dedup_url:
        dedup_db = warcprox.dedup.RethinkDedupDb(options=options)
        did_something = True
    if args.rethinkdb_big_table_url:
        dedup_db = warcprox.bigtable.RethinkCapturesDedup(options=options)
        did_something = True
    if args.rethinkdb_trough_db_url:
        dedup_db = warcprox.dedup.TroughDedupDb(options)
        logging.warn(
                'trough it responsible for creating most of the rethinkdb '
                'tables that it uses')
        did_something = True

    if not did_something:
        logging.error('nothing to do, no --rethinkdb-* options supplied')

if __name__ == '__main__':
    main()

