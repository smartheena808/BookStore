import psycopg2

connectionstring = "dbname='postgres' user='postgres' password='postgres123' host='localhost' port='5432'"

class Database:

    def delete_table():
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("DROP TABLE IF EXISTS SmartStoreDB")
        conn.commit()
        conn.close()

    def create_table():
        query = f"""CREATE TABLE IF NOT EXISTS SmartStoreDB(
            title TEXT NOT NULL,
            author TEXT,
            year INTEGER,
            ISBN VARCHAR(20) NOT NULL UNIQUE)"""

        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute(query)
        conn.commit()
        conn.close()

    def insert_entry(booktitle, bookauthor, year, isbn):
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("INSERT INTO SmartStoreDB(title, author, year, ISBN) VALUES ('%s','%s','%s','%s')" %(booktitle, bookauthor, year, isbn))
        conn.commit()
        conn.close()

    def view_data():
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("SELECT * FROM SmartStoreDB")
        rows = curr.fetchall()
        conn.close()
        return rows    

    def delete_title(title):
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("DELETE FROM SmartStoreDB WHERE title='%s'" % (title,) )
        conn.commit()
        conn.close()

    def delete_author(author):
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("DELETE FROM SmartStoreDB WHERE author='%s'" % (author,) )
        conn.commit()
        conn.close()           

    def delete_isbn(isbn):
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("DELETE FROM SmartStoreDB WHERE ISBN='%s'" % (isbn,) )
        conn.commit()
        conn.close()     

    def search_by_title(title):
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("SELECT * FROM SmartStoreDB WHERE title LIKE '%s%s'" %(title,'%'))
        rows = curr.fetchall()
        conn.close()
        return rows  

    def search_by_author(author):
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("SELECT * FROM SmartStoreDB WHERE author LIKE '%s%s'" %(author,'%'))
        rows = curr.fetchall()
        conn.close()
        return rows

    def search_by_year(year):
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("SELECT * FROM SmartStoreDB WHERE year ='%s'" % (year,))
        rows = curr.fetchall()
        conn.close
        return rows

    def search_by_isbn(isbn):
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("SELECT * FROM SmartStoreDB WHERE ISBN ='%s'" % (isbn,))
        rows = curr.fetchall()
        conn.close
        return rows

    def update_data(title, author, year, isbn):
        conn = psycopg2.connect(connectionstring)
        curr = conn.cursor()
        curr.execute("UPDATE SmartStoreDB SET title ='%s', author='%s', year='%s' WHERE ISBN='%s'" %(title, author, year, isbn))
        conn.commit()
        conn.close()

"""    
def delete_table():
    conn = psycopg2.connect(connectionstring)
    curr = conn.cursor()
    curr.execute("DROP TABLE IF EXISTS SmartStoreDB")
    conn.commit()
    conn.close()

delete_table()    

""" 
