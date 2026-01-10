[app]

title = Medicine Tracker
package.name = medicinetracker
package.domain = com.pushpesh
version = 1.0.0

source.dir = .
source.main = main.py

requirements = python3,kivy==2.3.1,Pillow,requests,python-dateutil

icon.filename = icon.png
presplash.filename = presplash.png

orientation = portrait

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.arch = armeabi-v7a, arm64-v8a

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.copy_libs = 1
android.entrypoint = org.kivy.android.PythonActivity

p4a.bootstrap = sdl2

# 🔥 CRITICAL FIX (stops libffi autoreconf crash)
android.skip_update = libffi

log_level = 2