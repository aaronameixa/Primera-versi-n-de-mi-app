[app]
# Nombre de la app
title = BuscadorProductos

# Nombre del paquete (interno en Android)
package.name = buscador

# Dominio (debe ser único)
package.domain = org.example

# Código fuente
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,ttc

# Icono
icon.filename = %(source.dir)s/icon.png

# Orientación y pantalla
orientation = portrait
fullscreen = 0

# Permisos necesarios
android.permissions = INTERNET, CAMERA

# Requisitos de Python
requirements = python3,kivy,gspread,oauth2client,pandas,opencv-python,pyzbar

# Versión
package.version = 1.0
version = 1.0

# 🔹 Configuración de firma del APK (release)
android.release_keystore = keystore.jks
android.release_keyalias = $KEY_ALIAS

[buildozer]
log_level = 2
warn_on_root = 1
