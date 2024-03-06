import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.clock import Clock


class NoiseApp(App):

    def build(self):
        return NoiseTool()


class NoiseTool(BoxLayout):
    def __init__(self, **kwargs):
        super(NoiseTool, self).__init__(**kwargs)

        self.start_button = self.ids['start_button']
        self.stop_button = self.ids['stop_button']
        self.display_label = self.ids['display_label']
        self.switch = self.ids['duration_switch']
        self.user_input = self['user_input']
        self.duration = int(self.user_input.text)


        self.zero = 1
        self.mins = 0
        self.counter = ''


    def start_recording_clock(self):
        self.zero = 1 # reset zero when the function gets called

        Clock.schedule_interval(self.updateDisplay, 1)
        self.start_button.disable = True
        self.stop_button.disabled = False
        self.switch.disabled = True


    def stop_recording(self):

        Clock.unschedule(self.updateDisplay)
        self.display_label.text = 'Finished Recording!'
        self.start_button.disable = False
        self.stop_button.disable = True
        self.switch.disabled = True


    def updateDisplay(self,dt):
         ### Called every second
        if self.switch.active == False:
            if self.zero < 60 and len(str(self.zero) == 1):
                self.display_label.text = '0' + str(self.mins) + ':0' + str(self.zero)
                self.zero += 1

            elif self.zero < 60 and len(str(self.zero)) == 2:






if __name__ == '__main__':
    NoiseApp().run()


theApp = NoiseApp()

theApp.run()