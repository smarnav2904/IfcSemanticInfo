import ifcopenshell
import ifcopenshell.util.placement
import ifcopenshell.geom
import numpy as np
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import open3d as o3d

model = ifcopenshell.open('model.ifc')
settings = ifcopenshell.geom.settings()
walls = model.by_type('IfcWall')


doors = model.by_type('IfcDoor')

columns = model.by_type('IfcColumn')

# Listas para almacenar las coordenadas
all_coordinates = []

for wall in walls:
    matrix = ifcopenshell.util.placement.get_local_placement(wall.ObjectPlacement)
    all_coordinates.append((matrix[:, 3][:3], 1)) # 1 Representa pared

    shape = ifcopenshell.geom.create_shape(settings, wall)
    points = np.array(shape.geometry.verts).reshape(-1, 3)
    indices_a_eliminar = [3 - 1, 8 - 1]
    filtered_points = np.delete(points, indices_a_eliminar, axis=0)

    for vert in filtered_points:
        all_coordinates.append((vert, 1))

for door in doors:
    matrix = ifcopenshell.util.placement.get_local_placement(door.ObjectPlacement)
    all_coordinates.append((matrix[:, 3][:3], 2)) # 2 Representa puerta

    shape = ifcopenshell.geom.create_shape(settings, door)
    points = np.array(shape.geometry.verts).reshape(-1, 3)

    for vert in points:
        all_coordinates.append((vert, 2))
    

for column in columns:
    matrix = ifcopenshell.util.placement.get_local_placement(column.ObjectPlacement)
    all_coordinates.append((matrix[:, 3][:3], 3)) # 3 Representa columna

    shape = ifcopenshell.geom.create_shape(settings, column)
    points = np.array(shape.geometry.verts).reshape(-1, 3)

    for vert in points:
        all_coordinates.append((vert, 3))
    

# Convertir la lista de coordenadas en una única matriz numpy
#all_coordinates = np.array(all_coordinates)

max_x = np.max([coord[0] for coord, _ in all_coordinates])
max_y = np.max([coord[1] for coord, _ in all_coordinates])
max_z = np.max([coord[2] for coord, _ in all_coordinates])


max_x = int(np.round(max_x))
max_y = int(np.round(max_y))
max_z = int(np.round(max_z))

#print("Coordenadas máximas:")
#print("X más alta:", max_x)
#print("Y más alta:", max_y)
#print("Z más alta:", max_z)


resolution = 1

zero_array = np.zeros(((max_x * resolution) + 1, (max_y * resolution) + 1, (max_z * resolution) + 1))

for coord, elem_type in all_coordinates:
    rounded_coord = tuple(round(value) for value in coord)
    x, y, z = rounded_coord * resolution
    zero_array[x, y, z] = elem_type

print(zero_array)

