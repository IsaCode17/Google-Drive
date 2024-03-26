from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from tkinter import Tk, filedialog

# Define los alcances de la API y el token de acceso
SCOPES = ['https://www.googleapis.com/auth/drive.file']
creds = None

# Comprueba si hay credenciales guardadas
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')

# Si no hay credenciales válidas, pide al usuario que inicie sesión
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # Guarda las credenciales para la próxima vez
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Construye el servicio de Google Drive
drive_service = build('drive', 'v3', credentials=creds)

# Solicita al usuario que seleccione el archivo localmente
root = Tk()
root.withdraw()  # Oculta la ventana principal de Tkinter
file_path = filedialog.askopenfilename()  # Abre el diálogo de selección de archivos
root.destroy()  # Cierra la ventana de Tkinter

# Sube el archivo seleccionado al Drive
if file_path:
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('Archivo subido. ID:', file.get('id'))
else:
    print('No se ha seleccionado ningún archivo.')
