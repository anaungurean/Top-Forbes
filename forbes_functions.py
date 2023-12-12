
def get_top_10_youngest_billionaires(billionaires_db):
    try:
        billionaires_db.connect()
        billionaires_db.cursor.execute(
            '''
            SELECT * FROM billionaires
            ORDER BY age ASC
            LIMIT 10;
            '''
        )
        top_10_youngest = billionaires_db.cursor.fetchall()
        return top_10_youngest
    except Exception as e:
        print(f"An error occurred while getting the top 10 youngest billionaires: {e}")
    finally:
        billionaires_db.disconnect()


def count_citizenship(billionaires_db, is_american = True):
    try:
        billionaires_db.connect()
        condition = "citizenship = 'United States'" if is_american else "citizenship != 'United States'"
        count_query = f'''
            SELECT COUNT(*) FROM billionaires WHERE {condition}
        '''
        billionaires_db.cursor.execute(count_query)
        count = billionaires_db.cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"An error occurred while counting data from the database: {e}")
    finally:
        billionaires_db.disconnect()

def get_top_10_philanthropists(billionaires_db):
    try:
        billionaires_db.connect()
        billionaires_db.cursor.execute(
            '''
            SELECT * FROM billionaires
            WHERE philanthropy_score IS NOT NULL
            ORDER BY philanthropy_score DESC
            LIMIT 10;
            '''
        )
        top_10_philanthropists = billionaires_db.cursor.fetchall()
        return top_10_philanthropists
    except Exception as e:
        print(f"An error occurred while getting the top 10 philanthropists: {e}")
    finally:
        billionaires_db.disconnect()

