import compas.geometry as cg

def draw_frame(frame, viewer, axis_length=1.0, polygon_size=0.3):
    # assumes compas.geometry as cg and viewer exist in the notebook
    # normalize and safe helpers
    def _point_translate(p, v, s=1.0):
        return cg.Point(p.x + v.x * s, p.y + v.y * s, p.z + v.z * s)

    # build a compas Frame if a Line was provided
    if isinstance(frame, cg.Frame):
        fr = frame
    elif isinstance(frame, cg.Line):
        v = cg.Vector.from_start_end(frame.start, frame.end)
        xaxis = v.unitized()
        z = cg.Vector(0, 0, 1)
        yaxis = z.cross(xaxis)
        if yaxis.length < 1e-9:
            yaxis = cg.Vector(0, 1, 0)
        else:
            yaxis = yaxis.unitized()
        fr = cg.Frame(frame.end, xaxis, yaxis)
    else:
        raise TypeError("frame must be a compas.geometry.Frame or compas.geometry.Line")

    origin = fr.point

    # X axis (red)
    x_end = _point_translate(origin, fr.xaxis, axis_length)
    x_line = cg.Line(origin, x_end)
    viewer.scene.add(x_line, color=(255, 0, 0))

    # Y axis (green)
    y_end = _point_translate(origin, fr.yaxis, axis_length)
    y_line = cg.Line(origin, y_end)
    viewer.scene.add(y_line, color=(0, 255, 0))

    # simple square polygon in the frame plane (centered at origin)
    s = polygon_size
    p1 = _point_translate(origin, fr.xaxis + fr.yaxis, s)
    p2 = _point_translate(origin, -fr.xaxis + fr.yaxis, s)
    p3 = _point_translate(origin, -fr.xaxis - fr.yaxis, s)
    p4 = _point_translate(origin, fr.xaxis - fr.yaxis, s)
    poly = cg.Polygon([p1, p2, p3, p4])
    viewer.scene.add(poly, color=(200, 200, 200))