import logging
from typing import Any

from errbot.storage.base import StorageBase, StoragePluginBase
import rethinkdb as R
from repool_forked import ConnectionPool


__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "1.1.2"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"


log = logging.getLogger('errbot.storage.rethinkdb')


class RethinkDBStorage(StorageBase):

    def __init__(self, rethinkdb_pool, table_name, namespace):
        self.pool = rethinkdb_pool
        self.ns = namespace
        self.storage = R.table(table_name)
        database_name = self.pool._conn_args.get('db', None)  # pylint: disable=protected-access
        with self.pool.connect() as conn:
            exists_databases = R.db_list().run(conn)
            if database_name not in exists_databases:
                R.db_create(database_name).run(conn)
        with self.pool.connect() as conn:
            # Check if table exists
            exists_tables = R.table_list().run(conn)
            if table_name not in exists_tables:
                R.table_create(table_name).run(conn)

    def find(self, key: str) -> Any:
        with self.pool.connect() as c:
            result = list(self.storage.filter(R.row['key'] == key).run(c))
        return result[0] if result else None

    def get(self, key: str) -> Any:
        log.debug('Get key: %s', key)
        result = self.find(key)
        if result is None:
            raise KeyError("%s doesn't exists." % (key))
        return result['value']

    def remove(self, key: str):
        log.debug("Removing value at '%s'", key)
        with self.pool.connect() as c:
            result = self.storage.filter(R.row['key'] == key).delete().run(c)
            if result is None:
                raise KeyError('%s does not exist' % (key))

    def set(self, key: str, value: Any) -> None:
        log.debug("Setting value '%s' at '%s'", value, key)
        record = self.find(key)
        if record is None:
            with self.pool.connect() as c:
                self.storage.insert(dict(key=key, value=value)).run(c)
        else:
            with self.pool.connect() as c:
                self.storage.filter(R.row['id'] == record['id']).update(dict(key=key, value=value)).run(c)

    def len(self):
        return len(self.keys())

    def keys(self):
        with self.pool.connect() as c:
            keys = list(map(lambda x: x['key'], self.storage.pluck('key').run(c)))
        log.debug('Keys: %s', keys)
        return keys

    def close(self) -> None:
        self.pool.release_pool()


class RethinkDBPlugin(StoragePluginBase):

    def open(self, namespace: str) -> StorageBase:
        config = self._storage_config
        table_name = config.pop('table_name', 'storage')
        connection = ConnectionPool(**config)

        return RethinkDBStorage(connection, table_name, namespace)
