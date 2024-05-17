import gmsh

#####おまじない的存在。必ず初めにcallする。
gmsh.initialize()

#####モデルの追加。引数はモデル名で任意。
gmsh.model.add("tut1")

lc = 1e-2
"""
Pointの定義。
    input : (x, y, z, mesh size, tag)
        x, y, z -> <float> 座標点
        mesh size -> <float; optional> メッシュサイズ
        tag -> <int; optional> タグの値。
Note:
    tagを指定しない場合、よしなにタグ値を決めてくれる。付与されたタグはoutputとして返される。
"""
gmsh.model.geo.addPoint(0, 0, 0, lc, 1) #タグを指定する場合
#tag_point = gmsh.model.geo.addPoint(0, 0, 0, lc) #指定しない場合。
gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(.1, .3, 0, lc, 3)
gmsh.model.geo.addPoint(0, .3, 0, lc, 4)

"""
Lineの定義
    input: (p1, p2, tag)
        p1 -> <int> 開始点のPointのタグ
        p2 -> <int> 終了点のPointのタグ
        tag -> <int; optional> タグ
"""
gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(3, 2, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)

"""
Surface定義の前にCurve Loopが必要。
    Input: ((p1, p2, ...), tag)
        (p1, p2, ...) -> <list of int> Curve Loopを構成するLineの順序付き集合。閉曲線になるように順序付けされている。負値のpiはLine(pi)と逆向きのラインを意味する。
"""
gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)

"""
Surface定義
    Input: ((cl1), tag)
        (cl1) -> <list of int> Curve Loopのタグの集合。閉じた面の場合、要素数は1。
"""
gmsh.model.geo.addPlaneSurface([1], 1)

#####メッシュ作成前に同期処理が必要。
gmsh.model.geo.synchronize()

"""
Physical Groupの追加
    Input:  (dim, (t1, t2, ...), name)
        dim -> <int> dimension
        (t1, t2, ...) -> <list of int> list of tags
        name -> <str> physical name
"""
gmsh.model.addPhysicalGroup(1, [1, 2, 3, 4], name = "My Line")
gmsh.model.addPhysicalGroup(2, [1], name="My surface")

##### 2Dメッシュの作成
gmsh.model.mesh.generate(2)
##### mshファイルフォーマットのバージョン指定。
gmsh.option.setNumber("Mesh.MshFileVersion", 2) #version2のASCIIフォーマットで書かれる。
##### msh作成
gmsh.write("tut1.msh")

#####おまじない的な処理
gmsh.finalize()