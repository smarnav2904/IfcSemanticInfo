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

zero_array = np.zeros(((220) + 1, (220) + 1, (4) + 1))




for wall in walls:
    matrix = ifcopenshell.util.placement.get_local_placement(wall.ObjectPlacement)
    #zero_array.append((matrix[:, 3][:3], 1)) # 1 Representa pared
    print("Funciona pared")
    shape = ifcopenshell.geom.create_shape(settings, wall)
    points = np.array(shape.geometry.verts).reshape(-1, 3)
    indices_a_eliminar = [3 - 1, 8 - 1]
    filtered_points = np.delete(points, indices_a_eliminar, axis=0)

    points = np.round(filtered_points).astype(int)

    # Obtener coordenadas X y Z de los puntos
    x_values = points[:, 0]
    y_values = points[:, 1]
    z_values = points[:, 2]
    
    # Calcular los valores máximos y mínimos
    max_x = np.max(x_values)
    min_x = np.min(x_values)
    max_y = np.max(y_values)
    min_y = np.min(y_values)
    max_z = np.max(z_values)
    min_z = np.min(z_values)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                if 0 <= x < 221 and 0 <= y < 221 and 0 <= z < 5:
                    print("X:" + str(x) + " Y:" + str(y) + " Z:" + str(z))
                    if(zero_array[x, y, z] == 0):
                        zero_array[x, y, z] = 1

    

for door in doors:
    matrix = ifcopenshell.util.placement.get_local_placement(door.ObjectPlacement)
    #zero_array.append((matrix[:, 3][:3], 2)) # 2 Representa puerta
    print("Funciona puerta")
    shape = ifcopenshell.geom.create_shape(settings, door)
    points = np.array(shape.geometry.verts).reshape(-1, 3)

    points = np.round(points).astype(int)

    # Obtener coordenadas X y Z de los puntos
    x_values = points[:, 0]
    y_values = points[:, 1]
    z_values = points[:, 2]
    
    # Calcular los valores máximos y mínimos
    max_x = np.max(x_values)
    min_x = np.min(x_values)
    max_y = np.max(y_values)
    min_y = np.min(y_values)
    max_z = np.max(z_values)
    min_z = np.min(z_values)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y+1):
            for z in range(min_z, max_z + 1):
                if 0 <= x < 221 and 0 <= y < 221 and 0 <= z < 5:
                    print("X:" + str(x) + " Y:" + str(y) + " Z:" + str(z))
                    if(zero_array[x, y, z] == 0 or 1):
                        zero_array[x, y, z] = 2

    
    

for column in columns:
    matrix = ifcopenshell.util.placement.get_local_placement(column.ObjectPlacement)
    #zero_array.append((matrix[:, 3][:3], 3)) # 3 Representa columna
    print("Funciona columna")
    shape = ifcopenshell.geom.create_shape(settings, column)
    points = np.array(shape.geometry.verts).reshape(-1, 3)

    points = np.round(points).astype(int)

    # Obtener coordenadas X y Z de los puntos
    x_values = points[:, 0]
    y_values = points[:, 1]
    z_values = points[:, 2]
    
    # Calcular los valores máximos y mínimos
    max_x = np.max(x_values)
    min_x = np.min(x_values)
    max_y = np.max(y_values)
    min_y = np.min(y_values)
    max_z = np.max(z_values)
    min_z = np.min(z_values)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y+1):
            for z in range(min_z, max_z + 1):
                if 0 <= x < 221 and 0 <= y < 221 and 0 <= z < 5:
                    print("X:" + str(x) + " Y:" + str(y) + " Z:" + str(z))
                    if(zero_array[x, y, z] == 0):
                        zero_array[x, y, z] = 3


print(zero_array)

    


