[app]
title = MyApp
package.name = myapp
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.api = 33
android.minapi = 21
android.sdk = 33

android.build_tools_version = 33.0.2
android.ndk = 25b
android.ndk_api = 21

android.accept_sdk_license = True
android.skip_update = True

android.permissions = INTERNET

android.archs = arm64-v8a,armeabi-v7a

# Fix build cache issues
p4a.local_recipes = 
p4a.bootstrap = sdl2
