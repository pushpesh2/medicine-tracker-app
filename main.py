from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

# This string handles the entire Modern UI Layout (KV Language)
KV = '''
MDScreen:
    MDNavigationLayout:
        MDScreenManager:
            id: screen_manager
            
            # --- MEDICINE SECTION ---
            MDScreen:
                name: "meds"
                MDBoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: "Medicine Cabinet"
                        elevation: 4
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "20dp"
                        spacing: "15dp"
                        
                        MDTextField:
                            id: med_name
                            hint_text: "Medicine Name"
                            mode: "outline"
                        
                        MDBoxLayout:
                            adaptive_height: True
                            spacing: "10dp"
                            MDChips:
                                id: chip_morn
                                text: "Morning"
                                icon: "weather-sunny"
                                checkable: True
                            MDChips:
                                id: chip_noon
                                text: "Noon"
                                icon: "weather-sunset"
                                checkable: True
                            MDChips:
                                id: chip_night
                                text: "Night"
                                icon: "weather-night"
                                checkable: True

                        MDRaisedButton:
                            text: "ADD MEDICINE"
                            pos_hint: {"center_x": .5}
                            on_release: app.add_medicine()

                        ScrollView:
                            MDList:
                                id: med_list

            # --- WATER SECTION ---
            MDScreen:
                name: "water"
                MDBoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: "Hydration Tracker"
                        elevation: 4
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "20dp"
                        spacing: "30dp"
                        
                        MDCard:
                            orientation: "vertical"
                            padding: "20dp"
                            size_hint: None, None
                            size: "280dp", "180dp"
                            pos_hint: {"center_x": .5}
                            radius: [15,]
                            
                            MDLabel:
                                id: water_status
                                text: "0 ml"
                                font_style: "H3"
                                halign: "center"
                                theme_text_color: "Primary"
                            
                            MDRaisedButton:
                                text: "+ 250ml"
                                pos_hint: {"center_x": .5}
                                on_release: app.add_water()

                        MDBoxLayout:
                            adaptive_height: True
                            spacing: "20dp"
                            MDLabel:
                                text: "Hourly Reminders"
                            MDSwitch:
                                id: water_switch
                                on_active: app.toggle_water_alarm(*args)

        # --- SIDEBAR (NAV DRAWER) ---
        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            MDNavigationDrawerMenu:
                MDNavigationDrawerHeader:
                    title: "Health Buddy"
                    text: "Your daily assistant"
                    spacing: "4dp"
                    padding: "16dp", 0, 0, "16dp"
                
                MDNavigationDrawerItem:
                    icon: "pill"
                    text: "Medicines"
                    on_release: 
                        screen_manager.current = "meds"
                        nav_drawer.set_state("close")
                
                MDNavigationDrawerItem:
                    icon: "water"
                    text: "Water"
                    on_release: 
                        screen_manager.current = "water"
                        nav_drawer.set_state("close")
'''

class HealthBuddyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.store = JsonStore('health_data.json')
        return Builder.load_string(KV)

    def on_start(self):
        # Load existing data from database
        if self.store.exists('water'):
            self.root.ids.water_status.text = f"{self.store.get('water')['amount']} ml"
        self.load_meds()

    def add_medicine(self):
        name = self.root.ids.med_name.text
        if name:
            # Logic to save and update list
            self.root.ids.med_name.text = ""
            # (Simplified for briefness, add storage logic here)

    def add_water(self):
        current = self.store.get('water')['amount'] if self.store.exists('water') else 0
        new_total = current + 250
        self.store.put('water', amount=new_total)
        self.root.ids.water_status.text = f"{new_total} ml"

    def toggle_water_alarm(self, instance, value):
        # Logic to trigger background service
        pass

if __name__ == "__main__":
    HealthBuddyApp().run()
