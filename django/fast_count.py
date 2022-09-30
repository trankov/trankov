from django.db import connection


def pg_count(model):
    """
    Returns Count() using PostgreSQL service tables
    """
    cursor = connection.cursor()
    cursor.execute(
    f'''
        SELECT reltuples::bigint
        FROM pg_catalog.pg_class
        WHERE relname='{model.objects.model._meta.db_table}';
    ''')
    return cursor.fetchone()


"""
    >>> class MyUser(models.Model):
    >>>     ...
    >>>     @classmethod
    >>>     def postgres_count(cls):
    >>>         return pg_count(cls)

    >>> print(f"Number or registerted users: {MyUser.postgres_count()}")

"""

# TODO: Define as model's manager cuctom method
