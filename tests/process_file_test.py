import json
from datetime import datetime
import pandas as pd
#from modules.download_file import download_and_extract_zip

def process_excel(file_path):
    try:
        # Cargar el archivo Excel en un DataFrame de pandas
        df = pd.read_excel(file_path)
        
        # Filtrar por los departamentos IT y Marketing
        filtered_df = df[df['Department'].isin(['IT', 'Marketing'])]

        # Borrar dos columnas ('Unpaid Leaves' y 'Overtime Hours')
        filtered_df = filtered_df.drop(['Unpaid Leaves', 'Overtime Hours'], axis=1)
        
        # Acortar los nombres en la columna 'First Name' a los tres primeros caracteres
        filtered_df['First Name'] = filtered_df['First Name'].str[:3]

        # Crear una lista de nombres críticos
        critical_names = ['Ali', 'Sah', 'Sam']  # Ejemplo de nombres críticos (puedes ajustar según tus necesidades)

        # Asignar valores a 'flux critique' basado en la lista de nombres críticos
        filtered_df['flux critique'] = filtered_df['First Name'].apply(lambda x: 'critique' if x in critical_names else 'non critique')

        # Reordenar columnas para que 'flux critique' esté junto a 'First Name'
        columns = filtered_df.columns.tolist()
        columns.remove('flux critique')  # Asegurarse de que la columna no esté duplicada
        flux_critique_index = columns.index('First Name') + 1
        columns.insert(flux_critique_index, 'flux critique')
        filtered_df = filtered_df[columns]

        # Guardar el archivo procesado con la fecha actual en el nombre
        current_date = datetime.now().strftime('%d_%m_%Y')
        processed_file_path = file_path.replace('.xlsx', f'_{current_date}.xlsx')
        filtered_df.to_excel(processed_file_path, index=False)
        
        return processed_file_path
    except Exception as e:
        print(f"Error procesando el archivo Excel: {e}")
        return None
    
# Bloque de prueba que se ejecuta solo si el archivo se ejecuta directamente
if __name__ == "__main__":
    # Configuración de prueba
    file_path = "/home/rodolfo/Escritorio/Selenium/data/Employees.xlsx"  # Cambia esto a la ruta de un archivo Excel existente para probar

    # Ejecutar el procesamiento
    processed_file = process_excel(file_path)
    
    if processed_file:
        print(f"Archivo procesado guardado en: {processed_file}")
    else:
        print("El procesamiento del archivo falló.")
