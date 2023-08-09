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
    
}
    