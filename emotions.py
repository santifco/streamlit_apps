import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from workalendar.america import Argentina
import math
from scipy.stats import norm
from datetime import datetime, timedelta
from io import BytesIO
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from pathlib import Path
from google.oauth2 import service_account

# Configuración inicial de la página de Streamlit
st.set_page_config(page_title="Registro de Pensamientos Negativos", layout="wide")

# Título de la aplicación
st.title("Registro de Pensamientos Negativos")

credentials_info = st.secrets["gcp_service_account"]
# Información de autenticación para Google Sheets
# credentials_info = {
#     "type": "service_account",
#     "project_id": "inbound-pattern-429101-c5",
#     "private_key_id": "9dcc01743c917fb186294a8c6d228d4c2fb005bc",
#     "private_key": """-----BEGIN PRIVATE KEY-----
# MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDPvpK+357PGmvc
# 6jxJTHyKfpUs/2861MGvfClaGMjEw9G8YmeeeH8PAkc/rZxaHpl2zcmpUQfTauxs
# 0mhbOD42jxRflbdi00yvHVkBBtYdzfvtGwepEUsP26yqOySm6PiVI/XKHWdct61B
# 28l/VW+mjXDVPiDiMATQRTJi4tYTgC5eSjhnkT4efY7gUMHmO2057cI+jmRob1WV
# PEEWLGt76R4IGnH/FtoW2B6lPoOb7KefRx2WgHfTu+zsXvqmbGbgRLSlheG4Zb6g
# h0dZXcyojx5vGgJT3ty4o5XgpA6n9EH2uURDXUBYQ9KE8mcNDM9VK6KQEYeBmIJr
# QOvMftM1AgMBAAECggEAAn4NSNdS4/vtzVvknLk+SUTmmuklQvARPtBfK1zqZSza
# cQ1XARha/p3r7ReQCpAFyJinRharmulIrFJJjmmF4HdUnycjIxxNUyH5GJLgJpM1
# cY1Ad6PNkKZSsKH41iVDCGk3N8mk4tH5rynGKKViwreabZX5sEuQdiEIlRXchgLN
# ransgsarOU/8+RI2W5JRt7wPAO56WsZc+zeOIyLS7RScibfdi8wMQYZF7PsPB5EG
# 6ps50hxHWZ18lgLgJO5iK6YZkINHwW8AWDaxonxTgn4eYT8iUDMol8D5i2AXM5x1
# JnRzhLKnNUdzug4RB7XrcCOsjoDOU2dW1VbXTNkyxQKBgQD4WbO23ktbkl64dmdA
# ZKhRSRcBfbUf8/+Olp8Dt/PTb53Rjvsm3XK5EUK6t9oMGgL131UuOcKysV1RCyzT
# I5jjiY5Q3Ws2L0N2IFfxSBI7Di2hxSWLaXgETsMUV0MBfv1TH/8E+3tEtoj26lZY
# A0GVOrGprEJVNcL3X3T83R3mNwKBgQDWJK8icbaJujm9HfXi9ODcG7YpPYKRcqJa
# LZclOiccRHIUN4SzouIfB6kp63k96W5Yzm6GeRgaiB/LQNPNTDFO4Q7Zrm7wci9o
# kzRUHWJcgKl7r8Q+TYXBPJVn0dZe65G5O/d+7cmQn+MUp0Gi5cnYu9eaeKHoJGY0
# P6vCKhab8wKBgC2cK8k14hkbNJIkDKpi0ha7maIIeC86HIEPYHzKV9lI8m7+F1n3
# 6Y3bganRAhae4FRPg9FNglhXApBTwRO1wepn5N8tCveUjosvPXduiQqXfAHttwt3
# fzcrT+B4djHcJKITij5cATOJYnYWa20WjADgGqjSngwQJ5JO0alu4oLZAoGAD138
# j203mzSY9iBTR+EozcLTVKxMVWGzkuMYqJw+uEGVKiw9wqJatb1X/2EdhzrcJ1VR
# Cydfem/wUCarzFy+YRm3dhmVbn3TNx7xL2QYbejxwKWBYLMxeQd+9T9SsecXwwIx
# pZMs1ssSgaXrCOSSkpIQS86CV+VczD0Rd1KL4s8CgYEAhfI92S/3eL6eOkm7yHL1
# 4331R/gomiO4QehLpyUZfirpqxNO/8BL6f25Jp5cC3dJeNu4xEbbMIMpEpT9C+ZJ
# 4WWYzDCC43HB8AbA8SgMDz7Vaa6h9zHJolLLrcsDMtiD4JT7VeV4UluWXIaRbg6p
# XYwWQL2d6uGePDriQHXIUmY=
# -----END PRIVATE KEY-----""",
#     "client_email": "google-sheets-api@inbound-pattern-429101-c5.iam.gserviceaccount.com",
#     "client_id": "107649396128661753097",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-sheets-api%40inbound-pattern-429101-c5.iam.gserviceaccount.com",
#     "universe_domain": "googleapis.com"
# }

# Configurar los scopes correctos
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_info(credentials_info, scopes=scopes)

# Autenticar cliente de Google Sheets
client = gspread.authorize(creds)

# ID de la hoja de Google Sheets
sheet_id = '11cB0mKzeECOTx87zOOVXVrT0EJ_x5lQNL3m_PEQuPEg'  # Reemplaza con tu sheet_id real

# Abre la hoja de Google Sheets
sheet = client.open_by_key(sheet_id).sheet1

# Opciones predefinidas de pensamientos negativos
opciones_pensamientos = [
    "Que va a pensar x de esto",
    "A nadie le importa lo que hago",
    "No soy lo suficientemente interesante",
    "No me se expresar bien",
    "No soy lo suficientemente bueno",
]

# Formulario para seleccionar pensamientos negativos
st.subheader("Registrar Pensamiento Negativo")
pensamiento_seleccionado = st.selectbox("Selecciona el pensamiento negativo", opciones_pensamientos)

if st.button("Registrar"):
    if not pensamiento_seleccionado:
        st.error("Debes seleccionar un pensamiento.")
    else:
        # Registrar el pensamiento con fecha y hora
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([fecha_hora, pensamiento_seleccionado])
        st.success("¡Pensamiento registrado con éxito!")

# Mostrar los últimos pensamientos registrados
st.subheader("Últimos Pensamientos Registrados")
data = sheet.get_all_records()
df = pd.DataFrame(data)
if not df.empty:
    st.dataframe(df)
else:
    st.write("No hay pensamientos registrados aún.")
