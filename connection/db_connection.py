import psycopg
import mysql.connector as connector
from pymongo import MongoClient


class PostgresDBConnector:
    def __init__(self, name, host, user, password, port):
        self.connection = psycopg.connect(f"dbname={name} user={user} host={host} password={password} port={port}")

    def insert(self, insert_command):
        self.connection.execute(insert_command)


class MongoDBConnector:
    def __init__(self, name, host, user, password, port):
        self.client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/{name}")

    def insert(self, insert_command):
        pass


class MySQLDBConnector:
    def __init__(self, name, host, user, password, port):
        self.connection = connector.connect(password=password, host=host, database=name, user=user, port=port)
        self.cursor = self.connection.cursor()

    def insert(self, insert_command):
        self.cursor.execute(insert_command)

