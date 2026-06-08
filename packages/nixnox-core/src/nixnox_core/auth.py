# ----------------------------------------------------------------------
# Copyright (c) 2022
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# ----------------
# standard imports
# ----------------

import hashlib

# -----------
# own imports
# -----------

from nixnox_dao import AuthRole

# ------------------
# Auxiliar functions
# ------------------


def verify_password(password: str, password_hash: str) -> bool:
    """Verifica contraseña contra hash almacenado."""
    salt, stored_hash = password_hash.split("$")
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()
    return new_hash == stored_hash

############################################################################################
############################################################################################
# ESTO DE AQUI SON NOTAS PARA IMPLEMENTAR
############################################################################################
############################################################################################

def add_user(
    login: str, password: str, role: AuthRole = AuthRole.USER, full_name: str = None
) -> bool:
    """Agregar usuario a la base de datos."""
  

    conn = get_db_connection()
    try:
        api_key = secrets.token_urlsafe(32)
        if overwrite:
            conn.execute(
                """
                INSERT OR REPLACE INTO users (login, password_hash, role, full_name, api_key)
                VALUES (?, ?, ?, ?, ?)
            """,
                (login, hash_password(password), role, full_name, api_key),
            )
        else:
            conn.execute(
                """
                INSERT INTO users (login, password_hash, role, full_name, api_key)
                VALUES (?, ?, ?, ?, ?)
            """,
                (login, hash_password(password), role, full_name, api_key),
            )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(login: str, password: str) -> dict | None:
    """Autenticar usuario y devolver datos si es válido."""
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchone()
    conn.close()

    if user and verify_password(password, user["password_hash"]):
        return dict(user)
    return None


def get_user_by_api_key(api_key: str) -> dict | None:
    """Obtener usuario por API key."""
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE api_key = ?", (api_key,)).fetchone()
    conn.close()
    return dict(user) if user else None

def login_ui() -> bool:
    """Renderizar UI de login y devolver True si está autenticado."""
    if 'user_id' in st.session_state:
        return True
    
    with st.sidebar:
        st.title("🔐 Login")
        
        if 'logout_requested' in st.session_state:
            st.session_state.pop('user_id', None)
            st.session_state.pop('login', None)
            st.session_state.pop('role', None)
            st.session_state.pop('logout_requested', None)
            st.rerun()
        
        login = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar sesión"):
            user = authenticate_user(login, password)
            if user:
                st.session_state['user_id'] = user['id']
                st.session_state['login'] = user['login']
                st.session_state['role'] = user['role']
                st.session_state['full_name'] = user['full_name']
                st.success(f"¡Bienvenido, {user['login']}!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
        
        st.divider()
        if st.button("Cerrar sesión"):
            st.session_state['logout_requested'] = True
            st.rerun()
    
    return False

def require_role(required_role: str) -> bool:
    """Verificar si el usuario tiene el rol requerido."""
    if st.session_state.get('role') != required_role:
        return False
    return True

def get_all_users() -> list:
    """Obtener todos los usuarios (solo para admin)."""
    conn = get_db_connection()
    users = conn.execute(
        'SELECT id, login, role, full_name, created_at FROM users ORDER BY login'
    ).fetchall()
    conn.close()
    return [dict(user) for users]


 # pages/0_🏠_Inicio.py
import streamlit as st

st.title("🏠 Bienvenido a NIXNOX Web")
st.markdown("""
Esta es una **página pública** que no requiere autenticación.

## Características:
- 🔐 Acceso seguro para usuarios registrados
- 📊 Subida de datos personales
- ⚙️ Panel de administración
""")

if st.button("Ir al Login"):
    st.switch_page("pages/1_🔐_Login.py")


# pages/1_🔐_Login.py
import streamlit as st
from auth_utils import init_user_db, login_ui

# Inicializar DB
init_user_db()

st.title("🔐 Autenticación")

if login_ui():
    st.success("¡Ya estás logueado!")
    if st.session_state.get('role') == 'admin':
        st.info("👉 Ve a la página de Admin para gestionar usuarios")
    else:
        st.info("👉 Ve a 'Mis Datos' para subir tu información")
    
    if st.button("Actualizar página"):
        st.rerun()
else:
    st.info("👉 Completa el formulario en el sidebar para iniciar sesión")

# pages/2_📊_Mis_Datos.py
import streamlit as st
from auth_utils import init_user_db, login_ui

# Inicializar DB
init_user_db()

# Verificar autenticación
if not login_ui():
    st.warning("⚠️ Debes iniciar sesión para ver esta página.")
    st.stop()

# Verificar que esté logueado (cualquier rol)
st.title(f"📊 Mis Datos - {st.session_state.get('login')}")
st.write(f"Rol: **{st.session_state.get('role')}**")

st.divider()

st.subheader("📤 Subir tus datos")
uploaded_file = st.file_uploader("Selecciona un archivo", type=['csv', 'txt', 'json'])

if uploaded_file:
    st.success(f"Archivo subido: {uploaded_file.name}")
    # Aquí adds tu lógica para procesar el archivo
    # st.dataframe(pd.read_csv(uploaded_file))

st.divider()
st.info("💡 Esta página es accesible para todos los usuarios autenticados.")

# pages/3_⚙️_Admin_Usuarios.py
import streamlit as st
import pandas as pd
from auth_utils import init_user_db, login_ui, require_role, add_user, get_all_users

# Inicializar DB
init_user_db()

# Verificar autenticación
if not login_ui():
    st.warning("⚠️ Debes iniciar sesión para ver esta página.")
    st.stop()

# Verificar rol admin
if not require_role('admin'):
    st.error("🚫 **Acceso denegado**: Solo los administradores pueden ver esta página.")
    st.stop()

st.title("⚙️ Admin — Gestión de Usuarios")

# Crear/actualizar usuario
st.subheader("➕ Crear / Actualizar Usuario")
with st.form("create_user"):
    login = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    role = st.selectbox("Rol", ["admin", "user"])
    full_name = st.text_input("Nombre completo (opcional)")
    overwrite = st.checkbox("Sobrescribir si existe")
    
    submitted = st.form_submit_button("Crear / Actualizar usuario")
    
    if submitted:
        if login and password:
            try:
                if add_user(login, password, role=role, full_name=full_name, overwrite=overwrite):
                    st.success(f"✅ Usuario {login} guardado como {role}")
                else:
                    st.error("❌ Error: El usuario ya existe")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.error("⚠️ Username y password son obligatorios")

st.divider()

# Listar usuarios
st.subheader("📋 Usuarios existentes")
conn = sqlite3.connect("users.db")
df_users = pd.read_sql_query(
    "SELECT login, role, full_name, created_at FROM users ORDER BY login", 
    conn
)
conn.close()
st.dataframe(df_users)
