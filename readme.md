Video: http://youtu.be/Zz7c1OGv2U4

Knob
====

The :class:`Knob` widget creates a component that looks like a
control Knob or Dial (from Wikipedia: "A control knob is a rotary
control used to provide input to a device when grasped by an
operator and turned, so that the degree of rotation corresponds to
the desired input."). To configure a knob a max/min and step values
should be provided (like in Slider). Additionally, knobimg_source
could be set to load a texture that visually represents the knob.

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

License
=======
MIT license.

Credits
=======

- img/knob_metal.png by icondeposit.com (http://www.icondeposit.com/design:dial-version-3-includes-tutorial). Creative Commons Attribution 3.0.

- img/knob_black.ong by gliskard. http://gliskard.deviantart.com/art/UI-KNOB-free-PSD-324742538
