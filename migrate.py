from peewee import PostgresqlDatabase, BooleanField, CharField, IntegerField
from playhouse.migrate import PostgresqlMigrator, migrate

from DB_Structure import Staff

my_db = PostgresqlDatabase('active_database', host='localhost', port=5432, user='postgres', password='postgres')
migrator = PostgresqlMigrator(my_db)
mobile_field = IntegerField(null=True)

migrate(
    migrator.drop_column('staff', 'mobile'),
    migrator.add_column('staff', 'mobile', mobile_field)
)