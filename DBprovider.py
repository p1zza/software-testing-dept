import random
import string

import psycopg2

class DBProvider:

    headings = []
    userdata = []
    name = ""
    userNames = []
    privelegies = []

    def __init__(self,name):
        self.name = name

    def get_privelegies(self,cur,user):
        expression = str("SELECT table_catalog, table_schema, table_name, privilege_type FROM information_schema.table_privileges WHERE grantee = '{0}';").format(user)
        cur.execute(expression)
        self.privelegies.append(cur.fetchall())

    def get_users(self, cur):
        cur.execute("select * from pg_shadow;")
        description = list(cur.description)
        for names in description:
             self.headings.append(names.name)


        users = list(cur.fetchall())
        for user in users:
            self.userNames.append(user[0])
            for userdata in user:
                self.userdata.append(userdata)


