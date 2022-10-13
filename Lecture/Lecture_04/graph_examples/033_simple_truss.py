import compas.geometry as cg
import compas.datastructures as cd

# Create top and bottom plates

b_s = (0, 1, 0)
b_e = (20, 1, 0)
t_s = (0, 10, 0)
t_e = (20, 10, 0)

top_plate_line = cg.Line(b_s, b_e)
bottom_plate_line = cg.Line(t_s, t_e)

network = cd.Network()

top_plate_id = network.add_node(
    attr_dict={
        "type": "plate",
        "topology": top_plate_line
    }
)

bottom_plate_id = network.add_node(
    attr_dict={
        "type": "plate",
        "topology": bottom_plate_line
    }
)

top_params = [0.1, 0.3, 0.5, 0.9]
bottom_params = [0.2, 0.3, 0.6, 0.8]


for i in range(4):
    top_plate_pt = top_plate_line.point(top_params[i])
    bottom_plate_pt = bottom_plate_line.point(bottom_params[i])
    stud_line = cg.Line(
        top_plate_pt,
        bottom_plate_pt
    )
    stud_id = network.add_node(
        attr_dict={
            "type": "stud",
            "topology": stud_line
        }
    )
    network.add_edge(
        stud_id,
        top_plate_id,
        attr_dict={
            "type": "plate-stud",
            "location": top_plate_pt
        }
    )
    network.add_edge(
        stud_id,
        bottom_plate_id,
        attr_dict={
            "type": "plate-stud",
            "location": bottom_plate_pt
        }
    )
