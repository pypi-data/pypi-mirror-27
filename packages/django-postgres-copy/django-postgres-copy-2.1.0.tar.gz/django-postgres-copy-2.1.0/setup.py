from setuptools import setup
from distutils.core import Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import django
        from django.core.management import call_command
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': 'test',
                    'USER': 'postgres',
                    'ENGINE': 'django.db.backends.postgresql_psycopg2'
                },
                'alternative': {
                    'NAME': 'test_alternative',
                    'USER': 'postgres',
                    'ENGINE': 'django.db.backends.postgresql_psycopg2'
                },
                'sqlite': {
                    'NAME': 'sqlite',
                    'ENGINE': 'django.db.backends.sqlite3'
                },
                'secondary': {
                    'NAME': 'test_secondary',
                    'USER': 'postgres',
                    'ENGINE': 'django.db.backends.postgresql_psycopg2'
                }
            },
            INSTALLED_APPS=("tests",),
            DATABASE_ROUTERS=['tests.router.CustomRouter']
        )
        django.setup()
        call_command('test', 'tests.tests')


setup(
    name='django-postgres-copy',
    version='2.1.0',
    description="Quickly move comma-delimited data in and out of a Django model using PostgreSQL's COPY command",
    author='Ben Welsh',
    author_email='ben.welsh@gmail.com',
    url='http://django-postgres-copy.californiacivicdata.org/',
    license="MIT",
    packages=("postgres_copy",),
    install_requires=("psycopg2>=2.7.3",),
    cmdclass={'test': TestCommand},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'License :: OSI Approved :: MIT License',
    ],
)
