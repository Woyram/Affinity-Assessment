# Import mysql library
import os
import traceback
import mysql.connector
from app import config


class MysqlLib:
    """
    This class manages all database connections
    """

    cnx = None  # DB connection variable
    cursor = None  # DB cursor variable
    DB_NAME = ""

    # Constructor
    def __init__(
        self,
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWD,
        database_name=config.MYSQL_DATABASE,
    ):
        """
        Creates a database connection instance
        """
        try:
            if database_name != None:
                self.cnx = mysql.connector.connect(
                    user=user,
                    password=password,
                    database=database_name,
                    host=host,
                    port=port,
                )
                self.cursor = self.cnx.cursor(buffered=True, dictionary=True)
            else:
                self.cnx = mysql.connector.connect(
                    user=user, password=password, host=host, port=port
                )
                self.cursor = self.cnx.cursor(buffered=True, dictionary=True)
                pass

            self.setDB_NAME(database_name)

        except Exception as e:
            print("Error: DB Connection error")
            raise e

    def setDB_NAME(self, database_name):
        """
        This sets the DB_NAME for the connection
        Parameters: database_name => String(Name of the database)
        Returns: VOID
        """
        if database_name != None:
            self.DB_NAME = database_name

    def getDB_NAME(self):
        """
        This Returns created DB connection instance
        Parameters: VOID
        Returns: MYSQL Connection Object
        """
        return self.DB_NAME

    def getInstance(self):
        """
        This Returns created DB connection instance
        Parameters: VOID
        Returns: MYSQL Connection Object
        """
        if self.cnx != None:
            return self.cnx

    def getInstanceCursor(self):
        """
        This Returns created DB connection cursor
        Parameters: VOID
        Returns: MYSQL Connection Cursor Object
        """
        if self.cursor != None:
            return self.cursor
        pass

    def closeInstanceConnection(self):
        """
        This Returns created DB connection cursor
        Parameters: VOID
        Returns: Boolean(True for Success and Fals for Failure)
        """
        if self.cnx != None:
            self.cnx.close()
            return True
        pass

    def show_database(self):
        """
        This function creates a new database.
        Parameters: db_name  => String(Name of the database to be created)
        Returns: dictionary(True for success and False for failure)
        """
        try:
            dbs = []
            cursor = self.getInstanceCursor()
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()

            for db in databases:
                dbs.append(db["Database"])

            return dbs
        except Exception as e:
            raise e

    def create_database(self, db_name):
        """
        This function creates a new database.
        Parameters: db_name  => String(Name of the database to be created)
        Returns: Boolean(True for success and False for failure)
        """
        try:
            cursor = self.getInstanceCursor()
            # print("Creating table {0}: ".format(db_name), end='')
            cursor.execute(
                "CREATE DATABASE {0} DEFAULT CHARACTER SET 'utf8'".format(db_name)
            )
            return True
        except Exception as e:
            raise e

    def drop_database(self, db_name):
        """
        This function Drops a database.
        Parameters: db_name  => String(Name of the database to be created)
        Returns: Boolean(True for success and False for failure)
        """
        try:
            cursor = self.getInstanceCursor()
            # print("Droping Database {0}: ".format(db_name), end='')
            cursor.execute("DROP DATABASE {0}".format(db_name))
            return True
        except Exception as e:
            raise e

    def create_table(self, tables={}):
        """
        This function creates a new table.
        Parameters: table  => Dict(The key of the dictionary is the name of the table1
                            and the value is a tuple with the sql query to create the table)
        Returns: Boolean(True for success and False for failure)

        Example:
        tables = {}
        tables['dept_emp'] = (  "CREATE TABLE `dept_emp` ("
                                "  `emp_no` int(11) NOT NULL,"
                                "  `dept_no` char(4) NOT NULL,"
                                "  `from_date` date NOT NULL,"
                                "  `to_date` date NOT NULL,"
                                "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
                                "  KEY `dept_no` (`dept_no`),"
                                "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
                                "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
                                "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
                                "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
                                ") ENGINE=InnoDB")
        """
        try:
            cursor = self.getInstanceCursor()
            for name, ddl in tables.items():
                # print("Creating table {0}: ".format(name), end='')
                cursor.execute(ddl)

            return True
        except Exception as e:
            raise e

    def show_tables(self):
        """
        This function creates a new database.
        Parameters: db_name  => String(Name of the database to be created)
        Returns: dictionary(True for success and False for failure)
        """
        try:
            dbs = []
            cursor = self.getInstanceCursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            # print(tables)

            for db in tables:
                dbs.append(db["Tables_in_{0}".format(self.DB_NAME)])

            return dbs
        except Exception as e:
            raise e

    def drop_table(self, table_name):
        try:
            cursor = self.getInstanceCursor()
            # print("Droping table {0}: ".format(table_name), end='')
            cursor.execute("DROP TABLE {0}".format(table_name))

            return True
        except Exception as e:
            raise e

    def truncate_table(self, table_name):
        try:
            cursor = self.getInstanceCursor()
            # print("Truncating table {0}: ".format(table_name), end='')
            cursor.execute("TRUNCATE TABLE {0}".format(table_name))

            return True
        except Exception as e:
            raise e

    def find_one(self, table_name, condition):
        try:
            cursor = self.getInstanceCursor()
            query = f"select * from {table_name} where {condition}"
            print(query)
            cursor.execute(query)
            found = cursor.fetchone()

            return found
        except Exception as e:
            raise e
            return None

    def dump_database(self, host, password, user_name, database, output_path):
        print("Here to dump database.")
        try:
            print("Here we are!!!")
            # Form the database dump command
            dump_command = f"mysqldump -h {host} -u {user_name} -p{password} {database} > {output_path}"
            print(dump_command)

            # Execute the command
            os.system(dump_command)

            print(f"Database dump completed. File saved to: {output_path}")
            return True
        except Exception as e:
            traceback.print_exc()
            print("The error is {}".format(e))
            print(f"Database dump failed: {str(e)}")
            raise e
            return None

    def insert_in_table(self, table, fields):
        """
        This function insert data into a mysql database.
        Parameters: table  => String(Name of the table)
                    fields => Dictionary(key is table field name, value is the value to insert)
        Returns: Boolean(True for success and False for failure)
        """
        keys = ""  # contains table fields
        values = ""  # contains table values
        # print(fields)
        try:
            for key, value in fields.items():
                keys += str(key) + ","
                if value == "NOW()":
                    values += str(value) + ","
                else:
                    values += "'" + str(value) + "'" + ","

            # remove the commars from the end of the variables
            keys = keys[:-1]
            values = values[:-1]

            # print(keys)
            # print(values)
            # form Query
            query = (
                "INSERT INTO " + table + "(" + keys + ") " + "VALUES(" + values + ");"
            )
            print("QUERY IS", query)
            self.cursor.execute(query)
            self.cnx.commit()
            # return boolen true on success
            return True
        except Exception as e:
            traceback.print_exc()
            raise e
            # return False

    def insert_in_table_new(self, table, fields):
        """
        This function insert data into a mysql database.
        Parameters: table  => String(Name of the table)
                    fields => Dictionary(key is table field name, value is the value to insert)
        Returns: Boolean(True for success and False for failure)
        """
        keys = ""  # contains table fields
        values = ""  # contains table values
        # print(fields)
        try:
            for key, value in fields.items():
                keys += str(key) + ","
                if value == "NOW()":
                    values += str(value) + ","
                else:
                    values += "'" + str(value) + "'" + ","

            # remove the commars from the end of the variables
            keys = keys[:-1]
            values = values[:-1]

            # print(keys)
            # print(values)
            # form Query
            query = (
                "INSERT INTO " + table + "(" + keys + ") " + "VALUES(" + values + ");"
            )
            print("QUERY IS", query)
            self.cursor.execute(query)
            self.cnx.commit()
            # return boolen true on success
            return {"value": True, "lastRowId": self.cursor.lastrowid}
        except Exception as e:
            traceback.print_exc()
            raise e
            # return False

    def insert_in_table_ret_id(self, table, fields):
        """
        This function insert data into a mysql database.
        Parameters: table  => String(Name of the table)
                    fields => Dictionary(key is table field name, value is the value to insert)
        Returns: Boolean(True for success and False for failure)
        """
        keys = ""  # contains table fields
        values = ""  # contains table values
        # print(fields)
        try:
            for key, value in fields.items():
                keys += str(key) + ","
                if value == "NOW()":
                    values += str(value) + ","
                else:
                    values += "'" + str(value) + "'" + ","

            # remove the commars from the end of the variables
            keys = keys[:-1]
            values = values[:-1]

            # print(keys)
            # print(values)
            # form Query
            query = (
                "INSERT INTO " + table + "(" + keys + ") " + "VALUES(" + values + ");"
            )
            # print(query)
            # Excute query and process results
            self.cursor.execute(query)
            self.cnx.commit()
            insert_id = self.cursor.lastrowid
            # return boolen true on success
            return insert_id
        except Exception as e:
            raise e
            return False

    def select_from_table(self, table, fields=["*"], condition="WHERE 1"):
        """
        This function selects data form a mysql database.
        Parameters: table     => String(Name of the table)
                    fields    => List(Value is table field name)
                    condition => String(condition for selection)
        Returns: dictionary(Contains query results)
        """
        keys = ""
        try:
            for value in fields:
                keys += str(value) + ","
            # remove the commars from the end of the variables
            keys = keys[:-1]

            # print(table)
            # print(condition)
            # form Query
            query = "SELECT " + keys + " FROM " + table + " " + condition + ";"
            print(query)
            # Excute query and process results
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            # return boolen true on success
            return res
        except Exception as e:
            raise e
            return False

    def select_from_table_paged(
        self, table, fields=["*"], condition="WHERE 1", offset=0, records=10
    ):
        """
        This function selects data form a mysql database.
        Parameters: table     => String(Name of the table)
                    fields    => List(Value is table field name)
                    condition => String(condition for selection)
        Returns: dictionary(Contains query results)
        """
        keys = ""
        try:
            for value in fields:
                keys += str(value) + ","
            # remove the commars from the end of the variables
            keys = keys[:-1]

            # print(keys)
            # form Query
            query = (
                "SELECT "
                + keys
                + " FROM "
                + table
                + " "
                + condition
                + " LIMIT {}, {}".format(offset, records)
                + ";"
            )
            print("QUERY", query)
            # Excute query and process results
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            # return boolen true on success
            return res
        except Exception as e:
            raise e
            return False

    def select_distinct(self, table, fields=""):
        """
        This function selects distinct data form a mysql database.
        Parameters: table     => String(Name of the table)
                    fields    => List(Value is table field name)
        Returns: dictionary(Contains query results)
        """
        keys = ""
        try:
            keys += str(fields)
            # print(table)
            # form Query
            query = "SELECT DISTINCT(" + keys + ") FROM " + table + ";"
            # print(query)
            # Excute query and process results
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            # return boolen true on success
            return res
        except Exception as e:
            raise e
            return False

    def joint_select(
        self,
        table_main,
        join_tables=[],
        fields=["*"],
        on_condition=[],
        gen_condition="WHERE 1",
    ):
        """
        This function selects data form multiple tables using join a mysql database.
        Parameters: table_main => String(Main table name)
                    join_table => list(Name of the table) Eg.[table1, table2]
                    fields     => List(Value is table field name) Eg.["table1.field1", "table2.field1"]
                    on_condition  => String(condition for selection) Eg.["table_main.id=table2.id", "table1.id=table2.id"]
                    gen_condition  => String(condition for selection)
        Returns: dictionary(Contains query results)
        """

        if len(join_tables) == len(on_condition):
            keys = ""
            joins = ""
            tb_len = len(join_tables)
            try:
                # Loop is for the fields to select
                for value in fields:
                    keys += str(value) + ","
                # remove the commars from the end of the variables
                keys = keys[:-1]

                # Loop is for the fields to select
                for x in range(tb_len):
                    joins += (
                        "INNER JOIN " + join_tables[x] + " ON " + on_condition[x] + " "
                    )
                    pass

                # print(keys)
                # print(joins)
                # form Query
                query = (
                    "SELECT "
                    + keys
                    + " FROM "
                    + table_main
                    + " "
                    + joins
                    + " "
                    + gen_condition
                    + ";"
                )
                print(".............................")
                print(query)
                # print(query)
                # Excute query and process results
                self.cursor.execute(query)
                res = self.cursor.fetchall()
                # return boolen true on success
                return res
            except Exception as e:
                raise e
                return False
        else:
            print("join_tables and on_condition should be of the same length")
            return {
                "code": "02",
                "msg": "join_tables and on_condition should be of the same length",
            }

    def joint_select_distinct(
        self,
        table_main,
        join_tables=[],
        fields=["*"],
        on_condition=[],
        gen_condition="WHERE 1",
    ):
        """
        This function selects data form multiple tables using join a mysql database.
        Parameters: table_main => String(Main table name)
                    join_table => list(Name of the table) Eg.[table1, table2]
                    fields     => List(Value is table field name) Eg.["table1.field1", "table2.field1"]
                    on_condition  => String(condition for selection) Eg.["table_main.id=table2.id", "table1.id=table2.id"]
                    gen_condition  => String(condition for selection)
        Returns: dictionary(Contains query results)
        """

        if len(join_tables) == len(on_condition):
            keys = ""
            joins = ""
            tb_len = len(join_tables)
            try:
                # Loop is for the fields to select
                for value in fields:
                    keys += str(value) + ","
                # remove the commars from the end of the variables
                keys = keys[:-1]

                # Loop is for the fields to select
                for x in range(tb_len):
                    joins += (
                        "INNER JOIN " + join_tables[x] + " ON " + on_condition[x] + " "
                    )
                    pass

                # print(keys)
                # print(joins)
                # form Query
                query = (
                    "SELECT "
                    + keys
                    + " FROM "
                    + table_main
                    + " "
                    + joins
                    + " "
                    + gen_condition
                    + ";"
                )
                print(".............................")
                print(query)
                # print(query)
                # Excute query and process results
                self.cursor.execute(query)
                res = self.cursor.fetchall()
                # return boolen true on success
                return res
            except Exception as e:
                raise e
                return False
        else:
            print("join_tables and on_condition should be of the same length")
            return {
                "code": "02",
                "msg": "join_tables and on_condition should be of the same length",
            }

    def joint_select_paged(
        self,
        table_main,
        join_tables=[],
        fields=["*"],
        on_condition=[],
        gen_condition="WHERE 1",
        offset=0,
        records=10,
    ):
        """
        This function selects data form multiple tables using join a mysql database.
        Parameters: table_main => String(Main table name)
                    join_table => list(Name of the table) Eg.[table1, table2]
                    fields     => List(Value is table field name) Eg.["table1.field1", "table2.field1"]
                    on_condition  => String(condition for selection) Eg.["table_main.id=table2.id", "table1.id=table2.id"]
                    gen_condition  => String(condition for selection)
        Returns: dictionary(Contains query results)
        """

        if len(join_tables) == len(on_condition):
            keys = ""
            joins = ""
            tb_len = len(join_tables)
            try:
                # Loop is for the fields to select
                for value in fields:
                    keys += str(value) + ","
                # remove the commars from the end of the variables
                keys = keys[:-1]

                # Loop is for the fields to select
                for x in range(tb_len):
                    joins += (
                        "INNER JOIN " + join_tables[x] + " ON " + on_condition[x] + " "
                    )
                    pass

                # print(keys)
                # print(joins)
                # form Query
                query = (
                    "SELECT "
                    + keys
                    + " FROM "
                    + table_main
                    + " "
                    + joins
                    + " "
                    + gen_condition
                    + " LIMIT {}, {}".format(offset, records)
                    + ";"
                )
                # print(query)
                # Excute query and process results
                self.cursor.execute(query)
                res = self.cursor.fetchall()
                # return boolen true on success
                return res
            except Exception as e:
                raise e
                return False
        else:
            print("join_tables and on_condition should be of the same length")
            return {
                "code": "02",
                "msg": "join_tables and on_condition should be of the same length",
            }

    def select_count_table(self, table, condition="WHERE 1"):
        """
        This function selects data form a mysql database.
        Parameters: table     => String(Name of the table)
                    fields    => List(Value is table field name)
                    condition => String(condition for selection)
        Returns: dictionary(Contains query results)
        """
        keys = ""
        try:
            # for value in fields:
            #     keys += str(value) +","
            # #remove the commars from the end of the variables
            # keys = keys[:-1]

            # print(table)
            # print(condition)
            # form Query
            query = "SELECT COUNT(*) AS count FROM " + table + " " + condition + ";"
            # print(query)
            # Excute query and process results
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            # return boolen true on success
            return res
        except Exception as e:
            raise e
            return False

    def select_total_table(self, table, item, condition="WHERE 1"):
        """
        This function selects data form a mysql database.
        Parameters: table     => String(Name of the table)
                    fields    => List(Value is table field name)
                    condition => String(condition for selection)
        Returns: dictionary(Contains query results)
        """
        keys = ""
        try:
            # for value in fields:
            #     keys += str(value) +","
            # #remove the commars from the end of the variables
            # keys = keys[:-1]

            # print(table)
            # print(condition)
            # form Query
            query = "SELECT SUM(" + item + ") AS amount FROM " + table + " " + condition + ";"
            print(query)
            # Excute query and process results
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            # return boolen true on success
            return res
        except Exception as e:
            raise e
            return False

    def select_total_paid_table(self, table):
        """
        This function selects data form a mysql database.
        Parameters: table     => String(Name of the table)
                    fields    => List(Value is table field name)
                    condition => String(condition for selection)
        Returns: dictionary(Contains query results)
        """
        keys = ""
        try:
            # for value in fields:
            #     keys += str(value) +","
            # #remove the commars from the end of the variables
            # keys = keys[:-1]

            # print(table)
            # print(condition)
            # form Query
            query = ("select sum(transactions.amount) as amount from transactions inner join accounts on "
                     "transactions.account_id ="
                     " accounts.account_number where transactions.account_type = 'Loans' and transactions.trans_type ="
                     " 'Deposit' and accounts.account_type = 'Loans';")
            print(query)
            # Excute query and process results
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            # return boolen true on success
            return res
        except Exception as e:
            raise e
            return False

    def search_table(self, search_param, table, fields=["*"], condition=""):
        """
        This function selects data form a mysql database.
        Parameters: table     => String(Name of the table)
                    fields    => List(Value is table field name)
                    condition => String(condition for selection)
        Returns: dictionary(Contains query results)
        """
        keys = ""
        select_columns = ""
        try:
            for value in fields:
                select_columns += str(value) + ","
                keys += " " + str(value) + ' LIKE "%{0}%" OR'.format(search_param)
            # remove the commars from the end of the variables
            select_columns = select_columns[:-1]
            keys = keys[:-2]

            # print(keys)
            # form Query
            query = (
                "SELECT "
                + select_columns
                + " FROM "
                + table
                + " WHERE ("
                + keys
                + ") "
                + condition
                + ";"
            )
            print(query)
            # Excute query and process results
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            # return boolen true on success
            return res
        except Exception as e:
            raise e
            return False

    def joint_table_search(
        self,
        search_param,
        table_main,
        join_tables=[],
        fields=["*"],
        on_condition=[],
        gen_cond="",
    ):
        """
        This function selects data form multiple tables using join a mysql database.
        Parameters: table_main => String(Main table name)
                    join_table => list(Name of the table) Eg.[table1, table2]
                    fields     => List(Value is table field name) Eg.["table1.field1", "table2.field1"]
                    on_condition  => String(condition for selection) Eg.["table_main.id=table2.id", "table1.id=table2.id"]
                    gen_condition  => String(condition for selection)
        Returns: dictionary(Contains query results)
        """

        if len(join_tables) == len(on_condition):
            keys = ""
            joins = ""
            tb_len = len(join_tables)
            try:
                # Loop is for the fields to select
                for value in fields:
                    keys += str(value) + ","
                # remove the commars from the end of the variables
                keys = keys[:-1]

                # Loop is for the fields to select
                for x in range(tb_len):
                    joins += (
                        "INNER JOIN " + join_tables[x] + " ON " + on_condition[x] + " "
                    )
                    pass

                # print(keys)
                # print(joins)
                # form Query
                query = (
                    "SELECT "
                    + keys
                    + " FROM "
                    + table_main
                    + " "
                    + joins
                    + " "
                    + " WHERE Concat("
                    + keys
                    + ') LIKE "%{}%" {}'.format(search_param, gen_cond)
                    + ";"
                )
                # print(query)
                # Excute query and process results
                self.cursor.execute(query)
                res = self.cursor.fetchall()
                # return boolen true on success
                return res
            except Exception as e:
                raise e
                return False
        else:
            print("join_tables and on_condition should be of the same length")
            return {
                "code": "02",
                "msg": "join_tables and on_condition should be of the same length",
            }

    def update_table(self, table, fields, condition="WHERE 1"):
        """
        This function update data into a mysql database.
        Parameters: table => String(Name of the table)
                    fields => Dictionary(key is table field name, value is the value to insert)
                    condition => String(condition for selection)
        Returns: Boolean(True for success and False for failure)
        """
        set_value = ""  # contains table values
        try:
            for key, value in fields.items():
                if value == "NOW()":
                    set_value += str(key) + "=" + str(value) + ","
                else:
                    set_value += str(key) + "=" + "'" + str(value) + "'" + ","
            # remove the commars from the end of the variables
            set_value = set_value[:-1]
            print("Set value is: ", set_value)

            # print(set_value)
            # form Query
            query = "UPDATE " + table + " SET " + set_value + " " + condition + ";"
            print(query)
            # Excute query and process results
            self.cursor.execute(query)
            self.cnx.commit()
            # return boolen true on success
            return True
        except Exception as e:
            raise e
            return False

    def update_user_policies(self, id, policy_number, policy_holder):
        try:
            query = f"update policy set policy_number='{policy_number}' where id={id} and policy_holder={policy_holder}"
            print("QUERY", query)
            self.cursor.execute(query)
            self.cnx.commit()
            return True
        except Exception as e:
            raise e
            return False

    def get_all_transactions(self, where_condition, offset=0, records=12):
        try:
            query = f"""
            select transactions.*, policy.policy_number, policy.policy_holder, policy_holder.first_name as holder_first_name, policy_holder.last_name as holder_last_name, policy_holder.middle_name as holder_middle_name
            from transactions left outer join policy on transactions.payment_number=policy.policy_number 
            left outer join policy_holder on policy_holder.id=policy.policy_holder
            WHERE {where_condition}
            ORDER BY date DESC
            LIMIT {offset}, {records}
            """
            print("QUERY SENT", query)

            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
            return []

    def get_all_customers(self, offset=0, records=10):
        try:
            query = f"""
            SELECT * from policy_holder
            LIMIT {offset}, {records};
            """

            print("GET ALL CUSTOMERS QUERY SENT", query)

            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
            return []

    def get_all_products(self, offset=0, records=10):
        try:
            query = f"""
            SELECT * from tbl_products order by id DESC LIMIT {offset}, {records};
            """

            print("GET ALL PRODUCTS QUERY SENT", query)

            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
            return []

    def getSumOfTransaction(self, transType):
        try:
            query = f"""
            SELECT sum(amount) as amount FROM transactions WHERE payment_type = '{transType}';
            """
            print(query)
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
            return []

    def get_customer_by_policy_number(self, policy_number):
        try:
            query = f"""
            SELECT policy_holder.*, policy.policy_number from policy join policy_holder on policy.policy_holder=policy_holder.id
            WHERE policy.policy_number='{policy_number}';
            """

            print("GET CUSTOMER BY POLICY NUMBER", query)

            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
            return []

    def delete_from_table(self, table, condition="WHERE 1"):
        """
        This function selects data form a mysql database.
        Parameters: table     => String(Name of the table)
                    condition => String(condition for selection)
                    fields    => List(Value is table field name)
        Returns: dictionary(Contains query results)
        """
        try:
            # form Query
            query = "DELETE FROM " + table + " " + condition + ";"
            # print(query)
            # Excute query and process results
            self.cursor.execute(query)
            self.cnx.commit()
            # return boolen true on success
            return True
        except Exception as e:
            raise e
            return False

    # if __name__ == '__main__':
    # db = db_class(database_name=None)
    # db = db_class()

    """
    for Show database
    """
    # result = db.show_database()

    # if 'DB1' in result:
    #   db = db_class(database_name='DB1')
    # else:
    #   db.create_database('DB1')
    #   db = db_class(database_name='DB1')

    """
    for Drop database
    """
    # result = db.drop_database("pytestdb")

    """
    for Create database
    """
    # result = db.create_database()

    """
    for table database
    """
    # tables = {}
    # tables['dept_emp'] = (    "CREATE TABLE `dept_emp` (" \
    #                           "  `emp_no` int(11) NOT NULL," \
    #                              "  `dept_no` char(4) NOT NULL," \
    #                              "  `from_date` date NOT NULL," \
    #                              "  `to_date` date NOT NULL," \
    #                              "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`)," \
    #                              "  KEY `dept_no` (`dept_no`)" \
    #                              ") ENGINE=InnoDB")
    # result = db.create_table(tables)

    # '''
    # for Truncate table database
    # '''
    # result = db.truncate_table("dept_emp")

    """
    for Show tables database
    """
    # result = db.show_tables()

    """
    for Truncate table database
    """
    # result = db.drop_table("dept_emp")

    """
    for insert_in_table
    """
    # fields = {"type":"200", "name":"USER", "details":"Portal User"}
    # table = "lst_privileges_type"
    # result = db.insert_in_table(table, fields)

    """
    for select_from_table
    """
    # table = "lst_privileges_type"
    # fields = ["type", "name"]
    # condition = "WHERE type=300"
    # result = db.select_from_table(table) #returns all from the table
    # result = db.select_from_table(table, fields, condition)

    """
    for joint_select
    """
    # fields = ['topics_feeds.*', 'topics.*']
    # condition = "WHERE 1"
    # table = "topics_feeds"
    # jtables = ['topics', 'feed_delivery']
    # oncond = ['topics_feeds.t_id = topics.id', 'delivery.f_id = topics_feeds.fid']
    # result = db.joint_select(table,jtables,fields,oncond,condition)

    """
    for update_table
    """
    # table = "lst_privileges_type"
    # fields = {"type":"300"}
    # condition = "WHERE name='USER'"
    # result = db.update_table(table, fields, condition)

    """
    for delete
    """
    # result = db.delete_from_table("lst_privileges_type", "WHERE type=200")

    # db.closeInstanceConnection()
    # print(result)
