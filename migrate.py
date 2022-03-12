from peewee import PostgresqlDatabase, BooleanField
from playhouse.migrate import PostgresqlMigrator, migrate

my_db = PostgresqlDatabase('active_database', host='localhost', port=5432, user='postgres', password='postgres')
migrator = PostgresqlMigrator(my_db)
closed = BooleanField(default=False)


migrate(
    migrator.drop_column('availabledays', 'closed'),
    migrator.add_column('availabledays', 'closed', closed),

)