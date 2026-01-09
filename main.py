from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class MedicineTracker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.medicine_input = TextInput(
            hint_text="Medicine name",
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.medicine_input)

        dose_box = BoxLayout(size_hint_y=None, height=50)

        self.morning = CheckBox()
        self.afternoon = CheckBox()
        self.night = CheckBox()

        dose_box.add_widget(Label(text="Morning"))
        dose_box.add_widget(self.morning)
        dose_box.add_widget(Label(text="Afternoon"))
        dose_box.add_widget(self.afternoon)
        dose_box.add_widget(Label(text="Night"))
        dose_box.add_widget(self.night)

        self.add_widget(dose_box)

        add_btn = Button(text="Add Medicine", size_hint_y=None, height=50)
        add_btn.bind(on_press=self.add_medicine)
        self.add_widget(add_btn)

        self.scroll = ScrollView()
        self.list_layout = GridLayout(cols=1, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scroll.add_widget(self.list_layout)
        self.add_widget(self.scroll)

    def add_medicine(self, instance):
        name = self.medicine_input.text.strip()
        if not name:
            return

        dose = f"{int(self.morning.active)}-{int(self.afternoon.active)}-{int(self.night.active)}"

        label = Label(
            text=f"{name}  |  Dose: {dose}",
            size_hint_y=None,
            height=40
        )
        self.list_layout.add_widget(label)

        self.medicine_input.text = ""
        self.morning.active = False
        self.afternoon.active = False
        self.night.active = False

class MedicineApp(App):
    def build(self):
        return MedicineTracker()

if __name__ == "__main__":
    MedicineApp().run()