# server/set_admin.py

import firebase_admin
from firebase_admin import credentials, auth

# --- GANTI DENGAN EMAIL ANDA ---
ADMIN_EMAIL = "falahfahrur@gmail.com"
# -----------------------------

# Path ke file kunci rahasia Anda
CRED_PATH = "serviceAccountKey.json"

try:
    # Inisialisasi Firebase Admin SDK
    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK berhasil diinisialisasi.")

    # Dapatkan data pengguna berdasarkan email
    print(f"Mencari pengguna dengan email: {ADMIN_EMAIL}...")
    user = auth.get_user_by_email(ADMIN_EMAIL)
    
    # Tetapkan custom claim 'admin' pada pengguna tersebut
    auth.set_custom_user_claims(user.uid, {'admin': True})
    
    print(f"✅ Berhasil! Pengguna '{ADMIN_EMAIL}' (UID: {user.uid}) telah dijadikan admin.")
    print("Silakan login ulang di aplikasi untuk melihat perubahan.")

except Exception as e:
    print(f"❌ Terjadi kesalahan: {e}")
    print("Pastikan email pengguna sudah terdaftar di Firebase Authentication dan path ke serviceAccountKey.json sudah benar.")