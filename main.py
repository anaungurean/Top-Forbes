from ForbesScrapper import ForbesScraper
from DatabaseConnector import DatabaseConnector
from forbes_functions import get_top_10_youngest_billionaires
from prettytable import PrettyTable
from forbes_functions import count_citizenship
from forbes_functions import get_top_10_philanthropists


def format_as_table(billionaires_info):
    table = PrettyTable()
    table.field_names = ['Id', 'Name', 'Net Worth', 'Age', 'Source of Wealth', 'Self-Made Score',
                         'Philanthropy Score', 'Residence', 'Citizenship', 'Marital Status',
                         'Children', 'Education']

    for billionaire in billionaires_info:
        table.add_row(billionaire)
    return table


if __name__ == "__main__":
    scraper = ForbesScraper()
    scraper.run_scraper()
    db_connector = DatabaseConnector()
    top_10_youngest = get_top_10_youngest_billionaires(db_connector)
    print("Top 10 youngest billionaires:")
    print(format_as_table(top_10_youngest))
    number_american_billionaire = count_citizenship(db_connector,True)
    number_not_american_billionaire = count_citizenship(db_connector,False)
    print(f"Number of American billionaires: {number_american_billionaire}")
    print(f"Number of not American billionaires: {number_not_american_billionaire}")
    print("Top 10 philanthropists:")
    top_10_philanthropists = get_top_10_philanthropists(db_connector)
    print(format_as_table(top_10_philanthropists))




