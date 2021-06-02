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
    tables = []
    uniquetables = []
    privtypes = []
    uniqueprivtypes = []
    execresult = ""

    def __init__(self,name):
        self.name = name

    def get_privelegies(self,cur,user):
        expression = str("select table_catalog, table_schema, table_name, privilege_type from information_schema.table_privileges where grantee = '{0}';").format(user)
        cur.execute(expression)
        self.privelegies.append(cur.fetchall())


        exprtables = str("select table_name from information_schema.table_privileges where grantee = '{0}';").format(user)
        cur.execute(exprtables)
        self.tables = list(cur.fetchall())
        for table in self.tables:
            if table in self.uniquetables:
                continue
            else:
                self.uniquetables.append(table)

        privrtables = str("select privilege_type from information_schema.table_privileges where grantee = '{0}';").format(user)
        cur.execute(privrtables)
        self.privtypes = list(cur.fetchall())
        for priv in self.privtypes:
            if priv in self.uniqueprivtypes:
                continue
            else:
                self.uniqueprivtypes.append(priv)

    def prev_exec(self,cur,stringexec):
        cur.execute(stringexec)
        self.execresult = cur.fetchall()




    def get_users(self, cur):
        cur.execute("select * from pg_shadow;")
        description = list(cur.description)
        self.headings = []
        for names in description:
             self.headings.append(names.name)


        users = list(cur.fetchall())
        self.userdata = []
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

    def getpathbyproj(self,cur,projname):
        expression = str(f"select path from project where projectname = '{projname[0]}';")
        cur.execute(expression)
        self.projectpath = cur.fetchall()

    def usercreate(self, cur, strtoexec):
        cur.execute(strtoexec)
        self.execresult = ""
        self.execresult = cur.fetchall()





