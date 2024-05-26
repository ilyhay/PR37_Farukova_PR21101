from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.slider import Slider


class MyPaintWidget(Widget):
    line_color = (1, 0, 0, 1)  # Начальный цвет линии
    line_width = 2  # Начальная толщина линии
    lines = []  # Список для хранения всех нарисованных линий
    current_line = None  # Переменная для хранения текущей линии

    def on_touch_down(self, touch):
        if not self.is_point_inside_color_picker(touch) and self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.line_color)
                self.current_line = Line(points=(touch.x, touch.y), width=self.line_width)
                self.lines.append(self.current_line)

    def on_touch_move(self, touch):
        if not self.is_point_inside_color_picker(touch) and self.collide_point(*touch.pos) and self.current_line:
            self.current_line.points += [touch.x, touch.y]

    def is_point_inside_color_picker(self, touch):
        color_picker = self.parent.children[2]  # Индекс 2 - ColorPicker
        return color_picker.collide_point(*touch.pos)

    def update_line_width(self, width):
        self.line_width = width
        self.current_line = None  # Сбрасываем текущую линию при изменении толщины


class MyPaintApp(App):

    def build(self):
        parent = BoxLayout(orientation='vertical')
        self.painter = MyPaintWidget()

        # Кнопка для очистки холста
        clear_btn = Button(text='Clear', size_hint=(1, 0.1))
        clear_btn.bind(on_release=self.clear_canvas)

        # Виджет выбора цвета
        color_picker = ColorPicker()
        color_picker.bind(color=self.set_color)

        # Виджет выбора толщины линии
        thickness_slider = Slider(min=1, max=10, value=2, orientation='horizontal', size_hint=(1, 0.1))
        thickness_slider.bind(value=self.set_thickness)

        parent.add_widget(self.painter)
        parent.add_widget(clear_btn)
        parent.add_widget(color_picker)
        parent.add_widget(thickness_slider)

        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        self.painter.lines = []  # Очищаем список нарисованных линий

    def set_color(self, instance, value):
        self.painter.line_color = value

    def set_thickness(self, instance, value):
        if self.painter.current_line:
            self.painter.update_line_width(value)
        self.painter.line_width = value


if __name__ == '__main__':
    MyPaintApp().run()