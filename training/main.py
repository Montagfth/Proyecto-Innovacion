import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ==========================================
# 1. TU DATASET REAL (Cargado desde tu BD o CSV)
# ==========================================
# Suponiendo que exportas tus datos a un DataFrame de Pandas:
# df = pd.read_csv('tus_datos_de_impresion.csv')

# Para este ejemplo, simulamos una fila con tu estructura exacta:
valores_ejemplo = {
    'TipoTrabajo': ['Documento', 'Afiche', 'Flyer', 'Libro'],
    'Cantidad': [26, 100, 500, 50],
    'Tamaño': ['A2', 'A3', 'A4', 'A1'],
    'Material': ['Couché', 'Bond', 'Couché', 'Cartulina'],
    'Color': [1, 0, 1, 1], # 1 = Sí, 0 = No (True/False)
    'TiempoMinutos': [45, 20, 85, 120] # Tu columna objetivo (resultado de la BD)
}
df = pd.DataFrame(valores_ejemplo)

# ==========================================
# 2. DEFINICIÓN DE VARIABLES (X e y)
# ==========================================
# X contiene las 5 variables predictoras
X = df[['TipoTrabajo', 'Cantidad', 'Tamaño', 'Material', 'Color']]
# y contiene el tiempo real que demoró
y = df['TiempoMinutos']

# Dividimos en set de entrenamiento y prueba (en producción usa un dataset grande)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# 3. PREPROCESAMIENTO CONFIGURADO
# ==========================================
# Solo aplicamos One-Hot Encoding a las columnas de texto (categóricas)
# 'Cantidad' y 'Color' se quedan tal cual porque ya son números (passthrough)
features_categoricas = ['TipoTrabajo', 'Tamaño', 'Material']

preprocesador = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), features_categoricas)
    ],
    remainder='passthrough' # Deja 'Cantidad' y 'Color' intactas
)

# ==========================================
# 4. CREACIÓN Y ENTRENAMIENTO DEL PIPELINE
# ==========================================
# Usaremos Random Forest como ejemplo principal ya que suele dar el mejor resultado
pipeline_rf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Entrenar el modelo con los datos históricos de tu BD
pipeline_rf.fit(X_train, y_train)

print("¡Modelo entrenado exitosamente con tus 5 variables!")

# ==========================================
# 5. FUNCIÓN DE PREDICCIÓN PARA TU NUEVA VARIABLE
# ==========================================
def predecir_tiempo_impresion(tipo_trabajo, cantidad, tamano, material, color):
    """
    Recibe los 5 campos exactos y retorna el tiempo estimado en minutos.
    """
    # Mapeamos "Sí" a 1 y cualquier otra cosa a 0 por si te llega como texto desde el frontend
    color_binario = 1 if color in [1, True, 'Sí', 'si', 'SI'] else 0
    
    # Creamos la estructura idéntica a la que usó el modelo para entrenar
    nuevo_caso = pd.DataFrame([{
        'TipoTrabajo': tipo_trabajo,
        'Cantidad': cantidad,
        'Tamaño': tamano,
        'Material': material,
        'Color': color_binario
    }])
    
    # El pipeline se encarga de transformar el texto a binario y predecir automáticamente
    prediccion = pipeline_rf.predict(nuevo_caso)[0]
    return round(prediccion, 2)

# --- PRUEBA CON TU EJEMPLO ---
# TipoTrabajo: Documento | Cantidad: 26 | Tamaño: A2 | Material: Couché | Color: Sí (1)
tiempo_estimado = predecir_tiempo_impresion(
    tipo_trabajo='Documento',
    cantidad=26,
    tamano='A2',
    material='Couché',
    color='Sí'
)

print(f"\nTiempo estimado para tu trabajo de ejemplo: {tiempo_estimado} minutos.")