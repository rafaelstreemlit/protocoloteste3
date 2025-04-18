import streamlit as st
import psycopg2

def get_connection():
    """Create a connection to the PostgreSQL database using Streamlit secrets"""
    try:
        conn = psycopg2.connect(
            host=st.secrets["db_credentials"]["host"],
            dbname=st.secrets["db_credentials"]["database"],
            user=st.secrets["db_credentials"]["user"],
            password=st.secrets["db_credentials"]["password"],
            port=st.secrets["db_credentials"]["port"]
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def setup_database():
    """Set up the database and create the table if it doesn't exist"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Create the table 'protocolo' if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS protocolo (
                    id SERIAL PRIMARY KEY,
                    rota TEXT NOT NULL,
                    motorista TEXT NOT NULL,
                    transportadora TEXT NOT NULL,
                    pedido TEXT,
                    remessa TEXT,
                    nota_fiscal TEXT,
                    motivo TEXT,
                    data_registro DATE
                )
            ''')
            conn.commit()
        except Exception as e:
            st.error(f"Erro ao configurar o banco de dados: {e}")
        finally:
            conn.close()

def add_record(rota, motorista, transportadora, pedido, remessa, nota_fiscal, motivo, data_registro):
    """Add a new record to the database"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO protocolo (rota, motorista, transportadora, pedido, remessa, nota_fiscal, motivo, data_registro)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (rota, motorista, transportadora, pedido, remessa, nota_fiscal, motivo, data_registro))
            last_id = cursor.fetchone()[0]
            conn.commit()
            return last_id
        except Exception as e:
            st.error(f"Erro ao adicionar registro: {e}")
            return None
        finally:
            conn.close()

def view_record_by_id(id):
    """View a single record by ID"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM protocolo WHERE id=%s", (id,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            st.error(f"Erro ao consultar registro: {e}")
            return None
        finally:
            conn.close()

def view_all_records():
    """View all records in the database"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM protocolo ORDER BY id DESC")
            records = cursor.fetchall()
            return records
        except Exception as e:
            st.error(f"Erro ao consultar registros: {e}")
            return []
        finally:
            conn.close()

def delete_all_records(password):
    """Delete all records (requires password authentication)"""
    # Get the correct password from Streamlit secrets
    try:
        correct_password = st.secrets["admin"]["delete_password"]
        
        if password == correct_password:
            conn = get_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM protocolo")
                    conn.commit()
                    return True
                except Exception as e:
                    st.error(f"Erro ao excluir registros: {e}")
                    return False
                finally:
                    conn.close()
        else:
            return False
    except KeyError:
        st.error("Chave de segurança 'delete_password' não encontrada nas secrets do Streamlit.")
        return False