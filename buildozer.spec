[app]
title = Medicine Tracker
package.name = medicinetracker
package.domain = com.pushpesh
version = 1.0.0

source.dir = .
source.main = main.py

requirements = python3,kivy==2.3.1,Pillow,requests,python-dateutil

orientation = portrait
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.arch = armeabi-v7a, arm64-v8a

p4a.bootstrap = sdl2
android.copy_libs = 1

# 🔥 CRITICAL FIX
android.skip_update = libffi

log_level = 2