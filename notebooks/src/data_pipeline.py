import pandas as pd
import numpy as np
import sqlite3
# import pymongo # Se usaría en la implementación real

# --- Función 1: Simular datos de transacciones (SQL estructurado) ---
def simulate_historical_data():
    """Genera un DataFrame simple de transacciones históricas."""
    np.random.seed(42)
    n_rows = 5000
    df = pd.DataFrame({
        'transaction_id': range(1, n_rows + 1),
        'sender_id': np.random.randint(100, 999, n_rows),
        'receiver_id': np.random.randint(100, 999, n_rows),
        'amount': np.round(np.random.lognormal(2, 1.5, n_rows), 2),
        'is_fraud': np.random.choice([0, 1], n_rows, p=[0.99, 0.01]) # Desbalance
    })
    
    # Crear un pequeño grupo de fraude interconectado para el grafo
    df.loc[df.index < 50, 'is_fraud'] = 1
    df.loc[df.index < 50, 'sender_id'] = 101 # Fuente de fraude común
    
    return df

# --- Función 2: Simular logs NoSQL (para Monitoreo Continuo) ---
def simulate_nosql_logs(df_transactions):
    """Genera características no estructuradas (ej. dispositivo, IP)."""
    df_logs = df_transactions[['transaction_id', 'sender_id']].copy()
    df_logs['device_type'] = np.random.choice(['mobile', 'desktop', 'tablet'], len(df_logs))
    return df_logs.head(100) # Solo tomamos logs recientes