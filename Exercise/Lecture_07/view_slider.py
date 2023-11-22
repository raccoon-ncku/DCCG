from compas.geometry import Point, Polyline, Bezier
from compas.colors import Color
from compas_view2.app import App

curve = Bezier([[0, 0, 0], [3, 6, 0], [5, -3, 0], [10, 0, 0]])

# Enable dsginated side dock 1 and 2. These are fix designated areas where the content can be dynamically created and replaced.
viewer = App(viewmode="shaded", enable_sidebar=True, enable_sidedock1=True, enable_sidedock2=True, width=1600, height=900)
pointobj = viewer.add(Point(* curve.point(0)), pointsize=20, pointcolor=(1, 0, 0))
curveobj = viewer.add(Polyline(curve.locus()), linewidth=2)

viewer.sidedock1.setWindowTitle("Designated Area 1")
viewer.sidedock2.setWindowTitle("Designated Area 2")


@viewer.button(text="Control Set 1 - Area 1")
def click():

    viewer.sidedock1.setWindowTitle("Control Set 1") # Change the title of the side dock
    viewer.sidedock1.clear() # Clear the content of the dock

    # Add a checkbox to the side dock, make sure set the parent to sidedock1.content_layout
    @viewer.checkbox(text="Show Point", checked=True, parent=viewer.sidedock1.content_layout)
    def check(checked):
        pointobj.is_visible = checked
        viewer.view.update()


# Overwriting the sidedock1 with new content
@viewer.button(text="Control Set 2 - Area 1")
def click():
    viewer.sidedock1.setWindowTitle("Control Set 2")
    viewer.sidedock1.clear()

    @viewer.slider(title="Slide Point", maxval=100, step=1, bgcolor=Color.white(), parent=viewer.sidedock1.content_layout)
    def slide(value):
        value = value / 100
        pointobj._data = curve.point(value)
        pointobj.update()
        viewer.view.update()

    @viewer.button(text="Reset", parent=viewer.sidedock1.content_layout)
    def click():
        if viewer.confirm('This will reset the point to parameter t=0.'):
            pointobj._data = curve.point(0)
            pointobj.update()
            slide.value = 0
            viewer.view.update()


# Populating sidedock2
@viewer.button(text="Control Set 3 - Area 2")
def click():
    viewer.sidedock2.clear()

    @viewer.radio(title='Display', items=[
        {'text': 'Ghosted', 'value': 'ghosted', 'checked': viewer.view.mode == 'ghosted'},
        {'text': 'Shaded', 'value': 'shaded', 'checked': viewer.view.mode == 'shaded'},
        {'text': 'Lighted', 'value': 'lighted', 'checked': viewer.view.mode == 'lighted'},
        {'text': 'Wireframe', 'value': 'wireframe', 'checked': viewer.view.mode == 'wireframe'}
    ], parent=viewer.sidedock2.content_layout)
    def select1(value):
        viewer.view.mode = value
        viewer.view.update()

    @viewer.select(items=[
        {'text': 'Item 1'},
        {'text': 'Item 2'},
        {'text': 'Item 3'},
        {'text': 'Item 4'}
    ], parent=viewer.sidedock2.content_layout)
    def select2(index, text):
        viewer.info(f"You selected item '{index}' with text '{text}'")

# Open a dock window as popup.
@viewer.button(text="Control Set 4 - Popup")
def click():
    popup = viewer.popup("This is a popup")

    properties = {
        'text': 'Item 1',
        'num': 1,
    }

    @viewer.select(items=[
        {'text': 'Item 1'},
        {'text': 'Item 2'},
        {'text': 'Item 3'},
        {'text': 'Item 4'}
    ], parent=popup.content_layout)
    def select(index, text):
        properties['text'] = text

    @viewer.slider(title="Choose a number", maxval=100, step=1, bgcolor=Color.white(), parent=popup.content_layout)
    def slide(value):
        properties['num'] = value

    @viewer.button(text="OK", parent=popup.content_layout)
    def click():
        viewer.info(f"Property updated: {properties}")
        popup.close()


viewer.run()