import compas.datastructures as cd
from compas import is_grasshopper


mesh = cd.Mesh.from_polyhedron(4)

(v, _) = mesh.to_vertices_and_faces()

v = list(v)
f = []


def mid_point(v1, v2):
    mid = []
    for i in range(len(v1)):
        mid.append((v1[i] + v2[i])/2)
    return mid


def sierpinski(v_keys, depth=0, max_depth=5):
    if depth < max_depth:
        mid_0_1 = mid_point(v[v_keys[0]], v[v_keys[1]])
        mid_0_2 = mid_point(v[v_keys[0]], v[v_keys[2]])
        mid_0_3 = mid_point(v[v_keys[0]], v[v_keys[3]])
        mid_1_2 = mid_point(v[v_keys[1]], v[v_keys[2]])
        mid_1_3 = mid_point(v[v_keys[1]], v[v_keys[3]])
        mid_2_3 = mid_point(v[v_keys[2]], v[v_keys[3]])

        v.append(mid_0_1)
        key_0_1 = len(v) - 1
        v.append(mid_0_2)
        key_0_2 = len(v) - 1
        v.append(mid_0_3)
        key_0_3 = len(v) - 1
        v.append(mid_1_2)
        key_1_2 = len(v) - 1
        v.append(mid_1_3)
        key_1_3 = len(v) - 1
        v.append(mid_2_3)
        key_2_3 = len(v) - 1

        new_v_keys = (
            (v_keys[0], key_0_1, key_0_2, key_0_3),
            (key_0_1, v_keys[1], key_1_2, key_1_3),
            (key_0_2, key_1_2, v_keys[2], key_2_3),
            (key_0_3, key_1_3, key_2_3, v_keys[3])
        )
        new_depth = depth + 1
        for new_v_key in new_v_keys:
            sierpinski(new_v_key, new_depth, max_depth)
    else:
        f.extend(
            [(v_keys[0], v_keys[2], v_keys[1]),
             (v_keys[0], v_keys[1], v_keys[3]),
             (v_keys[0], v_keys[3], v_keys[2]),
             (v_keys[1], v_keys[2], v_keys[3])]
        )


sierpinski((0, 1, 2, 3), 0, 5)
mesh = cd.Mesh.from_vertices_and_faces(v, f)

if is_grasshopper():
    a = mesh
else:
    from compas_view2.app import App
    viewer = App()
    viewer.add(mesh)
    viewer.run()
