from kivy.app import App
import pyaudio
import pygame
import numpy as np
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Line, Color


pygame.mixer.init()
alarm_sound = pygame.mixer.Sound('alarm_sound.wav')


class AudioRecorderApp(App):

    def build(self):
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.sensitivity = 50

        self.root = BoxLayout(orientation='vertical')
        
        # Record button
        self.record_btn = Button(text='Record')
        self.record_btn.bind(on_press=self.start_recording)
        
        # Stop button
        self.stop_btn = Button(text='Stop', state='down')
        self.stop_btn.bind(on_press=self.stop_recording)

        # Sensitivity slider
        self.slider = Slider(min=1, max=100, value=50)
        self.slider.bind(value=self.on_slider_value) 
        self.slider_label = Label(text=f'Sensitivity: {self.slider.value} dB')

        # Stop Alarm button
        self.stop_alarm_btn = Button(text='Stop Alarm')
        self.stop_alarm_btn.bind(on_press=self.stop_alarm_sound)

        # Status display label
        self.status_label = Label(text= 'Hasn\'t started recording yet.')

        self.empty = Label()
        with self.root.canvas:
            self.waveform_color = Color(1, 0, 0, 1)  # Red color
            self.waveform_line = Line(points=[])
        
        self.root.add_widget(self.record_btn)
        self.root.add_widget(self.stop_btn)
        self.root.add_widget(self.slider)
        self.root.add_widget(self.slider_label)
        self.root.add_widget(self.stop_alarm_btn)
        self.root.add_widget(self.status_label)
        self.root.add_widget(self.empty)

        
        return self.root

    
    def update_waveform(self, audio_data):
        # Clear the previous waveform
        self.waveform_line.points = []

        for i, sample in enumerate(audio_data):
            x = i  # X coordinate: Sample index
            y = (sample / 32768.0) * 100 + 100  # Y coordinate: Sample amplitude
            self.waveform_line.points += [x, y]

    def start_recording(self, instance):
        self.is_recording = True
        self.record_btn.disabled = True
        self.stop_btn.disabled = False
        self.status_label.text = 'Recording...'

        # Audio stream parameters
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024,
                                      stream_callback=self.callback)
        
        print("Recording started...")

    def stop_recording(self, instance):
        self.is_recording = False
        self.record_btn.disabled = False
        self.stop_btn.disabled = True
        self.stream.stop_stream()
        self.stream.close()
        self.status_label.text = 'Recording stopped.'


        print("Recording stopped.")

    def on_slider_value(self, instance, value):
        self.slider_label.text = f'Sensitivity: {int(self.slider.value)} dB'
        self.sensitivity = int(value)
    
    def stop_alarm_sound(self, instance):
        alarm_sound.stop()  # Stop the alarm sound
        print("Alarm stopped.")

    def loud_noise_detected(self, *args):
        # This method will be called on the main thread
        alarm_sound.play()
        self.stop_btn.dispatch('on_press')
        self.status_label.text = f'LOUD NOISE DETECTED: {args[0]:.2f} dB PLAYING THE ALARM!'


    def callback(self, in_data, frame_count, time_info, status):
        if self.is_recording:
            # Convert string data to numpy array# Convert audio data to a larger data type to avoid overflow
            audio_data = np.frombuffer(in_data, dtype=np.int16).astype(np.float32)
            Clock.schedule_once(lambda dt: self.update_waveform(audio_data), 0)


            # Ensure no NaN or Inf values
            if not np.any(np.isnan(audio_data)) and not np.any(np.isinf(audio_data)):
                # Proceed with RMS calculation
                rms = np.sqrt(np.mean(np.square(audio_data)))
            else:
                # Handle invalid data case
                rms = 0  # or appropriate handling

            # Convert RMS to decibels
            db = 20 * np.log10(rms) if rms > 0 else 0

            if db > self.sensitivity:
                print(f"Loud noise detected! Volume: {db:.2f} dB")
                # Schedule the UI update and stop recording to be called on the main thread
                Clock.schedule_once(lambda dt: self.loud_noise_detected(db), 0)

            
            return (in_data, pyaudio.paContinue)
        else:
            return (in_data, pyaudio.paComplete)
