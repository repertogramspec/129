[app]
title = MyProxyVPN
package.name = myproxyapp
package.domain = org.testproxy
source.dir = .
source.include_exts = py

# Версия приложения
version = 1.0

# Самый стабильный набор библиотек
# Если в коде используешь requests, оставляем его здесь
requirements = python3,kivy==2.2.1,requests,urllib3,certifi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Собираем только под современную архитектуру (64-бит)
# Это ускорит сборку в 2 раза и уменьшит шанс ошибки
android.archs = arm64-v8a

# Настройки SDK/NDK (оптимальные для GitHub Actions)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# Иконка (пока стандартная, чтобы не было ошибок путей)
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
