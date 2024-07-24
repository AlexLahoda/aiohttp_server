import psycopg # this uses psycopg version 3

def conection():
    config = {'user':'postgres',
          'password':'postgres',
              'host':'127.0.0.1',
              'port':'5432',
            'dbname':'iot',
        'autocommit':True}
    try:
        cnx = psycopg.connect(**config)
    except psycopg.Error as err:
        print(err)
        exit(1)
    else:
        return cnx

if __name__ == "__main__":
    conection()