import bpy

# 頂点を伸ばすオペレーター
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_strech_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    # redo, undo 可能オプション
    bl_optioms = {'REGISTER', 'Undo'}

    # メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました")


        # オペレーターの命令終了を通知
        return {'FINISHED'}

