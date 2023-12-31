#!/usr/bin/env python3

import ifcopenshell
import ifcopenshell.util.placement
import ifcopenshell.geom
import numpy as np
import sys
import matplotlib.pyplot as plt
import numpy as np
import rospy
from std_msgs.msg import Int32MultiArray, MultiArrayDimension, MultiArrayLayout

class grid3d():
    def __init__(self):

        # Inicializacion del archivo IFC
        rospy.loginfo(sys.path)
        self.model = ifcopenshell.open('/home/rva_container/rva_exchange/catkin_ws/src/IfcGrid/scripts/model.ifc')
        self.settings = ifcopenshell.geom.settings()

        # Elementos a representar
        self.walls = self.model.by_type('IfcWall')
        self.doors = self.model.by_type('IfcDoor')
        self.columns = self.model.by_type('IfcColumn')

        rospy.loginfo("Termina carga de IFC")
        self.world_size_x = rospy.get_param('~world_size_x', 220)
        self.world_size_y = rospy.get_param('~world_size_y', 220)
        self.world_size_z = rospy.get_param('~world_size_z', 20)
        self.resolution = rospy.get_param('~resolution', 0.2)
        self.x_y_size = self.world_size_x * self.world_size_y

        rospy.loginfo("Termina inicializacion de dimensiones")
        self.semantic_grid = np.zeros((int(self.world_size_x / self.resolution), int(self.world_size_y / self.resolution), int(self.world_size_z / self.resolution)), dtype=int)
        self.occ_grid = self.semantic_grid

        rospy.loginfo("Termina inicializacion de los grid a 0")
        self.pub = rospy.Publisher('/semantic_grid', Int32MultiArray, queue_size=10)

        rospy.loginfo("Termina carga de parametros")

        for wall in self.walls:
            matrix = ifcopenshell.util.placement.get_local_placement(wall.ObjectPlacement)
            shape = ifcopenshell.geom.create_shape(self.settings, wall)

            
            points = np.array(shape.geometry.verts).reshape(-1, 3)
            
            # Calcular el centro de la pared
            centro = matrix[:,3][:3]

            rotation_matrix  = matrix[:3, :3]

            
            points = np.dot(points, rotation_matrix)

            # Sumar el centro a las coordenadas de los puntos para obtener su posicion global
            points = (points + centro) / self.resolution
            

            if(len(points) > 8):
                points = self.calcular_extremos(points)
            
            
            points = np.round(points)  # Redondear a un decimal
            
            
            # Calcular valores máximos
            max_x_local = int(np.max(points[:, 0]))
            max_y_local = int(np.max(points[:, 1]))
            max_z_local = int(np.max(points[:, 2]))

            # Calcular valores minimos
            min_x_local = int(np.min(points[:, 0]))
            min_y_local = int(np.min(points[:, 1]))
            min_z_local = int(np.min(points[:, 2]))

            
            # Bucles for para recorrer el espacio entre mínimos y máximos en cada coordenada
            for x in range(min_x_local, max_x_local + 1):
                for y in range(min_y_local, max_y_local + 1):
                    for z in range(min_z_local, max_z_local + 1):
                        self.semantic_grid[x, y, z] = 1
                        self.occ_grid[x, y, z] = 1
                        #rospy.loginfo("Pared rellenada")

        for door in self.doors:
            matrix = ifcopenshell.util.placement.get_local_placement(door.ObjectPlacement)
            shape = ifcopenshell.geom.create_shape(self.settings, door)

            points = np.array(shape.geometry.verts).reshape(-1, 3)
            
            # Calcular el centro de la puerta
            centro = matrix[:,3][:3]
            
            rotation_matrix  = matrix[:3, :3]

            points = np.dot(points, rotation_matrix)
            # Sumar el centro a las coordenadas de los puntos
            points = (points + centro) / self.resolution
            points = np.round(points)  # Redondear a un decimal

         # Calcular valores máximos
            max_x_local = int(np.max(points[:, 0]))
            max_y_local = int(np.max(points[:, 1]))
            max_z_local = int(np.max(points[:, 2]))

            # Calcular valores minimos
            min_x_local = int(np.min(points[:, 0]))
            min_y_local = int(np.min(points[:, 1]))
            min_z_local = int(np.min(points[:, 2]))

            for x in range(min_x_local, max_x_local + 1):
                for y in range(min_y_local, max_y_local + 1):
                    for z in range(min_z_local, max_z_local + 1):
                        self.semantic_grid[x, y, z] = 2
                        self.occ_grid[x, y, z] = 1
                        rospy.loginfo("Puerta rellenada")
    
        for column in self.columns:
            matrix = ifcopenshell.util.placement.get_local_placement(column.ObjectPlacement)
            shape = ifcopenshell.geom.create_shape(self.settings, column)

            points = np.array(shape.geometry.verts).reshape(-1, 3)
            
            # Calcular el centro de la puerta
            centro = matrix[:,3][:3]
            
            rotation_matrix  = matrix[:3, :3]

            points = np.dot(points, rotation_matrix)
            # Sumar el centro a las coordenadas de los puntos
            points = (points + centro) / self.resolution
            points = np.round(points)  # Redondear a un decimal
        

            # Calcular valores máximos
            max_x_local = int(np.max(points[:, 0]))
            max_y_local = int(np.max(points[:, 1]))
            max_z_local = int(np.max(points[:, 2]))

            # Calcular valores minimos
            min_x_local = int(np.min(points[:, 0]))
            min_y_local = int(np.min(points[:, 1]))
            min_z_local = int(np.min(points[:, 2]))

            for x in range(min_x_local, max_x_local + 1):
                for y in range(min_y_local, max_y_local + 1):
                    for z in range(min_z_local, max_z_local + 1):
                        self.semantic_grid[x, y, z] = 3
                        self.occ_grid[x, y, z] = 1
                        rospy.loginfo("Columna rellenada")
    

    rospy.loginfo("Termina de rellenar las matrices")
    def calcular_extremos(self, array):
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
    def calcular_puntos_medios(self, points, n=1):
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
    def calcular_centro(self, vertices):
        vertices = np.array(vertices).reshape(-1, 3)
        centro = np.mean(vertices, axis=0)
        return centro
    def getWorldIndex(self, x, y, z):

        return z * self.x_y_size + y * self.world_size_x + x 
    def getDiscreteWorldPositionFromIndex(self, index):

        z = index / self.x_y_size
        ind = index - (z * self.x_y_size)
        y = ind / self.world_size_x
        x = ind % self.world_size_x

        return (x, y, z)
    def create_layout(self):
        layout = MultiArrayLayout()

        # Create a dimension for the first axis (x)
        dim_x = MultiArrayDimension()
        dim_x.label = "x"
        dim_x.size = int(self.world_size_x / self.resolution)
        dim_x.stride = self.x_y_size
        layout.dim.append(dim_x)

        # Create a dimension for the second axis (y)
        dim_y = MultiArrayDimension()
        dim_y.label = "y"
        dim_y.size = int(self.world_size_y / self.resolution)
        dim_y.stride = self.world_size_x
        layout.dim.append(dim_y)

        # Create a dimension for the third axis (z)
        dim_z = MultiArrayDimension()
        dim_z.label = "z"
        dim_z.size = int(self.world_size_z / self.resolution)
        dim_z.stride = 1  # Since it's the innermost dimension
        layout.dim.append(dim_z)

        layout.data_offset = 0  # This is usually 0

        return layout

    def publish_semantic_grid(self):
        layout = self.create_layout()

        # Create your Int32MultiArray message
        semantic_grid_msg = Int32MultiArray()
        semantic_grid_msg.layout = layout

        # Set the data
        semantic_grid_msg.data = self.semantic_grid.flatten().tolist()

        # Publish the message
        self.pub.publish(semantic_grid_msg)
    

if __name__ == '__main__':
    try:
        rospy.init_node("semantic_grid", anonymous=False)

        g = grid3d()

        rospy.loginfo("Semantic Grid Avaliable")
        r = rospy.Rate(0.1)

        #rospy.loginfo(g.semantic_grid[0, 0, :])
        
        while not rospy.is_shutdown():  # Use rospy.is_shutdown() for the loop condition

            g.publish_semantic_grid()
            r.sleep()

    except Exception as e:
        rospy.loginfo(e)
        rospy.loginfo(f"Error: {e}")

