import bpy
import mathutils
import bmesh


#doplnit textovy popis - nazvy bodu - vlastni collection

print('spoustim landXml import')

def main():
    
    #print(3 % 3)
    #return
    
    arrayX = []
    arrayY = []
    arrayZ = []
    slova = []
    indexy = []

    #        <Pnts>
    #"\t\t\t\t<Pnts>\n" \t jsou 2 mezery
    #jdu radek po radku, az najdu radek <Pnts> (zrejme odstranuju mezery a TAB - zatim dam 
    with open("UniControl/Cyklostezka prelozka vytlaku.xml", "r") as file:
        boolPoints = False
        boolFaces = False
        for line in file:
            if boolPoints == True:
                boolSouradnice = False
                slovo = ''
                for char in line:
                    if boolSouradnice == True:
                        if char != ' ' and char != '<':
                            slovo = slovo + char
                        if char == ' ' or char == '<':
                            slova.append(slovo)
                            slovo = ''
                        if char == '<':
                            boolSouradnice = False
                    if char == '>':
                        boolSouradnice = True
                        
            if boolFaces == True:
                boolIndexy = False
                index = ''
                for char in line:
                    if boolIndexy == True:
                        if char != ' ' and char != '<':
                            index = index + char
                        if char == ' ' or char == '<':
                            indexy.append(index)
                            index = ''
                        if char == '<':
                            boolIndexy = False
                    if char == '>':
                        boolIndexy = True
            
                        
            if line.replace("\t", "") == "<Pnts>\n":
                boolPoints = True
            if line.replace(" ", "") == "<Pnts>\n":
                boolPoints = True
            if line.replace("\t", "") == "</Pnts>\n":
                boolPoints = False
            if line.replace(" ", "") == "</Pnts>\n":
                boolPoints = False
            if line.replace("\t", "") == "<Faces>\n":
                boolFaces = True
            if line.replace(" ", "") == "<Faces>\n":
                boolFaces = True
            if line.replace("\t", "") == "</Faces>\n":
                boolFaces = False
            if line.replace(" ", "") == "</Faces>\n":
                boolFaces = False
                
        #mame slova najebana ve slova[] x, y, z
        counter = 0
        for slovo in slova:
            if counter % 3 == 0:
                arrayX.append(float(slovo))
            if counter % 3 == 1:
                arrayY.append(float(slovo))
            if counter % 3 == 2:
                arrayZ.append(float(slovo))
            counter = counter + 1
        
    bpy.ops.mesh.primitive_plane_add()
    objectMesh = bpy.context.active_object.data
    bFA=bmesh.new() 
    odecetX=782700.0 # X je vzdy to mensi cislo
    odecetY=1197500.0
    odecetZ=720.0

    indA = 0
    for xVal in arrayX: #prohozene, protoze landXML ma prvni Y souradnice
        #vector = (xVal-odecetX, arrayY[indA]-odecetY, arrayZ[indA]-odecetZ)
        vector = (arrayY[indA]-odecetX, xVal-odecetY, arrayZ[indA]-odecetZ)
        bFA.verts.new(vector)
        indA = indA + 1
    
    bFA.verts.ensure_lookup_table()

    listVert = []
    counter2 = 0
    for index in indexy:
        listVert.append(bFA.verts[int(index)-1])
        if counter2 % 3 == 2:
            bFA.faces.new(listVert)
            listVert.clear()
        counter2 = counter2 + 1
            
    bFA.to_mesh(objectMesh)
    bFA.free()

main()