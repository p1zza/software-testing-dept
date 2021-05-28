import random
import string
import paramiko
import psycopg2

class DBProvider:

    headings = []
    userdata = []
    name = ""
    userNames = []
    privelegies = []
    projects = []
    projectslist = []
    projectpath = ""

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

    def get_projects(self,cur):
        expression = str("select * from project;")
        cur.execute(expression)
        self.projects.append(cur.fetchall())
        expression = str("select projectname from project;")
        cur.execute(expression)
        res = cur.fetchall()
        for a in res:
            self.projectslist.append(a)

    def getPathbyProj(self,cur,projname):
        expression = str(f"select path from project where projectname = '{projname[0]}';")
        cur.execute(expression)
        self.projectpath = cur.fetchall()






