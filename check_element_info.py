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


#Inicializacion del archivo IFC
model = ifcopenshell.open('model.ifc')
settings = ifcopenshell.geom.settings()

#Elementos a representar
walls = model.by_type('IfcWall')
doors = model.by_type('IfcDoor')
columns = model.by_type('IfcColumn')

# Crear un archivo de texto para guardar los puntos y centros
output_file_gt_3 = open('puertas_z_mayor_3.txt', 'w')
output_file_lt_3 = open('puertas_z_menor_3.txt', 'w')
count = 0
normal_walls = 0
rare_walls = 0

# Crear una figura 3D para visualizar los puntos
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for wall in walls:
    matrix = ifcopenshell.util.placement.get_local_placement(wall.ObjectPlacement)
    shape = ifcopenshell.geom.create_shape(settings, wall)

    points = np.array(shape.geometry.verts).reshape(-1, 3)
    
    # Calcular el centro de la pared
    centro = matrix[:,3][:3]

    rotation_matrix  = matrix[:3, :3]

    points = np.dot(points, rotation_matrix)
    # Sumar el centro a las coordenadas de los puntos para obtener su posicion global
    points = points + centro
    
    if(len(points) > 8):
        
        points = calcular_extremos(points)

    
    # # Escribir los puntos de la pared en el archivo
    # for i, point in enumerate(points):
    #     output_file.write(f'{count} {point[0]} {point[1]} {point[2]}\n')
    
    # Visualizar los puntos en la matriz 3D
    if(len(points)):
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], marker='.', c='red')

    count += 1

count = 0

for door in doors:
    matrix = ifcopenshell.util.placement.get_local_placement(door.ObjectPlacement)
    shape = ifcopenshell.geom.create_shape(settings, door)

    points = np.array(shape.geometry.verts).reshape(-1, 3)
    
    # Calcular el centro de la puerta
    centro = matrix[:,3][:3]
    
    rotation_matrix  = matrix[:3, :3]

    points = np.dot(points, rotation_matrix)
    # Sumar el centro a las coordenadas de los puntos
    points = points + centro
    
    if(len(points)):
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], marker='.', c='blue')

    if centro[2] > 3:
        for point in points:
            output_file_gt_3.write(f'{count} {point[0]} {point[1]} {point[2]}\n')
    else:
        for point in points:
            output_file_lt_3.write(f'{count} {point[0]} {point[1]} {point[2]}\n')
    
    # Visualizar los puntos en la matriz 3D
  
    
    count += 1

count = 0

for column in columns:
    matrix = ifcopenshell.util.placement.get_local_placement(column.ObjectPlacement)
    shape = ifcopenshell.geom.create_shape(settings, column)

    points = np.array(shape.geometry.verts).reshape(-1, 3)
    
    # Calcular el centro de la puerta
    centro = matrix[:,3][:3]
    
    
    rotation_matrix  = matrix[:3, :3]

    points = np.dot(points, rotation_matrix)
    # Sumar el centro a las coordenadas de los puntos
    points = points + centro
    
    
    
    #Visualizar los puntos en la matriz 3D
    if(len(points)):
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], marker='.', c='green')

    count += 1

# Mostrar la matriz 3D
ax.axis("equal")
plt.show()

# Cerrar el archivo de texto
output_file_gt_3.close()
output_file_lt_3.close()

