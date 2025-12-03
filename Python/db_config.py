from sqlalchemy import create_engine

server = r'MOE-2635896356\SQLEXPRESS'
database = 'Ex'
username = r'MOE-2635896356\IMOE001'
password = ''
driver = 'ODBC Driver 18 for SQL Server'

conn_str = (
    f"mssql+pyodbc://@{server}/{database}"
    f"?driver={driver}"
    f"&Trusted_Connection=yes"
    f"&Encrypt=yes"
    f"&TrustServerCertificate=yes"
)

def get_engine():
    return create_engine(conn_str)