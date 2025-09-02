import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
from kivy.config import Config

# --- Fuente global: SimSunExtG desde la carpeta del proyecto ---
LabelBase.register(name="ChineseFont", fn_regular="SimsunExtG.ttf")
Config.set("kivy", "default_font", ["ChineseFont"])

# --- Fondo blanco ---
class FondoBlanco(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # blanco
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

# --- Configuración log ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

class BuscadorApp(App):
    def build(self):
        self.layout = FondoBlanco(orientation="vertical", padding=10, spacing=10)

        # Campo de código
        self.codigo_input = TextInput(
            hint_text="📷 Código de barras",
            size_hint_y=None, height=60,
            font_size=24, foreground_color=(0,0,0,1)
        )
        self.layout.add_widget(self.codigo_input)

        buscar_btn = Button(text="🔎 Buscar", size_hint_y=None, height=60, font_size=22)
        buscar_btn.bind(on_press=self.buscar)
        self.layout.add_widget(buscar_btn)

        # Campos editables
        self.layout.add_widget(Label(text="Producto:", font_size=20, color=(0,0,0,1)))
        self.prod_input = TextInput(font_size=22, foreground_color=(0,0,0,1))
        self.layout.add_widget(self.prod_input)

        self.layout.add_widget(Label(text="Precio:", font_size=20, color=(0,0,0,1)))
        self.precio_input = TextInput(font_size=22, foreground_color=(0,0,0,1))
        self.layout.add_widget(self.precio_input)

        self.layout.add_widget(Label(text="Stock:", font_size=20, color=(0,0,0,1)))
        self.stock_input = TextInput(font_size=22, foreground_color=(0,0,0,1))
        self.layout.add_widget(self.stock_input)

        guardar_btn = Button(text="💾 Guardar cambios", size_hint_y=None, height=60, font_size=22)
        guardar_btn.bind(on_press=self.guardar)
        self.layout.add_widget(guardar_btn)

        # --- Conexión Google Sheets ---
        try:
            scope = ["https://spreadsheets.google.com/feeds",
                     "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            client = gspread.authorize(creds)
            self.sheet = client.open_by_key("1br-QHcxrCvI0-ORlZBU8bSXc80C5JQZHDqYyRmFGYuk").worksheet("PRUEBA")
        except Exception as e:
            logging.error(f"Error al conectar con Google Sheets: {e}")
            self.sheet = None

        return self.layout

    def buscar(self, instance):
        codigo = self.codigo_input.text.strip()
        if not codigo or not self.sheet:
            return

        inicio = time.time()

        # Escribir el código en A2
        self.sheet.update_acell("A2", codigo)

        # Leer datos calculados
        producto = self.sheet.acell("B2").value
        precio = self.sheet.acell("C2").value
        stock = self.sheet.acell("D2").value

        duracion = time.time() - inicio

        # Mostrar en los campos editables
        self.prod_input.text = producto if producto else ""
        self.precio_input.text = precio if precio else ""
        self.stock_input.text = stock if stock else ""

        logging.info(f"Resultado recibido en {duracion:.2f} s -> {producto}, {precio}, {stock}")

    def guardar(self, instance):
        if not self.sheet:
            return

        # Datos editados en la app
        prod = self.prod_input.text.strip()
        precio = self.precio_input.text.strip()
        stock = self.stock_input.text.strip()

        # Guardar en columnas H, I, J de la fila 2
        self.sheet.update_acell("H2", prod)
        self.sheet.update_acell("I2", precio)
        self.sheet.update_acell("J2", stock)

        logging.info(f"✅ Cambios guardados -> H2:{prod}, I2:{precio}, J2:{stock}")

if __name__ == "__main__":
    logging.info("Iniciando aplicación BuscadorApp...")
    BuscadorApp().run()
    logging.info("Aplicación cerrada.")
