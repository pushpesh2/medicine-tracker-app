[app]

# (str) Title of your application
title = Medicine Tracker

# (str) Package name
package.name = medicinetracker

# (str) Package domain (reverse DNS style)
package.domain = com.pushpesh

# ✅ (str) App version
version = 1.0.0

# (str) Source code where the main.py is located
source.dir = .

# (str) The main Python file
source.main = main.py

# (list) Application requirements
requirements = python3,kivy==2.3.1,Pillow,requests,python-dateutil

# (str) Icon of the app
icon.filename = icon.png

# (str) Supported orientation (portrait, landscape, all)
orientation = portrait

# (str) Supported Android API
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 27b
android.ndk_api = 21
android.arch = armeabi-v7a, arm64-v8a

# (bool) Copy libraries to APK
android.copy_libs = 1

# (str) Presplash
presplash.filename = presplash.png

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Additional permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# ✅ Updated bootstrap
p4a.bootstrap = sdl2

# (bool) Build in debug mode
log_level = 2