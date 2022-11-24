from walker import Walker
from compas_view2.app import App

walkers = [Walker() for i in range(3)]

geometries = []

for i in range(100):
    for walker in walkers:
        walker.walking()
        geometries.append(walker.draw())


viewer = App()
for geometry in geometries:
    viewer.add(geometry)
viewer.run()
