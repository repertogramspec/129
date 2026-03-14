[app]

# (str) Название твоего приложения
title = MyProxyVPN

# (str) Имя пакета (без пробелов)
package.name = myproxyapp

# (str) Домен пакета
package.domain = org.testproxy

# (str) Папка с исходным кодом (точка означает текущую папку)
source.dir = .

# (list) Расширения файлов, которые нужно включить в сборку
source.include_exts = py,png,jpg,kv,atlas

# (str) Версия приложения
version = 1.0

# (list) Зависимости (самое важное для SOCKS5)
requirements = python3,kivy

# (str) Ориентация экрана
orientation = portrait

# (bool) Использовать ли полноэкранный режим
fullscreen = 0

# (list) Архитектуры (arm64-v8a нужна для современных телефонов)
android.archs = armeabi-v7a, arm64-v8a

# (int) Минимальное API Android (21 — это Android 5.0)
android.minapi = 21

# (int) Целевое API Android (33 — требование Google Play 2023/24)
android.api = 33

# (bool) Разрешить установку на SD-карту
android.allow_backup = True

# (str) Формат иконки (если будет своя, укажи путь)
# icon.filename = %(source.dir)s/icon.png

# --- Настройки Python for Android ---
p4a.branch = master

[buildozer]
# (int) Уровень логов (2 — самый подробный)
log_level = 2

# (int) Удалять ли временные файлы сборки
warn_on_root = 1
