import socket
import threading
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

# --- НАСТРОЙКИ ---
HOST = '127.0.0.1'
PORT = 1080
USER = "admin"
PASS = "supersecret"

class ProxyApp(App):
    def build(self):
        self.is_running = False
        
        # Основной контейнер
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Заголовок статуса
        self.status = Label(
            text="VPN СТАТУС: ВЫКЛЮЧЕН", 
            font_size='22sp', 
            color=(1, 0.3, 0.3, 1),
            size_hint_y=0.2
        )
        layout.add_widget(self.status)
        
        # Кнопка управления
        self.btn = Button(
            text="ЗАПУСТИТЬ СЕРВЕР",
            size_hint_y=0.2,
            background_color=(0.1, 0.7, 0.2, 1)
        )
        self.btn.bind(on_press=self.toggle_proxy)
        layout.add_widget(self.btn)
        
        # Окно логов
        self.scroll = ScrollView(size_hint_y=0.6)
        self.logs = Label(
            text="[СИСТЕМА] Ожидание запуска...\n",
            size_hint_y=None,
            halign='left',
            valign='top',
            font_size='14sp'
        )
        self.logs.bind(texture_size=self.logs.setter('size'))
        self.scroll.add_widget(self.logs)
        layout.add_widget(self.scroll)
        
        return layout

    def log_msg(self, msg):
        # Безопасное обновление текста из других потоков
        Clock.schedule_once(lambda dt: setattr(self.logs, 'text', self.logs.text + f"{msg}\n"))

    def toggle_proxy(self, instance):
        if not self.is_running:
            self.is_running = True
            self.btn.text = "ВЫЙТИ ИЗ ПРИЛОЖЕНИЯ"
            self.btn.background_color = (0.8, 0.2, 0.2, 1)
            self.status.text = "VPN СТАТУС: АКТИВЕН"
            self.status.color = (0.3, 1, 0.3, 1)
            threading.Thread(target=self.start_server, daemon=True).start()
            self.log_msg("[ИНФО] SOCKS5 запущен на 127.0.0.1:1080")
        else:
            # Полный выход из процесса, чтобы убить все потоки
            os._exit(0)

    def start_server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen(50)
            while self.is_running:
                client, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
        except Exception as e:
            self.log_msg(f"[!] Ошибка сервера: {e}")

    def handle_client(self, c):
        try:
            c.settimeout(20)
            
            # 1. Приветствие SOCKS5
            header = c.recv(2)
            if not header: return
            nmethods = c.recv(1)[0]
            c.recv(nmethods)
            c.sendall(b"\x05\x02") # Требуем логин/пароль

            # 2. Авторизация
            auth_header = c.recv(2)
            if not auth_header: return
            u_len = c.recv(1)[0]
            user = c.recv(u_len).decode()
            p_len = c.recv(1)[0]
            pwd = c.recv(p_len).decode()

            if user == USER and pwd == PASS:
                c.sendall(b"\x01\x00") # Успех
            else:
                c.sendall(b"\x01\x01") # Отказ
                c.close()
                return

            # 3. Запрос соединения
            req = c.recv(4)
            if not req: return
            atyp = req[3]
            
            if atyp == 1: # IPv4
                addr = socket.inet_ntoa(c.recv(4))
            elif atyp == 3: # Domain
                d_len = c.recv(1)[0]
                addr = c.recv(d_len).decode()
            else:
                return

            port = int.from_bytes(c.recv(2), 'big')
            self.log_msg(f"-> Коннект к: {addr}:{port}")

            # 4. Проброс данных
            remote = socket.create_connection((addr, port), timeout=20)
            c.sendall(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
            
            def pipe(src, dst):
                try:
                    while True:
                        data = src.recv(16384)
                        if not data: break
                        dst.sendall(data)
                except: pass
                finally:
                    try: src.close()
                    except: pass
                    try: dst.close()
                    except: pass

            threading.Thread(target=pipe, args=(c, remote), daemon=True).start()
            pipe(remote, c)

        except Exception:
            try: c.close()
            except: pass

if __name__ == "__main__":
    ProxyApp().run()
          
