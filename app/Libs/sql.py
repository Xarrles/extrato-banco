import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            dbname="Ofx_Reader",  # Nome do banco que você criou no pgAdmin
            user="postgres",      # Usuário padrão do PostgreSQL
            password="pg1258", # senha usuario
            host="localhost",     # Servidor local
            port="5432",
            #encode = 'utf8'
        )
        print("Conexão bem-sucedida!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar: {str(e)}")
        return None
