"""
    Knob
    ====

    The :class:`Knob` widget creates a component that looks like a
    control Knob or Dial (from Wikipedia : "A control knob is a rotary
    control used to provide input to a device when grasped by an
    operator and turned, so that the degree of rotation corresponds to
    the desired input." http://en.wikipedia.org/wiki/Control_knob).
    To configure a knob a max/min and step values should be provided
    (like in Slider). Additionally, knobimg_source could be set to load
    a texture that visually represents the knob.

    To create a basic knob (in a kv file):

    Knob:
        size: 100, 100
        min: 0
        max: 100
        step: 1
        value: 0  # Default position of knob.
        knobimg_source: "img/knob_metal.png"  # Knob texture
        show_label: True  # Show central label
        show_marker: False  # Do not show surrounding marker

    To create a knob with a surrounding marker:

    Knob:
        size: 100, 100
        min: 0
        max: 100
        step: 1
        value: 0  # Default position of knob.
        knobimg_source: "img/knob_metal.png"  # Knob texture
        show_label: True  # Show central label
        show_marker: True  # Show surrounding marker
        marker_img: "img/bline.png" # Marker texture image
        knob_size: 0.9  # Scales knob size to leave space for marker
        markeroff_color: 0, 0, 0, 0

"""
__all__ = ('Knob', )
__version__ = '0.1'

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, StringProperty,\
    BooleanProperty, ReferenceListProperty, BoundedNumericProperty,\
    ListProperty
import math

Builder.load_string('''
<Knob>
    label: _label
    size_hint: None, None
    canvas.before:

        Color:
            rgba: self.markeroff_color
        Ellipse:
            pos: self.pos
            size: self.size[0], self.size[1]
            angle_start: 0
            angle_end: 360
            source: self.markeroff_img
        Color:
            rgba: self.marker_color
        Ellipse:
            pos: self.pos
            size: self.size[0], self.size[1]
            angle_start: self.marker_startangle
            angle_end: self._angle + self.marker_ahead\
                       if self._angle > self.marker_startangle else\
                       self.marker_startangle
            source: self.marker_img
        Color:
            rgba: self.knobimg_bgcolor
        Ellipse:
            pos: self.pos[0] + (self.size[0] * (1 - self.knobimg_size))/2,\
                 self.pos[1] + (self.size[1] * (1 - self.knobimg_size)) / 2

            size: self.size[0] * (self.knobimg_size), self.size[1] *\
                  (self.knobimg_size)
        Color:
            rgba: self.knobimg_color
        PushMatrix
        Rotate:
            angle: 360 - self._angle
            origin: self.center
        Rectangle:
            pos: self.pos[0] + (self.size[0] * (1 - self.knobimg_size)) /2,\
                 self.pos[1] + (self.size[1] * (1 - self.knobimg_size)) / 2
            size: self.size[0] * (self.knobimg_size), self.size[1] *\
                  (self.knobimg_size)
            source: self.knobimg_source
    canvas:
        PopMatrix
    Label:
        id: _label
        text: "%.f"%(root.value)
        center: root.center
        font_size: root.font_size
        color: root.font_color
        ''')


class Knob(Widget):
    """Class for creating a Knob widget."""

    min = NumericProperty(0)
    '''Minimum value for value :attr:`value`.
    :attr:`min` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.
    '''

    max = NumericProperty(100)
    '''Maximum value for value :attr:`value`.
    :attr:`max` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 100.
    '''

    range = ReferenceListProperty(min, max)
    ''' Range of the values for Knob.
    :attr:`range` is a :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`min`, :attr:`max`).
    '''

    value = NumericProperty(0)
    '''Current value of the knob. Set :attr:`value` when creating a knob to
    set its initial position. An internal :attr:`_angle` is calculated to set
    the position of the knob.
    :attr:`value` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.
    '''

    step = BoundedNumericProperty(1, min=0)
    '''Step interval of knob to go from min to max. An internal
    :attr:`_angle_step` is calculated to set knob step in degrees.
    :attr:`step` is a :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to 1 (min=0).
    '''

    knobimg_source = StringProperty("")
    '''Path of texture image that visually represents the knob. Use PNG for
    transparency support. The texture is rendered on a centered rectangle of
    size = :attr:`size` * :attr:`knobimg_size`.
    :attr:`knobimg_source` is a :class:`~kivy.properties.StringProperty`
    and defaults to empty string.
    '''

    knobimg_color = ListProperty([1, 1, 1, 1])
    '''Color to apply to :attr:`knobimg_source` texture when loaded.
    :attr:`knobimg_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1,1,1,1].
    '''

    show_label = BooleanProperty(True)
    ''' Shows/hides center label that show current value of knob.
    :attr:`show_label` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    '''

    font_size = StringProperty('10sp')
    ''' Font size of label.
    :attr:`font_size` is a :class:`~kivy.properties.StringProperty`
    and defaults to "10sp".
    '''

    font_color = ListProperty([1, 1, 1, 1])
    ''' Font color of label.
    :attr:`font_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1,1,1,1].
    '''

    knobimg_size = BoundedNumericProperty(0.9, max=1.0, min=0.1)
    ''' Internal proportional size of rectangle that holds
    :attr:`knobimg_source` texture.
    :attr:`knobimg_size` is a :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to 0.9.
    '''

    show_marker = BooleanProperty(True)
    ''' Shows/hides marker surrounding knob. use :attr:`knob_size` < 1.0 to
    leave space to marker.
    :attr:`show_marker` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    '''

    marker_img = StringProperty("")
    '''Path of texture image that visually represents the knob marker. The
    marker is rendered in a centered Ellipse (Circle) with the same size of
    the widget and goes from angle_start=:attr:`marker_startangle` to
    angle_end=:attr:`_angle`.
    :attr:`marker_img` is a :class:`~kivy.properties.StringProperty` and
    defaults to "".
    '''

    marker_color = ListProperty([1, 1, 1, 1])
    '''Color to apply to :attr:`marker_img` texture when loaded.
    :attr:`marker_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1,1,1,1].
    '''

    knobimg_bgcolor = ListProperty([0, 0, 0, 1])
    ''' Background color behind :attr:`knobimg_source` texture.
    :attr:`value` is a :class:`~kivy.properties.ListProperty` and defaults
    to [0,0,0,1].
    '''

    markeroff_img = StringProperty("")
    '''Path of texture image that visually represents the knob marker where
    it's off, that is, parts of the marker that haven't been reached yet by
    the knob (:attr:`value`).
    :attr:`markeroff_img` is a :class:`~kivy.properties.StringProperty`
    and defaults to "".
    '''

    markeroff_color = ListProperty([0, 0, 0, 0])
    '''Color applied to :attr:`markeroff_img` int the Canvas.
    :attr:`markeroff_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [0,0,0,0].
    '''

    marker_startangle = NumericProperty(0)
    '''Starting angle of Ellipse where :attr:`marker_img` is rendered.
    :attr:`value` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.
    '''

    marker_ahead = NumericProperty(0)
    ''' Adds degrees to angle_end of marker (except when :attr:`value` == 0).
    :attr:`marker_ahead` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 0.
    '''

    _angle = NumericProperty(0)  # Internal angle calculated from value.
    _angle_step = NumericProperty(0)  # Internal angle_step calculated from
                                      # step.
    _label = ObjectProperty(None)  # Internal label that show value.

    def __init__(self, *args, **kwargs):
        super(Knob, self).__init__(*args, **kwargs)
        self.bind(show_label=self._show_label)
        self.bind(show_marker=self._show_marker)
        self.bind(value=self._value)

    def _show_label(self, o, value):
        if value and self._label not in self.children:
            self.add_widget(self._label)
        elif not value and self._label in self.children:
            self.remove_widget(self._label)

    def _value(self, o, value):
        self._angle = (value - self.min) * 360. / (-self.min + self.max)

    def _show_marker(self, o, value):
        # This is my "show/hide" of marker.
        if value:
            self.knobimg_bgcolor[3] = 1
            self.marker_color[3] = 1
            self.markeroff_color[3] = 1
        else:
            self.knobimg_bgcolor[3] = 0
            self.marker_color[3] = 0
            self.markeroff_color[3] = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.update_angle(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.update_angle(touch, True)

    def update_angle(self, touch, being_pressed=False):
        posx, posy = touch.pos
        cx, cy = self.center
        rx, ry = posx - cx, posy - cy
        self._angle_step = 360. / ((self.max - self.min + 1) / self.step)

        if ry >= 0:  # Quadrants are clockwise.
            quadrant = 1 if rx >= 0 else 4
        else:
            quadrant = 3 if rx <= 0 else 2

        try:
            angle = math.atan(rx / ry) * 180. / 3.141592
            if quadrant == 2 or quadrant == 3:
                angle = 180 + angle
            elif quadrant == 4:
                angle = 360 + angle
        except:  # atan not def for angle 90 and 270
            angle = 90 if quadrant <= 2 else 270

        if not(being_pressed and abs(angle - self._angle) > 90):
            angle = int(
                self._angle_step * round(float(angle) / self._angle_step))
            if angle != self._angle:
                self.value = (-self.min + self.max) * angle / 360. + self.min


if __name__ == '__main__':
    from kivy.app import App
    from kivy.factory import Factory
    from kivy.config import Config

    class Main(Widget):
        pass

    class TestKnobApp(App):

        def build(self):
            self.root = Main()
            return self.root

    Factory.register('Main', Main)

    Builder.load_string('''
<Main>
    GridLayout:
        pos: root.pos
        size: root.size
        cols: 3
        spacing: 100
        padding: 50

        Knob:
            size: 200, 200
            value: 0
            show_label: True
            font_size: '38sp'
            font_color: 0, 0, 0,1
            show_marker: True
            knobimg_source: "img/knob_metal.png"
            show_marker: False

        Knob:
            size: 200, 200
            value: 0
            show_label: True
            font_size: '38sp'
            font_color: 0, 0, 0,1
            show_marker: True
            knobimg_source: "img/knob_metal.png"
            marker_img: "img/bline.png"
            markeroff_color: 0.3, 0.3, .3, 1

        Knob:
            size: 200, 200
            value: 0
            show_label: True
            font_size: '38sp'
            font_color: 1, 1, 1,1
            show_marker: True
            knobimg_source: ""
            knobimg_color: 0, 0, 0, 0
            marker_img: "img/bline.png"
            markeroff_color: 0, 0, 0, 0
            marker_inner_color: 0, 0, 0, 1

        Knob:
            size: 200, 200
            value: 0
            show_label: True
            font_size: '38sp'
            font_color: 0, 0, 0,1
            show_marker: True
            knobimg_source: "img/knob_metal.png"
            marker_img: "img/bline.png"
            markeroff_color: 0.0, 0.0, .0, 1
            knobimg_size: 0.7

        Knob:
            size: 200, 200
            step: 25
            value: 0
            show_label: True
            font_size: '30sp'
            font_color: 0, 0, 0,1
            show_marker: True
            knobimg_source: "img/knob_metal.png"
            marker_img: "img/bline2.png"
            markeroff_img: "img/bline2_off.png"
            markeroff_color: 0.3, 0.3, .3, 1
            marker_ahead: 6
            knobimg_size: 0.8
            marker_startangle: 6

        Knob:
            size: 200, 200
            value: 0
            show_label: True
            font_size: '38sp'
            font_color: 0, 0, 0,1
            show_marker: True
            knobimg_source: "img/knob_black.png"
            markeroff_color: 0.0, 0.0, .0, 1
            knobimg_size: 0.9
            marker_img: "img/bline3.png"
            font_color: 254/255., 148/255. , 0, 1
            ''')
    Config.set('modules', 'monitor', '')
    TestKnobApp().run()
