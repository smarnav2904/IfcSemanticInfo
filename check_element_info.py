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




# for wall in walls:
#     matrix = ifcopenshell.util.placement.get_local_placement(wall.ObjectPlacement)
#     #zero_array.append((matrix[:, 3][:3], 1)) # 1 Representa pared
#     shape = ifcopenshell.geom.create_shape(settings, wall)
#     points = np.array(shape.geometry.verts).reshape(-1, 3)
#     indices_a_eliminar = [3 - 1, 8 - 1]
#     filtered_points = np.delete(points, indices_a_eliminar, axis=0)

#     points = np.round(filtered_points).astype(int)

    
#     # Obtener coordenadas X y Z de los puntos
#     x_values = points[:, 0]
   
#     y_values = points[:, 1]

#     z_values = points[:, 2]

    
#     # Calcular los valores máximos y mínimos
#     max_x = np.max(x_values)
#     min_x = np.min(x_values)
#     max_y = np.max(y_values)
#     min_y = np.min(y_values)
#     max_z = np.max(z_values)
#     min_z = np.min(z_values)

#     for x in range(min_x, max_x + 1):
#         for y in range(min_y, max_y + 1):
#             for z in range(min_z, max_z + 1):
#                 if 0 <= x < 221 and 0 <= y < 221 and 0 <= z < 5:
#                     if(zero_array[x, y, z] == 0):
#                         zero_array[x, y, z] = 1

    

# for door in doors:
#     matrix = ifcopenshell.util.placement.get_local_placement(door.ObjectPlacement)
#     #zero_array.append((matrix[:, 3][:3], 2)) # 2 Representa puerta
#     shape = ifcopenshell.geom.create_shape(settings, door)
#     points = np.array(shape.geometry.verts).reshape(-1, 3)

#     points = np.round(points).astype(int)

#     # Obtener coordenadas X y Z de los puntos
#     x_values = points[:, 0]
#     y_values = points[:, 1]
#     z_values = points[:, 2]
    
#     # Calcular los valores máximos y mínimos
#     max_x = np.max(x_values)
#     min_x = np.min(x_values)
#     max_y = np.max(y_values)
#     min_y = np.min(y_values)
#     max_z = np.max(z_values)
#     min_z = np.min(z_values)

#     for x in range(min_x, max_x + 1):
#         for y in range(min_y, max_y+1):
#             for z in range(min_z, max_z + 1):
#                 if 0 <= x < 221 and 0 <= y < 221 and 0 <= z < 5:
#                     if(zero_array[x, y, z] == 0 or 1):
#                         zero_array[x, y, z] = 2

matrix = ifcopenshell.util.placement.get_local_placement(doors[2].ObjectPlacement)

psets = ifcopenshell.util.element.get_psets(doors[2])
print(psets['Dimensions'])
print("-------------------")
x, y, z = np.round(matrix[:, 3][:3])
print(matrix)
zero_array[int(x), int(abs(y)), int(z)] = 2
shape = ifcopenshell.geom.create_shape(settings, doors[0])
points = np.array(shape.geometry.verts).reshape(-1, 3)
print("---------------------------------------------")
print(shape.geometry.verts)

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
                if(zero_array[x, y, z] == 0 or 1):
                    zero_array[x, y, z] = 2

    
    

# for column in columns:
#     matrix = ifcopenshell.util.placement.get_local_placement(column.ObjectPlacement)
#     #zero_array.append((matrix[:, 3][:3], 3)) # 3 Representa columna
#     shape = ifcopenshell.geom.create_shape(settings, column)
#     points = np.array(shape.geometry.verts).reshape(-1, 3)

#     points = np.round(points).astype(int)

#     # Obtener coordenadas X y Z de los puntos
#     x_values = points[:, 0]
#     y_values = points[:, 1]
#     z_values = points[:, 2]
    
#     # Calcular los valores máximos y mínimos
#     max_x = np.max(x_values)
#     min_x = np.min(x_values)
#     max_y = np.max(y_values)
#     min_y = np.min(y_values)
#     max_z = np.max(z_values)
#     min_z = np.min(z_values)

#     for x in range(min_x, max_x + 1):
#         for y in range(min_y, max_y+1):
#             for z in range(min_z, max_z + 1):
#                 if 0 <= x < 221 and 0 <= y < 221 and 0 <= z < 5:
#                     if(zero_array[x, y, z] == 0):
#                         zero_array[x, y, z] = 3


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a meshgrid for the x, y, and z coordinates
x, y, z = np.meshgrid(
    np.arange(zero_array.shape[0]),
    np.arange(zero_array.shape[1]),
    np.arange(zero_array.shape[2])
)

# Flatten the arrays and filter non-zero values for plotting
x_vals = x.flatten()
y_vals = y.flatten()
z_vals = z.flatten()
values = zero_array.flatten()
non_zero_indices = values > 0

# Scatter plot the non-zero values
ax.scatter(x_vals[non_zero_indices], y_vals[non_zero_indices], z_vals[non_zero_indices], c=values[non_zero_indices], cmap='viridis')

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Matrix Plot of zero_array')

# Show the plot
plt.show()

    


