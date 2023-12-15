from configparser import ConfigParser
import psycopg2


def load_configuration(filename, section):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db


class DatabaseConnector:
    def __init__(self, filename='database.ini', section='postgresql'):
        self.db_config = load_configuration(filename, section)
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")

    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            print(f"An error occurred while disconnecting from the database: {e}")

    def create_table(self):
        try:
            self.connect()
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS billionaires(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    net_worth VARCHAR(20),
                    age INT,
                    source_of_wealth VARCHAR(255),
                    self_made_score INT,
                    philanthropy_score INT,
                    residence VARCHAR(255),
                    citizenship VARCHAR(255),
                    marital_status VARCHAR(255),
                    children INT,
                    education VARCHAR(255)
                );
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Table created successfully!")
        except Exception as e:
            print("An error occurred while creating the table : {e}")
        finally:
            self.disconnect()

    def insert_data(self, name, net_worth, age, source_of_wealth, self_made_score, philanthropy_score, residence,
                    citizenship, marital_status, children, education):
        try:
            self.connect()
            insert_query = '''
                INSERT INTO billionaires (name, net_worth, age, source_of_wealth, self_made_score, philanthropy_score, residence, 
                citizenship, marital_status, children, education)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''
            self.cursor.execute(insert_query, (name, net_worth, age, source_of_wealth, self_made_score,
                                               philanthropy_score, residence, citizenship, marital_status, children,
                                               education))
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred while inserting data into the database: {e}")
        finally:
            self.disconnect()

    def delete_all_data(self):
        try:
            self.connect()
            delete_query = '''
                DELETE FROM billionaires;
            '''
            self.cursor.execute(delete_query)
            self.connection.commit()
            print("Data deleted successfully!")
        except Exception as e:
            print(f"An error occurred while deleting data from the database: {e}")
        finally:
            self.disconnect()











