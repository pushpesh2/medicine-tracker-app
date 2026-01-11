from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore

# Modern Color Palette
COLORS = {
    "bg": "#F8F9FA",
    "primary": "#00C2FF",  # Bright Water Blue
    "secondary": "#7D5FFF", # Medicine Purple
    "card": "#FFFFFF",
    "text": "#2D3436",
    "accent": "#FF7675"    # Alarm Red
}

store = JsonStore('health_data.json')

class StyledCard(BoxLayout):
    def __init__(self, bg_color="#FFFFFF", **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgb=get_color_from_hex(bg_color))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15,])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MedicineTrackerApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex(COLORS["bg"])
        
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # --- HEADER ---
        header = Label(
            text="Health Buddy",
            font_size='28sp',
            color=get_color_from_hex(COLORS["text"]),
            bold=True,
            size_hint_y=None,
            height=60
        )
        root.add_widget(header)

        # --- SECTION: MEDICINE ---
        root.add_widget(Label(text="Medicines", color=get_color_from_hex(COLORS["text"]), size_hint_y=None, height=30, halign='left'))
        
        med_input_card = StyledCard(orientation='vertical', padding=15, spacing=10, size_hint_y=None, height=180)
        self.med_input = TextInput(hint_text="Pill Name...", multiline=False, size_hint_y=None, height=45)
        
        dose_layout = BoxLayout(spacing=5, size_hint_y=None, height=40)
        self.doses = {"Morning": Button(text="Morn", background_normal='', background_color=(.5,.5,.5,1)),
                      "Afternoon": Button(text="Aft", background_normal='', background_color=(.5,.5,.5,1)),
                      "Night": Button(text="Night", background_normal='', background_color=(.5,.5,.5,1))}
        
        for name, btn in self.doses.items():
            btn.bind(on_press=self.toggle_dose)
            dose_layout.add_widget(btn)
            
        add_med_btn = Button(text="Add to Cabinet", background_normal='', background_color=get_color_from_hex(COLORS["secondary"]), bold=True)
        add_med_btn.bind(on_press=self.add_medicine)
        
        med_input_card.add_widget(self.med_input)
        med_input_card.add_widget(dose_layout)
        med_input_card.add_widget(add_med_btn)
        root.add_widget(med_input_card)

        # --- SECTION: WATER ---
        root.add_widget(Label(text="Hydration", color=get_color_from_hex(COLORS["text"]), size_hint_y=None, height=30))
        
        water_card = StyledCard(padding=15, spacing=15, size_hint_y=None, height=100)
        self.water_label = Label(text="0 ml", color=get_color_from_hex(COLORS["primary"]), font_size='20sp', bold=True)
        
        water_btn = Button(text="+ 250ml", background_normal='', background_color=get_color_from_hex(COLORS["primary"]), bold=True)
        water_btn.bind(on_press=self.add_water)
        
        # Water Alarm Toggle
        self.water_alarm = Button(text="Alarm: OFF", background_color=get_color_from_hex(COLORS["accent"]))
        self.water_alarm.bind(on_press=self.toggle_water_alarm)
        
        water_card.add_widget(self.water_label)
        water_card.add_widget(water_btn)
        water_card.add_widget(self.water_alarm)
        root.add_widget(water_card)

        # --- LIST AREA ---
        self.scroll = ScrollView()
        self.med_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.med_list.bind(minimum_height=self.med_list.setter('height'))
        self.scroll.add_widget(self.med_list)
        root.add_widget(self.scroll)
        
        self.load_data()
        return root

    def toggle_dose(self, btn):
        if btn.background_color == [.5,.5,.5,1]:
            btn.background_color = get_color_from_hex(COLORS["secondary"])
        else:
            btn.background_color = [.5,.5,.5,1]

    def add_medicine(self, instance):
        name = self.med_input.text.strip()
        active_doses = [d for d, btn in self.doses.items() if btn.background_color != [.5,.5,.5,1]]
        
        if name and active_doses:
            med_entry = f"{name} ({', '.join(active_doses)})"
            self.save_med(med_entry)
            self.update_list_ui(med_entry)
            self.med_input.text = ""

    def add_water(self, instance):
        current = store.get('water')['amount'] if store.exists('water') else 0
        new_amount = current + 250
        store.put('water', amount=new_amount)
        self.water_label.text = f"{new_amount} ml"

    def toggle_water_alarm(self, btn):
        if "OFF" in btn.text:
            btn.text = "Alarm: ON"
            btn.background_color = (0, 1, 0.5, 1) # Success Green
        else:
            btn.text = "Alarm: OFF"
            btn.background_color = get_color_from_hex(COLORS["accent"])

    def save_med(self, entry):
        meds = store.get('meds')['list'] if store.exists('meds') else []
        meds.append(entry)
        store.put('meds', list=meds)

    def load_data(self):
        if store.exists('water'):
            self.water_label.text = f"{store.get('water')['amount']} ml"
        if store.exists('meds'):
            for med in store.get('meds')['list']:
                self.update_list_ui(med)

    def update_list_ui(self, text):
        item = Label(text=text, color=get_color_from_hex(COLORS["text"]), size_hint_y=None, height=40)
        self.med_list.add_widget(item)

if __name__ == "__main__":
    MedicineTrackerApp().run()