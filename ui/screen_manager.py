import tkinter as tk

class ScreenManager:
    """
    Uygulamadaki tüm ekranların kaydını tutar ve geçişleri yönetir.
    """
    def __init__(self, root_window):
        self.root = root_window
        # Tüm ekranların üst üste bineceği ana konteyner
        self.container = tk.Frame(self.root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

    def add_screen(self, screen_class, screen_name, game_controller):
        """
        Yeni bir ekranı oluşturur ve sisteme kaydeder.
        Dependency Injection burada yapılır (Controller ekrana verilir).
        """
        frame = screen_class(parent=self.container, manager=self, controller=game_controller)
        self.frames[screen_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_screen(self, screen_name):
        """İstenilen ekranı en öne getirir."""
        if screen_name in self.frames:
            frame = self.frames[screen_name]
            frame.on_show() # Ekranın açılış hazırlığını yap (Hook)
            frame.tkraise()
        else:
            print(f"Hata: '{screen_name}' adında bir ekran bulunamadı.")