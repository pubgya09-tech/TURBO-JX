[app]
title = Turbo JX
package.name = turbojx
package.domain = org.turbojx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,txt
version = 1.0

# DİQQAT: Agar o'yiningizda pygame ishlatgan bo'lsangiz, pastdagi qatorga ,pygame qo'shing
requirements = python3,kivy

orientation = landscape
fullscreen = 1

android.accept_sdk_license = True
android.api = 30
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a

log_level = 2
