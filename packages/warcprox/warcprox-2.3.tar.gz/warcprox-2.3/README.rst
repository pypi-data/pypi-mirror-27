warcprox - WARC writing MITM HTTP/S proxy
-----------------------------------------
.. image:: https://travis-ci.org/internetarchive/warcprox.svg?branch=master
    :target: https://travis-ci.org/internetarchive/warcprox

Based on the excellent and simple pymiproxy by Nadeem Douba.
https://github.com/allfro/pymiproxy

Install
~~~~~~~

Warcprox runs on python 2.7 or 3.4+.

To install latest release run:

::

    # apt-get install libffi-dev libssl-dev
    pip install warcprox

You can also install the latest bleeding edge code:

::

    pip install git+https://github.com/internetarchive/warcprox.git


Trusting the CA cert
~~~~~~~~~~~~~~~~~~~~

For best results while browsing through warcprox, you need to add the CA
cert as a trusted cert in your browser. If you don't do that, you will
get the warning when you visit each new site. But worse, any embedded
https content on a different server will simply fail to load, because
the browser will reject the certificate without telling you.

Usage
~~~~~

::

    usage: warcprox [-h] [-p PORT] [-b ADDRESS] [-c CACERT]
                    [--certs-dir CERTS_DIR] [-d DIRECTORY] [-z] [-n PREFIX]
                    [-s SIZE] [--rollover-idle-time ROLLOVER_IDLE_TIME]
                    [-g DIGEST_ALGORITHM] [--base32]
                    [--method-filter HTTP_METHOD]
                    [--stats-db-file STATS_DB_FILE] [-P PLAYBACK_PORT]
                    [--playback-index-db-file PLAYBACK_INDEX_DB_FILE]
                    [-j DEDUP_DB_FILE | --rethinkdb-servers RETHINKDB_SERVERS]
                    [--cdxserver-dedup CDX_SERVER_URL]
                    [--rethinkdb-db RETHINKDB_DB] [--rethinkdb-big-table]
                    [--onion-tor-socks-proxy ONION_TOR_SOCKS_PROXY]
                    [--plugin PLUGIN_CLASS] [--version] [-v] [--trace] [-q]

    warcprox - WARC writing MITM HTTP/S proxy

    optional arguments:
      -h, --help            show this help message and exit
      -p PORT, --port PORT  port to listen on (default: 8000)
      -b ADDRESS, --address ADDRESS
                            address to listen on (default: localhost)
      -c CACERT, --cacert CACERT
                            CA certificate file; if file does not exist, it
                            will be created (default:
                            ./ayutla.monkeybrains.net-warcprox-ca.pem)
      --certs-dir CERTS_DIR
                            where to store and load generated certificates
                            (default: ./ayutla.monkeybrains.net-warcprox-ca)
      -d DIRECTORY, --dir DIRECTORY
                            where to write warcs (default: ./warcs)
      -z, --gzip            write gzip-compressed warc records
      -n PREFIX, --prefix PREFIX
                            WARC filename prefix (default: WARCPROX)
      -s SIZE, --size SIZE  WARC file rollover size threshold in bytes
                            (default: 1000000000)
      --rollover-idle-time ROLLOVER_IDLE_TIME
                            WARC file rollover idle time threshold in seconds
                            (so that Friday's last open WARC doesn't sit
                            there all weekend waiting for more data)
                            (default: None)
      -g DIGEST_ALGORITHM, --digest-algorithm DIGEST_ALGORITHM
                            digest algorithm, one of sha1, sha384, sha512,
                            md5, sha224, sha256 (default: sha1)
      --base32              write digests in Base32 instead of hex
      --method-filter HTTP_METHOD
                            only record requests with the given http
                            method(s) (can be used more than once) (default:
                            None)
      --stats-db-file STATS_DB_FILE
                            persistent statistics database file; empty string
                            or /dev/null disables statistics tracking
                            (default: ./warcprox.sqlite)
      -P PLAYBACK_PORT, --playback-port PLAYBACK_PORT
                            port to listen on for instant playback (default:
                            None)
      --playback-index-db-file PLAYBACK_INDEX_DB_FILE
                            playback index database file (only used if
                            --playback-port is specified) (default:
                            ./warcprox-playback-index.db)
      -j DEDUP_DB_FILE, --dedup-db-file DEDUP_DB_FILE
                            persistent deduplication database file; empty
                            string or /dev/null disables deduplication
                            (default: ./warcprox.sqlite)
      --cdxserver-dedup CDX_SERVER_URL
                            use a CDX server for deduplication
                            (default: None)
      --rethinkdb-servers RETHINKDB_SERVERS
                            rethinkdb servers, used for dedup and stats if
                            specified; e.g.
                            db0.foo.org,db0.foo.org:38015,db1.foo.org
                            (default: None)
      --rethinkdb-db RETHINKDB_DB
                            rethinkdb database name (ignored unless
                            --rethinkdb-servers is specified) (default:
                            warcprox)
      --rethinkdb-big-table
                            use a big rethinkdb table called "captures",
                            instead of a small table called "dedup"; table is
                            suitable for use as index for playback (ignored
                            unless --rethinkdb-servers is specified)
      --onion-tor-socks-proxy ONION_TOR_SOCKS_PROXY
                            host:port of tor socks proxy, used only to
                            connect to .onion sites (default: None)
      --plugin PLUGIN_CLASS
                            Qualified name of plugin class, e.g.
                            "mypkg.mymod.MyClass". May be used multiple times
                            to register multiple plugins. Plugin classes are
                            loaded from the regular python module search
                            path. They will be instantiated with no arguments
                            and must have a method `notify(self,
                            recorded_url, records)` which will be called for
                            each url, after warc records have been written.
                            (default: None)
      --version             show program's version number and exit
      -v, --verbose
      --trace
      -q, --quiet

License
~~~~~~~

Warcprox is a derivative work of pymiproxy, which is GPL. Thus warcprox is also
GPL.

* Copyright (C) 2012 Cygnos Corporation
* Copyright (C) 2013-2017 Internet Archive

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

