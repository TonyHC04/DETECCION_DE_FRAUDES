import sys
import os
import pprint

print("--- DIAGNÓSTICO DE RUTA DE PYTHON ---")

# 1. Mostrar la carpeta de trabajo actual del script (debería ser el directorio raíz)
print(f"Directorio Actual (CWD): {os.getcwd()}")
print("-" * 30)

# 2. Intentar importar data_pipeline directamente
try:
    print("Intento de importación simple...")
    import data_pipeline
    print("✅ ¡Éxito! El módulo se encontró.")

except ImportError as e:
    print("❌ Fallo en la importación simple.")
    print("Razón: El directorio 'src' no está incluido por defecto.")
    print("-" * 30)
    
    # 3. Mostrar TODAS las rutas donde Python está buscando módulos
    print("Rutas de Búsqueda de Python (sys.path):")
    
    # Intentamos añadir la ruta relativa 'src' y 'notebooks'
    # NOTA: Si ejecutas este archivo desde la raíz, debes ver './src' y './notebooks'
    
    sys.path.append(os.path.join(os.getcwd(), 'src'))
    sys.path.append(os.path.join(os.getcwd(), 'notebooks'))
    
    # Usamos pprint para imprimir la lista de rutas
    pprint.pprint(sys.path)