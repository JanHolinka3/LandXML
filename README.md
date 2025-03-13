script for Blender to run from text editor and create landxml file from active collection objects

directly in code is mandatory to specify: projectName, fileName, pripocetX, pripocetY, pripocetZ, positiveNegative

pripocetX, pripocetY, pripocetZ are for world coords (you have to solve that for your self for your local coord system). Im using this script to create models for UniControl Machine Control

positiveNegative should be 1 for positive coords and -1 for negative coords

from active collection loop all objects: 3 type objects: with faces (tris only), with only egdes, with only verts

create TIN surface from face objects 

create breakLines from edges - you need 1 object for every continuus line - named by object name - order is solved by algorymt (Blender can have edges in any order)

create CgPoints from vert type object - you need only one such object, name by vert index

control checks and UI (simply conversion to extension/addon) will maybe added in future, unexpected results and behavior will most probably occur if you dont follow the rules
