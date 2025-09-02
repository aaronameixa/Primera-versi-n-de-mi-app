[app]
title = BuscadorProductos
package.name = buscador
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,ttc
icon.filename = %(source.dir)s/icon.png
orientation = all
fullscreen = 0
android.permissions = INTERNET, CAMERA
requirements = python3,kivy,gspread,oauth2client,pandas,opencv-python,pyzbar
package.version = 1.0
version = 1.0

[buildozer]
log_level = 2
warn_on_root = 1
