import database

# for testing individual methods without
# having to run everything at once

# FLASK commands:
#
# start envir:
# venv\Scripts\activate
#
# start FLASK:
# $env:FLASK_APP = "main"
# $env:FLASK_DEBUG = "development"
# flask run

def main():
    database.connect()
    print(database.getProjectParts(1))
    database.close()

if __name__ == '__main__':
    main()
