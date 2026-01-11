from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform

# Modern Palette
COLORS = {
    "bg": "#F0F2F5",
    "primary": "#007AFF", # iOS Blue
    "secondary": "#5856D6", # Deep Purple
    "danger": "#FF3B30", # Red
    "card": "#FFFFFF",
    "text": "#1C1C1E"
}

store = JsonStore('health_data.json')

class StyledCard(BoxLayout):
    def __init__(self, bg_color="#FFFFFF", rad=[15,], **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgb=get_color_from_hex(bg_color))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=rad)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MedicineTrackerApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex(COLORS["bg"])
        self.start_service() # Wake up the background alarm logic

        root = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # TITLE
        root.add_widget(Label(text="My Health Tracker", font_size='26sp', color=get_color_from_hex(COLORS["text"]), bold=True, size_hint_y=None, height=50))

        # MEDICINE CARD
        med_card = StyledCard(orientation='vertical', padding=15, spacing=10, size_hint_y=None, height=200)
        self.med_input = TextInput(hint_text="Medicine name...", multiline=False, size_hint_y=None, height=45, background_normal='', background_color=(0.9, 0.9, 0.9, 1))
        
        dose_box = BoxLayout(spacing=10, size_hint_y=None, height=45)
        self.dose_btns = {}
        for d in ["Morn", "Noon", "Night"]:
            btn = Button(text=d, background_normal='', background_color=(0.7, 0.7, 0.7, 1))
            btn.bind(on_press=self.toggle_btn)
            self.dose_btns[d] = btn
            dose_box.add_widget(btn)

        add_btn = Button(text="ADD MEDICINE", background_normal='', background_color=get_color_from_hex(COLORS["secondary"]), bold=True, size_hint_y=None, height=50)
        add_btn.bind(on_press=self.add_med)
        
        med_card.add_widget(self.med_input)
        med_card.add_widget(dose_box)
        med_card.add_widget(add_btn)
        root.add_widget(med_card)

        # WATER CARD
        water_card = StyledCard(padding=15, spacing=15, size_hint_y=None, height=100)
        self.water_lbl = Label(text="Water: 0ml", color=get_color_from_hex(COLORS["primary"]), bold=True, font_size='18sp')
        
        water_act_btn = Button(text="+250ml", background_normal='', background_color=get_color_from_hex(COLORS["primary"]), bold=True)
        water_act_btn.bind(on_press=self.add_water)
        
        self.alarm_btn = Button(text="Alarm Off", background_normal='', background_color=get_color_from_hex(COLORS["danger"]))
        self.alarm_btn.bind(on_press=self.toggle_alarm)
        
        water_card.add_widget(self.water_lbl)
        water_card.add_widget(water_act_btn)
        water_card.add_widget(self.alarm_btn)
        root.add_widget(water_card)

        # SCROLLABLE LIST
        self.scroll = ScrollView()
        self.list_ui = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.list_ui.bind(minimum_height=self.list_ui.setter('height'))
        self.scroll.add_widget(self.list_ui)
        root.add_widget(self.scroll)

        self.load_all()
        return root

    def start_service(self):
        if platform == 'android':
            from android import argb
            service = autoclass('com.pushpesh.medtrack.ServiceAlarmservice')
            service.start(App.get_running_app().get_package_domain(), '')

    def toggle_btn(self, btn):
        btn.background_color = get_color_from_hex(COLORS["secondary"]) if btn.background_color == [0.7, 0.7, 0.7, 1] else [0.7, 0.7, 0.7, 1]

    def add_med(self, _):
        name = self.med_input.text.strip()
        times = [t for t, b in self.dose_btns.items() if b.background_color != [0.7, 0.7, 0.7, 1]]
        if name and times:
            entry = f"{name} ({', '.join(times)})"
            meds = store.get('meds')['data'] if store.exists('meds') else []
            meds.append(entry)
            store.put('meds', data=meds)
            self.refresh_list()
            self.med_input.text = ""

    def add_water(self, _):
        val = store.get('water')['val'] if store.exists('water') else 0
        val += 250
        store.put('water', val=val)
        self.water_lbl.text = f"Water: {val}ml"

    def toggle_alarm(self, _):
        current = store.get('settings')['water_alarm'] if store.exists('settings') else False
        new_state = not current
        store.put('settings', water_alarm=new_state)
        self.alarm_btn.text = "Alarm On" if new_state else "Alarm Off"
        self.alarm_btn.background_color = (0, 0.8, 0.4, 1) if new_state else get_color_from_hex(COLORS["danger"])

    def load_all(self):
        if store.exists('water'): self.water_lbl.text = f"Water: {store.get('water')['val']}ml"
        if store.exists('settings'):
            state = store.get('settings')['water_alarm']
            self.alarm_btn.text = "Alarm On" if state else "Alarm Off"
            self.alarm_btn.background_color = (0, 0.8, 0.4, 1) if state else get_color_from_hex(COLORS["danger"])
        self.refresh_list()

    def refresh_list(self):
        self.list_ui.clear_widgets()
        if store.exists('meds'):
            for m in store.get('meds')['data']:
                card = StyledCard(bg_color="#FFFFFF", size_hint_y=None, height=50, padding=10)
                card.add_widget(Label(text=m, color=(0,0,0,1)))
                self.list_ui.add_widget(card)

if __name__ == "__main__":
    MedicineTrackerApp().run()
