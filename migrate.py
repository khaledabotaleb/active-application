from peewee import PostgresqlDatabase, CharField
from playhouse.migrate import PostgresqlMigrator, migrate

my_db = PostgresqlDatabase('active_database', host='localhost', port=5432, user='postgres', password='postgres')
migrator = PostgresqlMigrator(my_db)
day = CharField(default='')


migrate(
    migrator.drop_column('availabledays', 'date'),
    migrator.add_column('availabledays', 'day', day),

)