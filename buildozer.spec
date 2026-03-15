[app]
title = MyProxyVPN
package.name = myproxyapp
package.domain = org.testproxy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Самый стабильный набор для сетевых приложений
requirements = python3,kivy==2.2.1,openssl

orientation = portrait
fullscreen = 0

# Разрешения (добавили на всякий случай состояние сети)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Архитектуры (оставляем обе основные)
android.archs = armeabi-v7a, arm64-v8a

# API уровни
android.api = 33
android.minapi = 21

# Флаг для исправления ошибок компиляции на новых системах
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
