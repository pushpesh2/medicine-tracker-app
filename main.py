from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
import os

# This saves your data on the phone so it doesn't disappear
store = JsonStore('health_tracker.json')

class MedicineEntry(BoxLayout):
    """The UI for each medicine row in the list"""
    text = StringProperty('')

class TrackerHome(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        
        # Header
        self.add_widget(Label(text="Health Tracker", font_size='24sp', size_hint_y=None, height=50))

        # Input Area
        input_area = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=5)
        self.med_name = TextInput(hint_text="Medicine Name...", multiline=False)
        
        btn_layout = BoxLayout(spacing=10)
        add_med_btn = Button(text="Add Med", background_color=(0.2, 0.7, 0.3, 1))
        add_med_btn.bind(on_press=self.add_medicine)
        
        add_water_btn = Button(text="Log Water (250ml)", background_color=(0.2, 0.5, 0.9, 1))
        add_water_btn.bind(on_press=self.log_water)
        
        btn_layout.add_widget(add_med_btn)
        btn_layout.add_widget(add_water_btn)
        
        input_area.add_widget(self.med_name)
        input_area.add_widget(btn_layout)
        self.add_widget(input_area)

        # Labels for stats
        self.stats_label = Label(text="Water today: 0ml", size_hint_y=None, height=40)
        self.add_widget(self.stats_label)

        # List of Medicines
        self.add_widget(Label(text="Current Medications:", size_hint_y=None, height=30))
        self.med_list = RecycleView()
        self.med_list.viewclass = 'Label'  # Simplified for bulletproof build
        self.med_list_data = []
        self.load_data()
        self.add_widget(self.med_list)

    def load_data(self):
        """Load saved data from the phone storage"""
        if store.exists('water'):
            self.stats_label.text = f"Water today: {store.get('water')['amount']}ml"
        
        self.med_list_data = []
        if store.exists('medicines'):
            meds = store.get('medicines')['list']
            for m in meds:
                self.med_list_data.append({'text': m})
        self.med_list.data = self.med_list_data

    def add_medicine(self, instance):
        name = self.med_name.text.strip()
        if name:
            current_meds = []
            if store.exists('medicines'):
                current_meds = store.get('medicines')['list']
            
            current_meds.append(f"{name} (Added: {datetime.now().strftime('%H:%M')})")
            store.put('medicines', list=current_meds)
            self.med_name.text = ""
            self.load_data()

    def log_water(self, instance):
        amount = 0
        if store.exists('water'):
            amount = store.get('water')['amount']
        amount += 250
        store.put('water', amount=amount)
        self.load_data()

class MedicineApp(App):
    def build(self):
        return TrackerHome()

if __name__ == "__main__":
    MedicineApp().run()
