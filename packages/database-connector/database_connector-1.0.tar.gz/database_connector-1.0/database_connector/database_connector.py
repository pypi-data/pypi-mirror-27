import cx_Oracle
import pymysql
import json
from bson import json_util
import sys
if sys.version_info[0] == 3:
    import configparser
else:
    import ConfigParser as configparser


class Database_Connector(object):
    """Database Connector class"""

    def __init__(self, db):
        """
        db is a string for the type of database you want to connect to
        """
        self.db = db

    def get_db_name(self):
        """
        returns the name of the db (str)
        """
        return self.db

    def get_config(self, db, config_file):
        """
        param db:	name of database object (str)
        param config_file:	config file (str)
        retuns dictionary with config info
        """
        config = configparser.ConfigParser()
        config.read(config_file)
        config_info = {}
        options = config.options(db)
        for option in options:
            try:
                config_info[option] = config.get(db, option)
            except:
                print("exception on %s!" % option)
                config_info[option] = None
        return config_info

    def connect_mysql(self, host, user, pw, port, db):
        """
        param host:	host name of the connection (str)
        param user:	user of the connection (str)
        param pw:	password of the connection (str)
        param port:	port of the host connection (str)
        param db:	database name of the connection (str)
        """
        return pymysql.connect(
            host=host,
            user=user,
            passwd=pw,
            port=int(port),
            db=db
            )

    def connect_oracle(self, host, user, pw, port, service):
        """
        param host:	host name of the connection (str)
        param user:	user of the connection (str)
        param pw:	password of the connection (str)
        param port:	port of the host connection (str)
        param service:	service name of the connection (str)
        """
        conn_str = user + '/' + pw + '@' + host + ':' + port + '/' + service
        return cx_Oracle.connect(conn_str)

    def submit_query(self, query, connection):
        """
        param query:	SQL statement (str)
        param connection:	connection object
        """
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def submit_variable_query(self, query, connection, var_list):
        """
        param query:	SQL statement (str)
        param connection:	connection object
        param var_list:		list of variables (list)
        """
        cursor = connection.cursor()
        cursor.execute(query, var_list)
        data = cursor.fetchall()
        cursor.close()
        return data

    def return_json_query(self, query, connection):
        """
        param query:	SQL statement (str)
        param connection:	connection object
        """
        cursor = connection.cursor()
        cursor.execute(query)
        rows = [x for x in cursor]
        cols = [x[0] for x in cursor.description]
        vals = []
        for row in rows:
            val = {}
            for k, v in zip(cols, row):
                try:
                    v = v.strip()
                except:
                    pass
                val[k] = v
            vals.append(val)
        return json.dumps(vals, default=json_util.default, sort_keys=True,
                          indent=4, separators=(',', ': '))

    def close_connection(self, connection):
        """
        param connection:	pyodbc connection object
        closes odbc connection
        """
        connection.close()
