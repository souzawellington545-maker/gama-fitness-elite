[app]
title = Gama Fitness Elite
package.name = gamafitnesselite
package.domain = org.gama
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.accept_sdk_license = True
android.api = 31
android.min_api = 21
