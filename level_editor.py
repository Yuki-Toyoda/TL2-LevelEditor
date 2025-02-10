import bpy
import bpy_extras
import math
import gpu
import gpu_extras.batch
import copy
import mathutils
import json


# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Yuki Toyoda",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# 頂点を伸ばすオペレーターのインポート
from .stretch_vertex import MYADDON_OT_stretch_vertex

# ICO球生成オペレーター
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    # redo, undo 可能オプション
    bl_optioms = {'REGISTER', 'Undo'}


    # メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")


        # オペレーターの命令終了を通知
        return {'FINISHED'}

from .level_editor import MYADDON_OT_export_scene

# カスタムプロパティ追加オペレータ
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_filename"
    bl_label = "FileName 追加"
    bl_description = "['file_name']カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}


    def execute(self, context):
        #['file_name']カスタムプロパティを追加
        context.object["file_name"] = ""


        return {"FINISHED"}
   
# コライダー追加
class MYADDON_OT_add_collider(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_collider"
    bl_label = "コライダー追加"
    bl_description = "['collider']カスタムプロパティを追加します"
    # redo, undo 可能オプション
    bl_optioms = {'REGISTER', 'Undo'}


    def execute(self, context):
        #['collider']カスタムプロパティを追加
        context.object["collider"] = "BOX"
        context.object["collider_center"] = mathutils.Vector((0, 0, 0))
        context.object["collider_size"] = mathutils.Vector((2, 2, 2))


        return {"FINISHED"}


class OBJECT_PT_file_name(bpy.types.Panel):
    """オブジェクトのファイルネームパネル"""
    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"


    # サブメニューの描画
    def draw(self, context):
        # パネルに項目追加
        if "file_name" in context.object:
            # 既にプロパティがある場合プロパティを表示
            self.layout.prop(context.object, '["file_name"]', text=self.bl_label)
        else:
            # プロパティがなければプロパティの追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)


# パネル コライダー
class OBJECT_PT_collider(bpy.types.Panel):
    """オブジェクトのコライダーパネル"""
    bl_idname = "OBJECT_PT_collider"
    bl_label = "Collider"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"


    # サブメニューの描画
    def draw(self, context):
        # パネルに項目追加
        if "collider" in context.object:
            # 既にプロパティがある場合プロパティを表示
            self.layout.prop(context.object, '["collider"]', text="Type")
            self.layout.prop(context.object, '["collider_center"]', text="Center")
            self.layout.prop(context.object, '["collider_size"]', text="Size")
        else:
            # プロパティがなければプロパティの追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_collider.bl_idname)


# トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    # Blenderがクラスを識別するための固有の文字列
    bl_idName = "TOPBAR_MT_my_menu"
    # メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    # 著者表示用文字列
    bl_description = "拡張メニュー by " + bl_info["author"]


    # サブメニューの描画
    def draw(self, context):
        # トップバーのメニューに項目を追加する
        self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')


        # トップバーのエディターメニューに項目を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text=MYADDON_OT_stretch_vertex.bl_label)


        # トップバーのエディターメニューに項目を追加
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname, text=MYADDON_OT_create_ico_sphere.bl_label)


        # トップバーのエディターメニューに項目を追加
        self.layout.operator(MYADDON_OT_export_scene.bl_idname, text=MYADDON_OT_export_scene.bl_label)

    def subMenu(self, context):
        # ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idName)


classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
)


# コライダー描画
class DrawCollider:
    # 描画ハンドル
    handle = None


    # 3Dビューに登録する描画関数
    def draw_Collider():
        # 頂点データ
        vertices = {"pos":[]}
        # インデックスデータ
        indices = []


        # 各頂点のオブジェクト中心からのオフセット
        offsets = [
            [-0.5, -0.5, -0.5], # 左下前
            [+0.5, -0.5, -0.5], # 右下前
            [-0.5, +0.5, -0.5], # 左上前
            [+0.5, +0.5, -0.5], # 右上前
            [-0.5, -0.5, +0.5], # 左下奥
            [+0.5, -0.5, +0.5], # 右下奥
            [-0.5, +0.5, +0.5], # 左上奥
            [+0.5, +0.5, +0.5], # 右上奥
        ]


        # 立方体のX, Y, Z方向サイズ
        size = [2, 2, 2]


        # 現在シーンのオブジェクト全てを走査
        for object in bpy.context.scene.objects:
            # オブジェクトにコライダープロパティがなければ描画をしない
            if not "collider" in object:
                continue
           
            # 中心点とサイズの変数を宣言する
            center = mathutils.Vector((0, 0, 0))
            size = mathutils.Vector((2,2,2))


            # プロパティから値を取得
            center[0] = object["collider_center"][0]
            center[1] = object["collider_center"][1]
            center[2] = object["collider_center"][2]
            size[0] = object["collider_size"][0]
            size[1] = object["collider_size"][1]
            size[2] = object["collider_size"][2]


            # 追加前の頂点数
            start = len(vertices["pos"])


            # BOXの8頂点分回す
            for offset in offsets:
                # オブジェクトの中心座標コピー
                pos = copy.copy(center)
                # 中心点を基準に各頂点ごとにずらす
                pos[0] += offset[0] * size[0]
                pos[1] += offset[1] * size[1]
                pos[2] += offset[2] * size[2]


                # ローカル座標からワールド座標に変換
                pos = object.matrix_world @ pos


                # 頂点データリストに座標追加
                vertices['pos'].append(pos)


            # 前面を構成する辺の頂点インデックス
            indices.append([start + 0, start + 1])
            indices.append([start + 2, start + 3])
            indices.append([start + 0, start + 2])
            indices.append([start + 1, start + 3])
            # 奥面を構成する辺の頂点インデックス
            indices.append([start + 4, start + 5])
            indices.append([start + 6, start + 7])
            indices.append([start + 4, start + 6])
            indices.append([start + 5, start + 7])
            # 前と頂点をつなぐ辺のインデックス
            indices.append([start + 0, start + 4])
            indices.append([start + 1, start + 5])
            indices.append([start + 2, start + 6])
            indices.append([start + 3, start + 7])
               
        # ビルトインのシェーダー取得
        shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")


        # バッチを作成(引数 : シェーダー、トポロジー、頂点データ、インデックスデータ)
        batch = gpu_extras.batch.batch_for_shader(shader, "LINES", vertices, indices = indices)


        # シェーダーのパラメーター設定
        color = [0.5, 1.0, 1.0, 1.0]
        shader.bind()
        shader.uniform_float("color", color)


        # 描画
        batch.draw(shader)


# メニュー項目描画
def draw_menu_manual(self, context):
    #self : 呼び出し元の暮らすインスタンス
    #context : カーソルを合わせた際のポップアップのカスタマイズ等に使用


    # トップバーのメニューに項目を追加する
    self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')


# アドオン有効化時コールバック
def register():
    # Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)


    # 3Dビューに描画関数を追加
    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_Collider, (), "WINDOW", "POST_VIEW")


    # メニューに項目追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.subMenu)
    print("レベルエディタが有効化されました")


# アドオン無効化時コールバック
def unregister():
    # メニューから項目削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.subMenu)
   
    # 3Dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle, "WINDOW")


    # Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)


    print("レベルエディタが無効化されました")
# テスト実行用コード
if __name__ == "__main__":
    register()

