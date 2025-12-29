import tkinter as tk
from abc import ABC, abstractmethod

class AbstractScreen(tk.Frame, ABC):
    """
    Tüm ekranların atasıdır (Base Class).
    Tkinter Frame'i ve ABC'yi miras alır.
    """
    def __init__(self, parent, manager, controller):
        super().__init__(parent)
        self.manager = manager
        self.controller = controller

        # Ortak Görsel Ayarlar
        self.config(bg="#F0F3F4") # Constants kullanmadan hardcode ettik veya import edebilirsin

        # Arayüzü oluştur
        self.create_widgets()

    @abstractmethod
    def create_widgets(self):
        """
        Her ekran kendi butonlarını ve etiketlerini burada tanımlamak ZORUNDADIR.
        """
        pass

    def on_show(self):
        """
        Ekran görüntülendiğinde çalışır.
        Veri yenilemek isteyen ekranlar bunu ezer (Override).
        """
        pass

    def navigate(self, screen_name):
        """Başka bir ekrana geçişi kolaylaştırır."""
        self.manager.show_screen(screen_name)