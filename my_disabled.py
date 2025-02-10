import bpy

class MYADDON_OT_add_disabled(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_disabled"
    bl_label = "disabled 追加"
    bl_description = "['disabled']有効、無効オプションの追加"
    # redo, undo 可能オプション
    bl_optioms = {'REGISTER', 'Undo'}

    def execute(self, context):
        # 無効オプションの追加
        context["disabled"] = True
        
        # オペレーターの命令終了
        return {'FINISHED'}

class OBJECT_PT_disabled(bpy.types.Panel):
    bl_idname = "OBJECT_PT_disabled"
    bl_label = "Disabled"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    # サブメニューの描画
    def draw(self, context):
        # パネルに項目追加
        if "disabled" in context.object:
            # 既にプロパティがある場合プロパティを表示
            self.layout.prop(context.object, '["disabled"]', text=self.bl_label)
        else:
            # プロパティがなければプロパティの追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_disabled.bl_idname)