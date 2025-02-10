import bpy
import os
import bpy.ops

class spawnNames():
    #インデックス
    PROTOTYPE = 0
    INSTANCE = 1
    FILENAME = 2

    names = {}
    names["Enemy"] = ("PrototypeEnemySpawn", "EnemySpawn", "Enemy/Enemy.gltf")
    names["Player"] = ("PrototypePlayerSpawn", "PlayerSpawn", "Player/Player.gltf")

class MYADDON_OT_add_spawn_symbole(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_spawn_symbole"
    bl_label = "スポーンポイントシンボル 追加"
    bl_description = "スポーンポイントシンボル追加"
    
    def load_obj(self, type):
        spawn_object = bpy.data.objects.get(spawnNames.names[type][spawnNames.PROTOTYPE])
        if spawn_object is not None:
            return {'CANCELLED'}

        addon_directory = os.path.dirname(__file__)
        relative_path = spawnNames.names[type][spawnNames.FILENAME]
        
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
        object.name = spawnNames.names[type][spawnNames.PROTOTYPE]

        object["type"] = spawnNames.names[type][spawnNames.INSTANCE]

        bpy.context.collection.objects.unlink(object)

        # オペレーターの命令終了
        return {'FINISHED'}



    def execute(self, context):
        self.load_obj("Enemy")
        self.load_obj("Player")

        # オペレーターの命令終了
        return {'FINISHED'}

class MYADDON_OT_add_spawn(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_spawn"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを作成します"
    # redo, undo 可能オプション
    bl_optioms = {'REGISTER', 'Undo'}

    type: bpy.props.StringProperty(name="Type", default = "Player")

    def execute(self, context):
        spawn_object = bpy.data.objects.get(spawnNames.names[self.type][spawnNames.PROTOTYPE])

        if spawn_object is None:
            bpy.ops.myaddon.myaddon_ot_add_spawn('EXEC_DEFAULT')
            spawn_object = bpy.data.objects.get(spawnNames.names[self.type][spawnNames.PROTOTYPE])

        print("出現ポイントのシンボルを作成します")

        bpy.ops.object.select_all(action='DESELECT')

        object = spawn_object.copy()

        bpy.context.collection.objects.link(object)

        object.name = MYADDON_OT_add_spawn.object_name

        # オペレーターの命令終了
        return {'FINISHED'}

class MYADDON_OT_add_player_spawn(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_player_spawn"
    bl_label = "プレイヤーの出現ポイントシンボルの作成"
    bl_description = "プレイヤーの出現ポイントのシンボルを作成します"

    def execute(self, context):
        
        bpy.ops.myaddon.myaddon_ot_add_spawn('EXEC_DEFAULT', type = "Player")

        # オペレーターの命令終了
        return {'FINISHED'}
    
class MYADDON_OT_add_enemy_spawn(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_enemy_spawn"
    bl_label = "敵の出現ポイントシンボルの作成"
    bl_description = "敵の出現ポイントのシンボルを作成します"

    def execute(self, context):
        
        bpy.ops.myaddon.myaddon_ot_add_spawn('EXEC_DEFAULT', type = "Enemy")

        # オペレーターの命令終了
        return {'FINISHED'}
    