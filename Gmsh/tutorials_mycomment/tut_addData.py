"""
gmshでnodeとelementに物理量を設定し、mshファイルに保存する。
"""
import gmsh

"""
まずはメッシュの作成。tut1と同じものを作る。
"""
gmsh.initialize()
gmsh.model.add("tut_addData")
gmsh.model.geo.addPoint(0, 0, 0, 0.01, 1)
gmsh.model.geo.addPoint(.1, 0, 0, 0.01, 2)
gmsh.model.geo.addPoint(.1, .3, 0, 0.01, 3)
gmsh.model.geo.addPoint(0, .3, 0, 0.01, 4)
gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(3, 2, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)
gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)
gmsh.model.geo.addPlaneSurface([1], 1)
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)
gmsh.option.setNumber("Mesh.MshFileVersion", 2)
gmsh.write("tut_addData_mesh.msh") #物理量とは関係なしにメッシュを保存



"""
物理量の設定にnode tag、element tagの情報が必要。
"""
nodes, *_ = gmsh.model.mesh.getNodes() #nodes -> <np:int:(num_node, )> node tagのリスト
#2次元のelement(今回の場合3node三角形)のtagを取得
_, elements, __ = gmsh.model.mesh.getElements(2)
elements = elements[0]

"""
viewモデルの作成。mshファイルに書き込みたい物理量の数だけ作る。引数には物理量を認識できる名前を設定。
"""
t1 = gmsh.view.add("pressure")
t2 = gmsh.view.add("velocity")
# #addModelDataの使い方はdocs参照。
gmsh.view.addModelData(t1, 1, "tut_addData", "NodeData", nodes, [[i*1.] for i in range(len(nodes))], time = 100.)
gmsh.view.addModelData(t2, 1, "tut_addData", "ElementData", elements, [[i*1., i*2., i*3.] for i in range(len(elements))], time = 100.)

# 各モデルをmshファイルに書き込み。PostProcessing.SaveMeshを0に設定すると、tut_addData_pressure.mshなどには物理量と補間方法の情報しか含まれなくなる。
# これは、ensight goldのgeoファイルと物理量ファイルの分離と同様。
gmsh.option.setNumber("PostProcessing.SaveMesh", 0.)
gmsh.view.write(t1, "tut_addData_pressure.msh")
gmsh.view.write(t2, "tut_addData_velocity.msh")


gmsh.finalize()