# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import psycopg2

def print_hi():
    connection = psycopg2.connect(host="192.168.2.101", port=5432, database="testdb", user="postgres", password="postgres")
    cur = connection.cursor()
    cur.execute("SELECT datname,usename,client_addr,client_port FROM pg_stat_activity;")
    query_results = cur.fetchall()
    print(query_results)
    cur.close()
    connection.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()


