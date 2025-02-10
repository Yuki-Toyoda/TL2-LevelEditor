import bpy

from .stretch_vertex import MYADDON_OT_stretch_vertex
from .level_editor import MYADDON_OT_export_scene

# トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    # Blenderがクラスを識別するための固有の文字列
    bl_idName = "TOPBAR_MT_my_menu"
    # メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    # 著者表示用文字列
    bl_description = "拡張メニュー by Yuki Toyoda"

    # サブメニューの描画
    def draw(self, context):
        # トップバーのメニューに項目を追加する
        self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')


        # トップバーのエディターメニューに項目を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text=MYADDON_OT_stretch_vertex.bl_label)


        # トップバーのエディターメニューに項目を追加
        self.layout.operator(MYADDON_OT_export_scene.bl_idname, text=MYADDON_OT_export_scene.bl_label)

    def subMenu(self, context):
        # ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idName)