from ceda_intake.database_handler import DBHandler
import os



dbh = None



def setup_module():
    os.environ["CEDA_INTAKE_DB_SETTINGS"] = open(".postgres_credentials").read()

    global dbh
    dbh = DBHandler()


def test_create_db():
    assert isinstance(dbh, DBHandler) 


def teardown_module():
    del os.environ["CEDA_INTAKE_DB_SETTINGS"]
