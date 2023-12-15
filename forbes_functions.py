
def get_top_10_youngest_billionaires(billionaires_db):
    try:
        billionaires_db.connect()
        query = '''
            SELECT * FROM billionaires
            ORDER BY age ASC
            LIMIT 10;
        '''
        billionaires_db.cursor.execute(query)
        top_10_youngest = billionaires_db.cursor.fetchall()
        list_top_10_youngest = []
        for billionaire in top_10_youngest:
            list_top_10_youngest.append(billionaire)
        return list_top_10_youngest
    except Exception as e:
        print(f"An error occurred while getting the top 10 youngest billionaires: {e}")
    finally:
        billionaires_db.disconnect()


def count_citizenship(billionaires_db, is_american=True):
    try:
        billionaires_db.connect()
        if is_american:
            condition = "citizenship = 'United States'"
        else:
            condition = "citizenship != 'United States'"
        query = f'''
            SELECT COUNT(*) FROM billionaires WHERE {condition}
        '''
        billionaires_db.cursor.execute(query)
        count = billionaires_db.cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"An error occurred while counting data from the database: {e}")
    finally:
        billionaires_db.disconnect()


def get_top_10_philanthropists(billionaires_db):
    try:
        billionaires_db.connect()
        query = '''
            SELECT * FROM billionaires
            WHERE philanthropy_score IS NOT NULL
            ORDER BY philanthropy_score DESC
            LIMIT 10;
        '''
        billionaires_db.cursor.execute(query)
        top_10_philanthropists = billionaires_db.cursor.fetchall()
        list_top_10_philanthropists = []
        for billionaire in top_10_philanthropists:
            list_top_10_philanthropists.append(billionaire)
        return list_top_10_philanthropists
    except Exception as e:
        print(f"An error occurred while getting the top 10 philanthropists: {e}")
    finally:
        billionaires_db.disconnect()

