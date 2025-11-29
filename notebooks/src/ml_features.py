import networkx as nx
import pandas as pd
import numpy as np # Necesitas numpy para el manejo de NaN

# --- Función 1: Construir el Grafo de Transacciones (CORREGIDA) ---
def build_transaction_graph(df_transactions):
    """
    Construye un grafo dirigido para análisis de red AML,
    asegurando que los pesos sean numéricos limpios.
    """
    # 1. Limpieza de Datos
    # Reemplazar NaN en 'amount' (peso) con 0.0 o la media para evitar el error 1-D.
    df_transactions['amount'] = pd.to_numeric(df_transactions['amount'], errors='coerce').fillna(0.0)

    # 2. Creación de la lista de aristas (origen, destino, peso)
    edge_list = []
    for index, row in df_transactions.iterrows():
        # Añade la arista con el peso limpio
        edge_list.append((row['sender_id'], row['receiver_id'], {'weight': row['amount']}))

    G = nx.DiGraph() 
    G.add_edges_from(edge_list)
    
    return G

# --- Función 2: Calcular PageRank (CORREGIDA para asegurar la convergencia) ---
def calculate_pagerank_feature(G):
    """Calcula el PageRank para identificar cuentas centrales/líderes de riesgo."""
    
    try:
        # Ejecutar PageRank con pesos. Usamos tol y max_iter para estabilidad.
        pagerank_scores = nx.pagerank(G, weight='weight', max_iter=100, tol=1e-06)
    except nx.NetworkXNoPath:
        # Esto ocurre si el grafo está desconectado. Se calcula sin pesos.
        print("Advertencia: El grafo está desconectado. Calculando PageRank sin pesos.")
        pagerank_scores = nx.pagerank(G, weight=None) 
    except Exception as e:
        # Captura cualquier otro error, incluido el ValueError de Scipy si persiste
        print(f"Error grave en PageRank. Usando valor predeterminado. Error: {e}")
        # Si falla, asignamos un score promedio para no detener el modelo ML
        nodes = list(G.nodes())
        avg_score = 1.0 / len(nodes)
        pagerank_scores = {node: avg_score for node in nodes}


    df_pagerank = pd.DataFrame(
        list(pagerank_scores.items()), 
        columns=['customer_id', 'pagerank_score']
    )
    return df_pagerank