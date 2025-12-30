import tkinter as tk
from core.data_manager import CSVDataManager
from core.game_features import BasicScoreManager, MultipleChoiceGenerator
from core.game_controller import GameController
from ui.screen_manager import ScreenManager
from ui.screens.welcome_screen import WelcomeScreen
from ui.screens.menu_screen import MenuScreen
from ui.screens.language_select_screen import LanguageSelectScreen
from ui.screens.mode_select_screen import ModeSelectScreen
from ui.screens.game_screen import GameScreen
from ui.screens.match_screen import MatchScreen
from ui.screens.result_screen import ResultScreen
from ui.screens.add_word_screen import AddWordScreen

class WordGameApp:
    """
    Uygulamanın Başlatıcısı (Entry Point).
    Hiçbir mantık içermez, sadece kabloları bağlar.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kelime Oyunu")
        self.root.geometry("600x700")

        # 1. Çekirdek (Core) Kurulumu
        data_mgr = CSVDataManager()
        score_mgr = BasicScoreManager()
        # Varsayılan olarak çoktan seçmeli ile başlıyoruz ama controller bunu değiştirebilir
        generator = MultipleChoiceGenerator()

        self.controller = GameController(data_mgr, score_mgr)
        # Generator'ı controller'a set ediyoruz (Opsiyonel, oyun başlayınca da yapılabilir)
        self.controller.set_generator(generator)

        # 2. UI Kurulumu
        self.screen_manager = ScreenManager(self.root)

        # 3. Ekranları Kaydetme
        # Not: Diğer ekranları da ui/screens/ altına taşıyıp AbstractScreen'den türetmelisin.
        self.screen_manager.add_screen(WelcomeScreen, "WelcomeScreen", self.controller)
        self.screen_manager.add_screen(MenuScreen, "MenuScreen", self.controller)
        self.screen_manager.add_screen(LanguageSelectScreen, "LanguageSelectScreen", self.controller)
        self.screen_manager.add_screen(ModeSelectScreen, "ModeSelectScreen", self.controller)
        self.screen_manager.add_screen(GameScreen, "GameScreen", self.controller)
        self.screen_manager.add_screen(MatchScreen, "MatchScreen", self.controller)
        self.screen_manager.add_screen(ResultScreen, "ResultScreen", self.controller)
        self.screen_manager.add_screen(AddWordScreen, "AddWordScreen", self.controller)
        self.screen_manager.add_screen(MatchScreen, "MatchScreen", self.controller)
        # Uygulamayı başlat
        self.screen_manager.show_screen("WelcomeScreen")

    def run(self):
        self.root.mainloop()

