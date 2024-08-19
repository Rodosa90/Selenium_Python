import json
from modules.download_file import download_and_extract_zip
from modules.process_file import process_excel
from modules.send_email import send_email

def main():
    # Cargar configuración
    with open('config.json') as config_file:
        config = json.load(config_file)

    download_dir = config["download_dir"]
    kaggle_username = config["kaggle_username"]
    kaggle_password = config["kaggle_password"]

    smtp_config = config["smtp"]

    # Descargar y extraer archivo
    downloaded_file = download_and_extract_zip(download_dir, kaggle_username, kaggle_password)
    if downloaded_file:
        print(f"Archivo descargado: {downloaded_file}")

        # Procesar archivo
        processed_file = process_excel(downloaded_file)
        if processed_file:
            print(f"Archivo procesado: {processed_file}")

            # Enviar correo con el archivo procesado adjunto
            send_email(
                smtp_config["sender_email"],
                smtp_config["receiver_email"],
                smtp_config["subject"],
                smtp_config["body"],
                processed_file,  # Archivo adjunto
                smtp_config["smtp_server"],
                smtp_config["smtp_port"],
                smtp_config["login"],
                smtp_config["password"]
            )
        else:
            print("El procesamiento del archivo falló.")
    else:
        print("La descarga del archivo falló.")

if __name__ == "__main__":
    main()
