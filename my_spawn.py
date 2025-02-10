import bpy
import os
import bpy.ops

class MYADDON_OT_add_spawn_symbole(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_spawn_symbole"
    bl_label = "スポーンポイントシンボル 追加"
    bl_description = "スポーンポイントシンボル追加"

    prototype_object_name = "PrototypePlayerSpawn"
    object_name = "PlayerSpawn"

    def execute(self, context):
        print("出現ポイントのシンボルをImportします")

        spawn_object = bpy.data.objects.get(MYADDON_OT_add_spawn_symbole.prototype_object_name)
        if spawn_object is not None:
            return {'CANCELLED'}

        addon_directory = os.path.dirname(__file__)
        relative_path = "Player/Player.gltf"
        
        full_path = os.path.join(addon_directory, relative_path)

        bpy.ops.wm.obj_import('EXEC_DEAFAULT', 
                              filepath = full_path, 
                              display_type='THUMBNAIL',
                              forward_axis = 'Z', up_axis = 'Y')
        
        bpy.ops.object.transform_apply(location = False,
                                       rotation = True,
                                       scale = False,
                                       properties = False,
                                       isolate_users = False)

        object = bpy.context.active_object
        object = MYADDON_OT_add_spawn_symbole.prototype_object_name

        object["type"] = MYADDON_OT_add_spawn_symbole.object_name

        bpy.context.collection.objects.unlink(object)

        # オペレーターの命令終了
        return {'FINISHED'}

class MYADDON_OT_add_spawn(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_spawn"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを作成します"
    # redo, undo 可能オプション
    bl_optioms = {'REGISTER', 'Undo'}

    def execute(self, context):
        spawn_object = bpy.data.objects.get(MYADDON_OT_add_spawn_symbole.prototype_object_name)

        if spawn_object is None:
            bpy.ops.myaddon.myaddon_ot_add_spawn('EXEC_DEFAULT')
            spawn_object = bpy.data.objects.get(MYADDON_OT_add_spawn_symbole.prototype_object_name)

        print("出現ポイントのシンボルを作成します")

        bpy.ops.object.select_all(action='DESELECT')

        object = spawn_object.copy()

        bpy.context.collection.objects.link(object)

        object.name = MYADDON_OT_add_spawn.object_name

        # オペレーターの命令終了
        return {'FINISHED'}