from setuptools import setup, find_packages

setup(
    name="book-collection-manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "alembic",
        "faker",
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'book-manager=lib.cli:main',
        ],
    },
)