import sys
sys.path.insert(0, 'database_connector')
import database_connector as db  # noqa


def main():
    query = """
    select count(1)
    from sample_taqman_analysis_KB;
    """
    config_file = 'config.cfg'
    myDB = db.Database_Connector('DGD')
    db_config = myDB.get_config(myDB.get_db_name(), config_file)
    cxcn = myDB.connect_mysql(
            host=db_config['host'],
            user=db_config['user'],
            pw=db_config['pw'],
            port=int(db_config['port']),
            db=db_config['db']
    )
    data = myDB.submit_query(query, cxcn)
    for d in data:
        print(d)


if __name__ == '__main__':
    main()
