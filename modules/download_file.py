import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json

def download_and_extract_zip(download_dir, kaggle_username, kaggle_password):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': download_dir}
    chrome_options.add_experimental_option('prefs', prefs)

    try:
        # Inicializa el webdriver utilizando webdriver_manager para gestionar el driver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Navegar a la página de inicio de sesión de Kaggle
        driver.get("https://www.kaggle.com/account/login")
        
        # Esperar a que la opción de "Sign in with Email" esté disponible y hacer clic en ella
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Sign in with Email")]'))).click()
        
        # Ingresar el nombre de usuario y la contraseña
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(kaggle_username)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(kaggle_password)
        
        # Hacer clic en el botón de inicio de sesión
        driver.find_element(By.XPATH, '//span[contains(text(), "Sign In")]').click()
        
        # Esperar a que la sesión se inicie y redirigir a la página del dataset
        WebDriverWait(driver, 20).until(EC.title_contains("Home"))
        driver.get('https://www.kaggle.com/datasets/abdallahwagih/company-employees')

        try:
            wait = WebDriverWait(driver, 20)
            # Encuentra el enlace de descarga basado en el texto "Download (70 kB)"
            download_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Download")]')))
            download_link.click()
            print("Enlace de descarga clickeado, esperando a que se complete la descarga...")
            time.sleep(15)  # Espera más tiempo para asegurarte de que la descarga se complete
        finally:
            driver.quit()

        # Imprimir todos los archivos en la carpeta de descargas
        print("Archivos en la carpeta de descargas después de la descarga:")
        for filename in os.listdir(download_dir):
            print(filename)

        # Retorna el nombre del archivo .zip descargado
        zip_path = None
        for filename in os.listdir(download_dir):
            if filename.endswith('.zip'):
                zip_path = os.path.join(download_dir, filename)
                print(f"Archivo zip encontrado: {zip_path}")
                break

        if zip_path is None:
            print("No se encontró el archivo .zip descargado.")
            return None

        # Extraer el archivo .zip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(download_dir)

        # Buscar y retornar el archivo .xlsx dentro del contenido extraído
        for filename in os.listdir(download_dir):
            if filename.endswith('.xlsx'):
                return os.path.join(download_dir, filename)

        print("No se encontró el archivo .xlsx en el .zip extraído.")
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Cargar la configuración desde el archivo config.json
    with open('config.json') as config_file:
        config = json.load(config_file)

    download_dir = config["download_dir"]
    kaggle_username = config["kaggle_username"]
    kaggle_password = config["kaggle_password"]

    downloaded_file = download_and_extract_zip(download_dir, kaggle_username, kaggle_password)
    if downloaded_file:
        print(f"Archivo descargado y extraído: {downloaded_file}")
    else:
        print("No se pudo descargar o extraer el archivo.")
