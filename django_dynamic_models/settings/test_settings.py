from settings import *

MIGRATION_DIR = os.getcwd() + '/django_dynamic_models/dynamic_models/migrations'
TEST_MIGRATION_DIR = os.path.join(MIGRATION_DIR, 'test_migrations')

if not os.path.exists(TEST_MIGRATION_DIR):
    os.mkdir(TEST_MIGRATION_DIR)
    init_file = open(os.path.join(TEST_MIGRATION_DIR, '__init__.py'), 'w')
    init_file.close()

    init_migration_file_org = \
        open(os.path.join(MIGRATION_DIR, '0001_initial.py'), 'r')
    text = init_migration_file_org.read()
    init_migration_file_org.close()

    init_migration_file_copy = \
        open(os.path.join(TEST_MIGRATION_DIR, '0001_initial.py'), 'w')
    init_migration_file_copy.write(text)
    init_migration_file_copy.close()


SOUTH_MIGRATION_MODULES = {
    'dynamic_models': 'dynamic_models.migrations.test_migrations',
}