import ifcopenshell
import ifcopenshell.util.placement
import numpy as np
import open3d as o3d

model = ifcopenshell.open('model.ifc')

walls = model.by_type('IfcWall')
doors = model.by_type('IfcDoor')
columns = model.by_type('IfcColumn')

# Listas para almacenar las coordenadas, colores y etiquetas
all_coordinates = []
all_colors = []
all_labels = []

# Color para las paredes: Azul
wall_color = [0, 0, 255]

# Color para las puertas: Rojo
door_color = [255, 0, 0]

# Color para las columnas: Verde
column_color = [0, 255, 0]

for wall in walls:
    matrix = ifcopenshell.util.placement.get_local_placement(wall.ObjectPlacement)
    all_coordinates.append(matrix[:, 3][:3])
    all_colors.append(wall_color)
    all_labels.append("Wall")

for door in doors:
    matrix = ifcopenshell.util.placement.get_local_placement(door.ObjectPlacement)
    all_coordinates.append(matrix[:, 3][:3])
    all_colors.append(door_color)
    all_labels.append("Door")

for column in columns:
    matrix = ifcopenshell.util.placement.get_local_placement(column.ObjectPlacement)
    all_coordinates.append(matrix[:, 3][:3])
    all_colors.append(column_color)
    all_labels.append("Column")

# Convertir las listas en matrices numpy
all_coordinates = np.array(all_coordinates)
all_colors = np.array(all_colors) / 255.0  # Normalizar los valores de color entre 0 y 1

# Crear la nube de puntos y asignar coordenadas y colores
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(all_coordinates)
point_cloud.colors = o3d.utility.Vector3dVector(all_colors)


# Crear un diccionario para almacenar las etiquetas como atributo adicional
#point_cloud.point_labels = o3d.utility.Vector3dVector(all_labels)

# Guardar la nube de puntos en un archivo .pcd
o3d.io.write_point_cloud("nube_de_puntos_con_etiquetas.pcd", point_cloud)
