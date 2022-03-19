from Persistence.databaseconfig import DataBaseConfigReader
from Persistence.repository import Repository
from Persistence.queries import SELECT_ALL_REVIEWS

def main ():
    reader = DataBaseConfigReader()
    config = reader.read_db_config('databaseconfig.json')
    repository = Repository(config)

    results = repository.execute_query(SELECT_ALL_REVIEWS)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()