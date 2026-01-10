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
android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET
android.copy_libs = 1
p4a.bootstrap = sdl2

log_level = 2