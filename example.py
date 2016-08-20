from kivy.base  import  runTouchApp
from kivy.lang  import  Builder
from kivy.garden.knob import  Knob

# LOAD KV UIX
runTouchApp(Builder.load_file('example.kv'))
