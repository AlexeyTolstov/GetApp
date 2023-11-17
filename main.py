from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window 
from kivy.graphics import Color, RoundedRectangle, Rectangle

from funcs import decrypts, switch_new_line
import requests

url = "http://192.168.4.1/get?telephone=+79293451239&class=7&city=Biysk&gender=m&sections0=s0&sections1=s1&rests0=r0&favorite_subjects0=fs0&result=user_result"

Window.size = (360, 640)


def get_data():
    response = requests.get(url)
    try:
        if response.status_code == 200:
            json_data = response.json()
            print(json_data)
            return json_data
    except:
        return "Data is not generated"


class RoundedButton(Button):
    def __init__(self, color_, radius_=20, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.color_ = color_
        self.radius_ = radius_

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.color_)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius_,])


class GetDataApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        
        self.isRun = False
        self.isLoadData = False
        Clock.schedule_interval(self.update, 5)
        
        with self.layout.canvas.before:
            Color(.38, .33, .86)
            self.layout.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.label = Label(text="",
                                 pos_hint={'center_x': 0.5,
                                           'center_y': 0.6},
                                 size_hint=(0.1, 0.05),
                                 bold=True)

        self.button = RoundedButton(color_=(.95, .94, .99),
                                    text="Запустить",
                                    pos_hint={'center_x': 0.5,
                                              'center_y': 0.1},
                                    size_hint=(0.75, 0.1),
                                    color=(.55, .51, 1),
                                    background_normal="",
                                    bold=True)

        self.button.bind(on_release=self.click)
        
        self.label.scale = .5
        self.button.scale = 0.08

        self.button.bind(size=self.update_font_size)
        self.label.bind(size=self.update_font_size)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

    def click(self, instance):
        if not self.label.text:
            self.isRun = True
            self.label.text = "Loading ..."
            self.isLoadData = False
        else:
            self.label.text = ""
            self.button.text = "Запустить"
            self.isLoadData = False
            self.isRun = False

    def update_rect(self, instance, value):
        self.layout.rect.size = instance.size
        self.layout.rect.pos = instance.pos

    @staticmethod
    def update_font_size(instance, _):
        new_font_size = instance.width * instance.scale
        instance.font_size = new_font_size
    
    def update(self, *args):
        if self.isRun and not self.isLoadData:
            res = get_data()
            if isinstance(res, str):
                self.label.text = res
            else:
                label_str = ""
                for k, v in res.items():
                    label_str += str(k)+": "

                    if isinstance(v, list):
                        for ik, i in enumerate(v):
                            if not i:
                                break
                            
                            if ik == 0:
                                label_str += decrypts(str(i))
                            else:
                                label_str += ", " + decrypts(str(i))
                                if ik % 5 == 0 and ik != 0:
                                    label_str += "\n"
                    else:
                        label_str += decrypts(str(v))
                    label_str = switch_new_line(label_str, 30)
                    label_str += "\n"
                
                self.isLoadData = True
                self.isRun = False
                self.label.text = label_str
                
                self.button.text = "Очистить"

        else:
            self.button.text = "Запустить"
    
    def build(self):
        return self.layout
        

if __name__ == "__main__":
    GetDataApp().run()