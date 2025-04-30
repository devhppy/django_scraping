# devhome/database_router.py

from django_cassandra_engine.models import DjangoCassandraModel

class CassandraRouter:
    """
    Route Django ORM operations:
      – all DjangoCassandraModel-subclasses → 'cassandra'
      – everything else                      → 'default'
    """

    def db_for_read(self, model, **hints):
        if issubclass(model, DjangoCassandraModel):
            return 'cassandra'
        return 'default'

    def db_for_write(self, model, **hints):
        if issubclass(model, DjangoCassandraModel):
            return 'cassandra'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # allow relations if both objs use the same DB
        db1 = 'cassandra' if issubclass(obj1.__class__, DjangoCassandraModel) else 'default'
        db2 = 'cassandra' if issubclass(obj2.__class__, DjangoCassandraModel) else 'default'
        if db1 == db2:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # skip Django migrations for Cassandra models (we use sync_cassandra instead)
        if db == 'cassandra':
            return False
        # allow all migrations on default (SQLite/Postgres)
        return True
