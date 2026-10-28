[app]
title = Turbo JX
package.name = turbojx
package.domain = org.turbojx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,txt
version = 1.0

# Kivy versiyasi qat'iy belgilanmadi (tizim o'zi mosini topadi)
requirements = python3,kivy,libffi

orientation = landscape
fullscreen = 1

# Android sozlamalari
android.accept_sdk_license = True
android.api = 30
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a

# Qurish paytida xatoni aniqroq ko'rish uchun
log_level = 2
p4a.branch = develop
