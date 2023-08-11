#define IfcSchema Ifc4

#include <iostream>
#include <string>

#include <ifcparse/IfcFile.h>
#include <ifcparse/Ifc4.h>
#include <ifcparse/IfcSchema.h>

int main(){

    IfcParse::IfcFile file("archivo.ifc");    

    IfcSchema::IfcWindow::list::ptr windows = file.instances_by_type<IfcSchema::IfcWindow>();

    IfcSchema::IfcWall::list::ptr walls = file.instances_by_type<IfcSchema::IfcWall>();

    IfcSchema::IfcDoor::list::ptr doors = file.instances_by_type<IfcSchema::IfcDoor>();

    
    for (IfcSchema::IfcWindow::list::it it = windows->begin(); it != windows->end(); ++it) {
		
        IfcSchema::IfcObjectPlacement position;
		const IfcSchema::IfcWindow* w = *it;
		const IfcSchema::IfcWindow* window;

		if ((window = w->as<IfcSchema::IfcWindow>()) != 0) {
            position = window->ObjectPlacement();
			
		}

	}

    for (IfcSchema::IfcWall::list::it it = walls->begin(); it != walls->end(); ++it) {
		
        IfcSchema::IfcObjectPlacement position;
		const IfcSchema::IfcWall* w = *it;
		const IfcSchema::IfcWall* wall;
        
		if ((wall = w->as<IfcSchema::IfcWall>()) != 0) {
            position = wall->ObjectPlacement();
			
		}

	}

    for (IfcSchema::IfcDoor::list::it it = doors->begin(); it != doors->end(); ++it) {
		
        IfcSchema::IfcObjectPlacement position;
		const IfcSchema::IfcDoor* w = *it;
		const IfcSchema::IfcDoor* door;
        
		if ((door = w->as<IfcSchema::IfcDoor>()) != 0) {
            position = door->ObjectPlacement();
			
		}

	}
}
    