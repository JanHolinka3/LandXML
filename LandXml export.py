import bpy
import math
import bmesh

#from active collection loop all objects: 3 type objects: with faces (tris only), with only egdes, with only verts
#create TIN surface from face objects 
#create breakLines from edges - you need 1 object for every continuus line - named by object name - order is solved by algorymt (Blender can have edges in any order)
#create CgPoints from vert type object - you need only one such object, name by vert index

#control checks and UI will maybe added in future, unexpected results and behavior will most probably occur if you dont follow the rules

#testik

projectName = "model zlaby proviz 3"
fileName = "UniControl/vytycovaci modely/zlaby proviz model3.xml"

if bpy.context.active_object.mode == 'EDIT':
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

#hodnoty z importu
odecetX=782700.0
odecetY=1197500.0
odecetZ=720.0

pripocetX = 782700.0
pripocetY = 1197500.0
pripocetZ = 720.0

znamenko = 1

aktivniKolekce = bpy.context.view_layer.active_layer_collection.collection

listMeshObj = []
listLineObj = []
listPointsObj = []
def rozdelObjekty():
    for obj in aktivniKolekce.objects:
        if obj.type == 'MESH':
            if len(obj.data.polygons) > 0:
                listMeshObj.append(obj)
            elif len(obj.data.edges) > 0:
                listLineObj.append(obj)
            elif len(obj.data.vertices) > 0:
                listPointsObj.append(obj)
    print(listMeshObj)
    print(listLineObj)
    print(listPointsObj)

rozdelObjekty()

def zapisXml():
    with open(fileName, "w") as file:
        file.write("<?xml version=\"1.0\"?>\n")
        
        file.write("<LandXML xmlns=\"http://www.landxml.org/schema/LandXML-1.2\" ")
        file.write("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" ")
        file.write("xsi:schemaLocation=\"http://www.landxml.org/schema/LandXML-1.2 http://www.landxml.org/schema/LandXML-1.2/LandXML-1.2.xsd\" ")
        file.write("version=\"1.2\" date=\"2025-01-01\" time=\"11:11:11\" language=\"English\" readOnly=\"false\">\n")
        
        file.write("  <Units>\n")
        file.write("    <Metric linearUnit=\"meter\" areaUnit=\"squareMeter\" volumeUnit=\"cubicMeter\" />\n")
        file.write("  </Units>\n")
        
        '''
        file.write("  <CoordinateSystem desc=\"SCS900 Localizations (1)\" ") 
        file.write("ogcWktCode=\"PROJCS[&quot;SCS900 Record&quot;,GEOGCS[&quot;WGS 1984&quot;,DATUM[&quot;WGS 1984&quot;,")
        file.write("SPHEROID[&quot;World Geodetic System 1984&quot;,6378137,298.2572229329]],PRIMEM[&quot;Greenwich&quot;,0,AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],")
        file.write("UNIT[&quot;Degree&quot;,0.01745329251994,AUTHORITY[&quot;EPSG&quot;,&quot;9102&quot;]],AXIS[&quot;Long&quot;,EAST],AXIS[&quot;Lat&quot;,NORTH]],")
        file.write("PROJECTION[&quot;Transverse_Mercator&quot;],PARAMETER[&quot;False_Easting&quot;,734952.974],PARAMETER[&quot;False_Northing&quot;,1144347.092],")
        file.write("PARAMETER[&quot;Latitude_Of_Origin&quot;,49.194042861],PARAMETER[&quot;Central_Meridian&quot;,14.717576757],PARAMETER[&quot;Scale_Factor&quot;,1.000071977],")
        file.write("UNIT[&quot;Meter&quot;,1,AUTHORITY[&quot;EPSG&quot;,&quot;9001&quot;]],AXIS[&quot;East&quot;,EAST],AXIS[&quot;North&quot;,NORTH]]\" />\n")
        '''
        
        file.write("  <Application name=\"Blender\" desc=\"Topo\" version=\"4.3.2\" manufacturer=\"Blender Foundation\" ")
        file.write("manufacturerURL=\"www.blender.org\" />\n")
        
        file.write("  <Surfaces>\n")

        for obj in listMeshObj:
            meshObjektu = obj.data
            bm = bmesh.new()   # create an empty BMesh
            bm.from_mesh(meshObjektu)   # fill it in from a Mesh
            bmesh.ops.triangulate(bm, faces=bm.faces[:])
            
            file.write("    <Surface name=\"" + obj.name + "\">\n")
            file.write("      <Definition surfType=\"TIN\">\n")
            file.write("        <Pnts>\n")
            
            for vert in bm.verts:
                file.write("          <P id=\"" + str(vert.index + 1) + "\">")
                xSour = (vert.co[1]+pripocetY)*znamenko
                file.write(str("{:.3f}".format(xSour)) + " ")
                ySour = (vert.co[0]+pripocetX)*znamenko
                file.write(str("{:.3f}".format(ySour)) + " ")
                zSour = vert.co[2]+pripocetZ
                file.write(str("{:.3f}".format(zSour)))
                #pridat vyjimku pro posledni radek
                file.write("</P>\n")
            file.write("        </Pnts>\n")
            file.write("        <Faces>\n")
            for face in bm.faces:
                file.write("          <F>")
                counter = 0
                for vert in face.verts:
                    counter = counter + 1
                    if counter == 3:
                        file.write(str(vert.index + 1))
                    else:
                        file.write(str(vert.index + 1) + " ")
                file.write("</F>\n")
            file.write("        </Faces>\n")
            file.write("      </Definition>\n") 
            file.write("    </Surface>\n")
            bm.free()

        
        #for obj in listLineObj:
        if listLineObj:
            file.write("    <Surface name=\"lines\">\n")
            file.write("      <SourceData>\n")
            file.write("        <Breaklines>\n")
            for obj in listLineObj:
                meshObjektu = obj.data
                bm = bmesh.new()   # create an empty BMesh
                bm.from_mesh(meshObjektu)   # fill it in from a Mesh
                
                file.write("          <Breakline brkType=\"standard\" name=\"" + obj.name + "\">\n")

                file.write("            <PntList3D>")
                for vert in bm.verts:
                    listProslychEdges = []
                    listProslychVerts = []
                    if len(vert.link_edges) == 1:#po prvnim krajnim vert koncime

                        xSour = (vert.co[1]+pripocetY)*znamenko
                        file.write(str("{:.3f}".format(xSour)) + " ")
                        ySour = (vert.co[0]+pripocetX)*znamenko
                        file.write(str("{:.3f}".format(ySour)) + " ")
                        zSour = vert.co[2]+pripocetZ
                        file.write(str("{:.3f}".format(zSour)) + " ")

                        listProslychVerts.append(vert.index)

                        currentEdges = vert.link_edges
                        currentVerts = currentEdges[0].verts
                        for vert2 in currentVerts:
                            if vert2.index != vert.index:
                                xSour = (vert2.co[1]+pripocetY)*znamenko
                                file.write(str("{:.3f}".format(xSour)) + " ")
                                ySour = (vert2.co[0]+pripocetX)*znamenko
                                file.write(str("{:.3f}".format(ySour)) + " ")
                                zSour = vert2.co[2]+pripocetZ
                                file.write(str("{:.3f}".format(zSour)) + " ")
                                listProslychVerts.append(vert2.index)
                                break
                        listProslychEdges.append(currentEdges[0].index)

                        while True:
                            #ted se to bude opakovat - dame asi nejaky while s boolem nebo spis break, ktery se aktivuje az bude zase if len(vert.link_edges) == 1
                            if len(vert2.link_edges) == 1:
                                break #pridat break 

                            connectedEdges = vert2.link_edges
                            #projdu connectedEdges a ten ktery tam neni v listProslychEdges je nas nasledujici edge
                            for edge in connectedEdges:
                                if edge.index not in listProslychEdges:
                                    break
                            listProslychEdges.append(edge.index)
                            currentVerts = edge.verts
                            for vert in currentVerts:
                                if vert.index not in listProslychVerts:
                                    xSour = (vert.co[1]+pripocetY)*znamenko
                                    file.write(str("{:.3f}".format(xSour)) + " ")
                                    ySour = (vert.co[0]+pripocetX)*znamenko
                                    file.write(str("{:.3f}".format(ySour)) + " ")
                                    zSour = vert.co[2]+pripocetZ
                                    file.write(str("{:.3f}".format(zSour)) + " ")
                                    listProslychVerts.append(vert.index)
                                    vert2=vert
                                    break
                        break
                file.write("</PntList3D>\n")
                file.write("          </Breakline>\n")
                bm.free()
            file.write("        </Breaklines>\n")
            file.write("      </SourceData>\n") 
            file.write("    </Surface>\n")
        file.write("  </Surfaces>\n")

        if listPointsObj:
            file.write("  <CgPoints>\n")

            for obj in listPointsObj:
                meshObjektu = obj.data
                bm = bmesh.new()   # create an empty BMesh
                bm.from_mesh(meshObjektu)   # fill it in from a Mesh
                for vert in bm.verts:
                    file.write("    <CgPoint name=\"" + str(vert.index) + "\" code=\"\">")
                    xSour = (vert.co[1]+pripocetY)*znamenko
                    file.write(str("{:.3f}".format(xSour)) + " ")
                    ySour = (vert.co[0]+pripocetX)*znamenko
                    file.write(str("{:.3f}".format(ySour)) + " ")
                    zSour = vert.co[2]+pripocetZ
                    file.write(str("{:.3f}".format(zSour)) + " ")
                    file.write("</CgPoint>\n")

            file.write("  </CgPoints>\n")

        file.write("</LandXML>\n")

zapisXml()