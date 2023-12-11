from configparser import ConfigParser
import psycopg2

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def create_table():
    try:
        db_config = config()
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        create_table_query = '''
                  CREATE TABLE IF NOT EXISTS billionaires(
                      id SERIAL PRIMARY KEY,
                      name VARCHAR(255) NOT NULL,
                      net_worth VARCHAR(20),   
                      age INT,
                      country_territory VARCHAR(255),
                      source VARCHAR(255),
                      industry VARCHAR(255)
                  );
              '''
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabela a fost creată cu succes!")
    except Exception as e:
        print("Eroare la crearea tabelei : {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_data(name, net_worth, age, country_territory, source, industry):
    try:
        db_config = config()
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        insert_data_query = '''
                   INSERT INTO billionaires(name, net_worth, age, country_territory, source, industry)
                   VALUES (%s, %s, %s, %s, %s, %s);
        '''

        cursor.execute(insert_data_query, (name, net_worth, age, country_territory, source, industry))

        connection.commit()

        print("Datele au fost adăugate cu succes!")

    except Exception as e:
        print(f"Eroare la inserarea datelor: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def select_all():
    try:
        db_config = config()
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        select_all_query = 'SELECT * FROM billionaires;'
        cursor.execute(select_all_query)
        rows = cursor.fetchall()

        for row in rows:
            print(row)

    except Exception as e:
        print(f"Eroare la selectarea tuturor datelor: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    print(create_table())
    insert_data("Ana Ungurean", "$10.6 B", 30, "Romania", "IT", "IT")
    select_all()

