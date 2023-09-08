import ifcopenshell
import ifcopenshell.util.placement
import ifcopenshell.geom
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

import numpy as np

def calcular_extremos(array):
    # Obtener los valores máximos y mínimos en cada dimensión
    min_x = np.min(array[:,0])
    max_x = np.max(array[:,0])
    min_y = np.min(array[:,1])
    max_y = np.max(array[:,1])
    min_z = np.min(array[:,2])
    max_z = np.max(array[:,2])

    # Crear arrays para los mínimos y máximos de cada dimensión
    extremos_x = np.array([min_x, max_x])
    extremos_y = np.array([min_y, max_y])
    extremos_z = np.array([min_z, max_z])

    # Crear combinaciones de puntos
    combinaciones = []

    for x in extremos_x:
        for y in extremos_y:
            for z in extremos_z:
                combinaciones.append([x, y, z])

    return np.array(combinaciones)
def calcular_puntos_medios(points, n=1):
    new_points = list(points)
    for _ in range(n):
        temp_points = list(new_points)
        for i in range(len(points)):
            p1 = temp_points[i]
            p2 = temp_points[(i + 1) % len(points)]  # El último punto se conecta con el primero
            medio = (p1 + p2) / 2.0
            # Verificar si el punto medio ya está en la lista antes de agregarlo
            if not any(np.array_equal(medio, p) for p in new_points):
                new_points.append(medio)
    return np.array(new_points)
def calcular_centro(vertices):
    vertices = np.array(vertices).reshape(-1, 3)
    centro = np.mean(vertices, axis=0)
    return centro


# Inicializacion del archivo IFC
model = ifcopenshell.open('model.ifc')
settings = ifcopenshell.geom.settings()

# Elementos a representar
walls = model.by_type('IfcWall')
doors = model.by_type('IfcDoor')
columns = model.by_type('IfcColumn')


grid3d = np.zeros((2371, 1001, 81), dtype=int)
occ_grid = grid3d

for wall in walls:
    matrix = ifcopenshell.util.placement.get_local_placement(wall.ObjectPlacement)
    shape = ifcopenshell.geom.create_shape(settings, wall)

    points = np.array(shape.geometry.verts).reshape(-1, 3)
    
    # Calcular el centro de la pared
    centro = matrix[:,3][:3]

    # Sumar el centro a las coordenadas de los puntos para obtener su posicion global
    points = points + centro
    

    if(len(points) > 8):
        
        points = calcular_extremos(points)
        
    points = np.round(points, 1)  # Redondear a un decimal
    points = (points * 10).astype(int)
    
    # Calcular valores máximos
    max_x_local = np.max(points[:, 0])
    max_y_local = np.max(points[:, 1])
    max_z_local = np.max(points[:, 2])

    # Calcular valores minimos
    min_x_local = np.min(points[:, 0])
    min_y_local = np.min(points[:, 1])
    min_z_local = np.min(points[:, 2])

    # Bucles for para recorrer el espacio entre mínimos y máximos en cada coordenada
    for x in range(min_x_local, max_x_local + 1):
        for y in range(min_y_local, max_y_local + 1):
            for z in range(min_z_local, max_z_local + 1):
                grid3d[x, y, z] = 1
                occ_grid[x, y, z] = 1


    
for door in doors:
    matrix = ifcopenshell.util.placement.get_local_placement(door.ObjectPlacement)
    shape = ifcopenshell.geom.create_shape(settings, door)

    points = np.array(shape.geometry.verts).reshape(-1, 3)
    
    # Calcular el centro de la puerta
    centro = matrix[:,3][:3]
    
    points = points[:8]
    # Sumar el centro a las coordenadas de los puntos
    points = points + centro
    points = np.round(points, 1)  # Redondear a un decimal
    points = (points * 10).astype(int)

 # Calcular valores máximos
    max_x_local = np.max(points[:, 0])
    max_y_local = np.max(points[:, 1])
    max_z_local = np.max(points[:, 2])

    # Calcular valores minimos
    min_x_local = np.min(points[:, 0])
    min_y_local = np.min(points[:, 1])
    min_z_local = np.min(points[:, 2])

    for x in range(min_x_local, max_x_local + 1):
        for y in range(min_y_local, max_y_local + 1):
            for z in range(min_z_local, max_z_local + 1):
                grid3d[x, y, z] = 2
                occ_grid[x, y, z] = 1



for column in columns:
    matrix = ifcopenshell.util.placement.get_local_placement(column.ObjectPlacement)
    shape = ifcopenshell.geom.create_shape(settings, column)

    points = np.array(shape.geometry.verts).reshape(-1, 3)
    
    # Calcular el centro de la puerta
    centro = matrix[:,3][:3]
    
    
    # Sumar el centro a las coordenadas de los puntos
    points = points + centro
    points = np.round(points, 1)  # Redondear a un decimal
    points = (points * 10).astype(int)

      # Calcular valores máximos
    max_x_local = np.max(points[:, 0])
    max_y_local = np.max(points[:, 1])
    max_z_local = np.max(points[:, 2])

    # Calcular valores minimos
    min_x_local = np.min(points[:, 0])
    min_y_local = np.min(points[:, 1])
    min_z_local = np.min(points[:, 2])

    for x in range(min_x_local, max_x_local + 1):
        for y in range(min_y_local, max_y_local + 1):
            for z in range(min_z_local, max_z_local + 1):
                grid3d[x, y, z] = 3
                occ_grid[x, y, z] = 1

    
