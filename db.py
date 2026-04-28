import pyodbc

# FOR LEARNING: tum in details ko environment variables me bhi daal sakte ho (baad me)
SERVER = "sqlserver123.database.windows.net"
DATABASE = "demodb"
USERNAME = "azureadmin"
PASSWORD = "TeraPassword123!"

def get_db_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )
    conn = pyodbc.connect(conn_str)
    return conn