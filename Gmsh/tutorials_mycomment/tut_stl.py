"""
gmshでstlのサーフェスメッシュを切りなおす。
"""
import gmsh
import math

gmsh.initialize()
gmsh.clear() #オリジナルのtutに従いclear
gmsh.merge("mixing_elbow.stl") #stlをマージ

angle = 40. #ほぼ触らないパラメータ
forceParametrizablePatches = 0 #ほぼ触らないパラメータ
curveAngle = 180 #ほぼ触らないパラメータ
includeBoundary = True #ほぼ触らないパラメータ
gmsh.model.mesh.classifySurfaces(angle * math.pi / 180., includeBoundary, forceParametrizablePatches, curveAngle * math.pi / 180.)
gmsh.model.mesh.createGeometry() #classifySurfacesを事前に実行しない場合、エラーになった。
gmsh.model.geo.synchronize()

# physical valueを定義。
# stlと同じくin1 ~ sideの名前を使う。fluidの名前は任意。in1 ~ sideの名前の順番はstlでの定義の順番に従う。
gmsh.model.addPhysicalGroup(2, [1], name = "in1")
gmsh.model.addPhysicalGroup(2, [2], name = "in2")
gmsh.model.addPhysicalGroup(2, [3], name = "out")
gmsh.model.addPhysicalGroup(2, [4], name = "side")
# gmsh.model.addPhysicalGroup(3, [1], name = "fluid")

f = gmsh.model.mesh.field.add("MathEval")
gmsh.model.mesh.field.setString(f, "F", "0.005") #3番目の引数を小さくするとメッシュ数も増える。
gmsh.model.mesh.field.setAsBackgroundMesh(f)

gmsh.model.mesh.generate(2)
gmsh.option.setNumber("Mesh.MshFileVersion", 2)
gmsh.write('test.stl')

gmsh.finalize()