[app]

# (str) Title of your application
title = Medicine Water Tracker

# (str) Package name
package.name = medtrack

# (str) Package domain (needed for android packaging)
package.domain = com.pushpesh

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's include everything)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# pyjnius is CRITICAL for alarms. sqlite3 is for the database.
requirements = python3,kivy==2.3.0,pyjnius,sqlite3,openssl,hostpython3

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.2

# (list) Permissions
# Necessary for Alarms, Notifications, and Vibrate
android.permissions = INTERNET, SCHEDULE_EXACT_ALARM, USE_EXACT_ALARM, POST_NOTIFICATIONS, WAKE_LOCK, RECEIVE_BOOT_COMPLETED, VIBRATE

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, armeabi-v7a is for 32-bit, arm64-v8a is for 64-bit
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup
android.allow_backup = True

# (list) Android service to run in background
# This is what will handle your alarms even when the app is closed
services = AlarmService:service.py

# (list) The intent filters to allow the app to restart alarms after phone reboot
android.add_intent_filters = [ {"name": "android.intent.action.BOOT_COMPLETED"} ]

# (bool) Accept SDK license without operator interaction
android.accept_sdk_license = True

# (bool) Do not update the SDK (we handle this in the workflow now)
android.skip_update = False

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1