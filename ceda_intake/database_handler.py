import psycopg2
import os


class DBHandler:

    _max_id_length = 255
    _max_record_length = 255
    

    def __init__(self, table_name="intake_records", error_table_name="scan_errors"):
        """
        :param table_name: (str) Optional string name of the main db table.
        :param error_table_name: (str) Optional string name for the errors db table.
        """
        self.connection_info = os.environ.get("CEDA_INTAKE_DB_SETTINGS")
        if not self.connection_info:
            raise KeyError('Please create environment variable CEDA_INTAKE_DB_SETTINGS'
                           'in for format of "dbname=<db_name> user=<user_name>'
                           'host=<host_name> password=<password>"')
        
        self._test_connection()
        self.table_name = table_name
        self.error_table_name = error_table_name
        self._create_tables()


    def _test_connection(self):
        try:
            conn = psycopg2.connect(self.connection_info)
        except psycopg2.Error as err:
            print(err)
            raise ValueError('CEDA_INTAKE_DB_SETTINGS string is incorrect. Should be'
                             'in for format of "dbname=<db_name> user=<user_name>'
                             'host=<host_name> password=<password>"')

        conn.close()


    def _create_tables(self):
        """
        Creates tables if they don't already exist.
        """

        # Create main table
        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
                            f"    id varchar({self._max_id_length}) PRIMARY KEY, "
                            f"    record varchar({self._max_record_length}) NOT NULL"
                            f");")
                conn.commit()

                cur.execute(f"CREATE TABLE IF NOT EXISTS {self.error_table_name} ("
                            f"    id varchar({self._max_id_length}) PRIMARY KEY, "
                            f"    record varchar({self._max_record_length}) NOT NULL"
                            f");")
                conn.commit()



    def _delete_tables(self):
        """
        Drops the database tables
        """

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DROP TABLE {self.table_name};")
                conn.commit()
                cur.execute(f"DROP TABLE {self.error_table_name};")
                conn.commit()



    def get_record(self, identifier):
        """
        Selects the record of the job with the identifier parsed
        and returns it

        :param identifier: (str) Identifier of the job record
        :return: (str) Record of job
        """

        query = f"SELECT record FROM {self.table_name} " \
                f"WHERE id='{identifier}';"
        
        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                if cur.rowcount > 0:
                    return cur.fetchone()[0]

        return None


    def get_all_records(self):
        """
        :return: (dict) Dictionary of all job identifiers mapped to their respective records
        """

        query = f"SELECT * FROM {self.table_name}"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                record_dict = {}
                for (name, record) in cur:
                    record_dict[name] = record

        return record_dict


    def get_successful_runs(self):
        """
        :return: (str list) Returns a list of the identifiers of all successful runs
        """

        query = f"SELECT id FROM {self.table_name} " \
                "WHERE record='success';"
        
        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return [name[0] for name in cur]


    def get_failed_runs(self):
        """
        :return: (dict) Dictionary of error types mapped to lists of job identifiers which record in them
        """

        query = f"SELECT id, record FROM {self.table_name} " \
                "WHERE record<>'success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur: 
                cur.execute(query)
                failures = {}
                for (name, record) in cur:
                    failures.setdefault(record, [])
                    failures[record].append(name)

        return failures


    def delete_record(self, identifier):
        """
        Deletes entry specified by the given identifier
        from the database

        :param identifier: (str) Identifier of the job
        """

        query = f"DELETE FROM {self.table_name} " \
                f"WHERE id='{identifier}';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()


    def delete_all_records(self):
        """
        Deletes all entries from the table
        """

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {self.table_name};")
                conn.commit()


    def ran_successfully(self, identifier):
        """
        Returns true / false on whether the record with this
        identifier is successful

        :param identifier: (str) Identifier of the job record
        :return: (bool) Boolean on if job ran successfully
        """

        query = f"SELECT record FROM {self.table_name} " \
                f"WHERE id='{identifier}';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                record = cur.fetchone()
                if record is not None:
                    return record[0] == 'success'

        return False


    def count_records(self):
        """
        :return: (int) Number of records in the table
        """

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT COUNT(*) FROM {self.table_name};")

                return cur.fetchone()[0]


    def count_successes(self):
        """
        :return: (int) Number of successfull records in the table
        """

        query = f"SELECT COUNT(*) FROM {self.table_name} " \
                "WHERE record='success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return cur.fetchone()[0]


    def count_failures(self):
        """
        :return: (int) Number of failed records in the table
        """

        query = f"SELECT COUNT(*) FROM {self.table_name} " \
                "WHERE record<>'success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return cur.fetchone()[0]


    def batch_insert(self, records):
        "Batch insert records."

>>> execute_values(cur,
... "INSERT INTO test (id, v1, v2) VALUES %s",
... [(1, 2, 3), (4, 5, 6), (7, 8, 9)])



    def insert_success(self, identifier):
        """
        Inserts an entry into the table with a given identifier
        and the record 'success'

        :param identifier: (str) Identifier of the job
        """

        if self.get_record(identifier):
            self.delete_record(identifier)

        query = f"INSERT INTO {self.table_name} " \
                f"VALUES ('{identifier}', 'success');"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()


    def insert_failure(self, identifier, error_type='failure'):
        """
        Inserts an entry into the table with a given identifier
        and erroneous record

        :param identifier: (str) Identifier of the job
        :param error_type: (str) Record of the job
        """

        if self.get_record(identifier):
            self.delete_record(identifier)

        error_type = error_type[:self._max_record_length]
        
        query = f"INSERT INTO {self.table_name} " \
                f"VALUES ('{identifier}', '{error_type}');"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

