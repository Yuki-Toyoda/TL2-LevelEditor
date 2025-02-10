import bpy
import bpy_extras
import math
import json

# シーン出力オペレーター
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をエクスポートします"
    # 出力するファイル拡張子を設定
    filename_ext = ".json"


    # ファイルに文字列を書き込む関数
    def write_and_print(self, file, str):
        # 文字列出力
        print(str)


        # ファイルに書きこむ
        file.write(str)
        file.write('\n')


    def parse_scene_recursive(self, file, object, level):
        """"シーン解析用再帰関数"""


        # 深さ分インデントする(タブを挿入)
        indent = ''
        for i in range(level):
            indent += "\t"


        # オブジェクト名書き込み
        self.write_and_print(file, indent + object.type)
       
        # ローカルトランスフォーム行列から平行移動、回転、拡縮を取得
        trans, rot, scale = object.matrix_local.decompose()
        # 回転をクォータニオンからオイラーに変換
        rot = rot.to_euler()
        # ラジアンから度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
       
        # トランスフォーム情報を表示
        self.write_and_print(file, indent + "T %f, %f, %f" % (trans.x, trans.y, trans.z))
        self.write_and_print(file, indent + "R %f, %f, %f" % (rot.x, rot.y, rot.z))
        self.write_and_print(file, indent + "S %f, %f, %f" % (scale.x, scale.y, scale.z))


        # カスタムプロパティ 'file_name'
        if "file_name" in object:
            self.write_and_print(file, indent + "N %s" % object["file_name"])


        # カスタムプロパティ 'collider'
        if "collider" in object:
            self.write_and_print(file, indent + "C %s" % object["collider"])
            temp_str = indent + "CC %f %f %f"
            temp_str %= (object["collider_center"][0],object["collider_center"][1],object["collider_center"][2])
            self.write_and_print(file, temp_str)
            temp_str = indent + "CS %f %f %f"
            temp_str %= (object["collider_size"][0],object["collider_size"][1],object["collider_size"][2])
            self.write_and_print(file, temp_str)
       
        self.write_and_print(file, indent + 'END')
        self.write_and_print(file, '')


        # 子ノードへ進む
        for child in object.children:
            self.parse_scene_recursive(file, child, level + 1)


    def parse_scene_recursive_json(self, data_parent, object, level):
        # シーンのオブジェクト一個分のjsonオブジェクト生成
        json_object = dict()
        # オブジェクト種類
        json_object["type"] = object.type
        # オブジェクト名
        json_object["name"] = object.name


        # ローカルトランスフォーム行列から平行移動、回転、拡縮を取得
        trans, rot, scale = object.matrix_local.decompose()
        # 回転をクォータニオンからオイラーに変換
        rot = rot.to_euler()
        # ラジアンから度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        # トランスフォーム情報をディクショナリーに登録
        transform = dict()
        transform["translation"] = (trans.x, trans.y, trans.z)
        transform["rotation"]    = (rot.x, rot.y, rot.z)
        transform["scaling"]     = (scale.x, scale.y, scale.z)
        # まとめて一個分のjsonオブジェクトに登録
        json_object["transform"] = transform


        # カスタムプロパティ 'file_name'
        if "file_name" in object:
            json_object["file_name"] = object["file_name"]


        # カスタムプロパティ 'collider'
        if "collider" in object:
            collider = dict()
            collider["type"]          = object["collider"]
            collider["center"]        = object["collider_center"].to_list()
            collider["size"]          = object["collider_size"].to_list()
            json_object["collider"]   = collider


        # 一個分jsonオブジェクトを親オブジェクトに登録
        data_parent.append(json_object)


        if len(object.children) > 0:
            # 子ノードリストを生成
            json_object["children"] = list()


            # 子ノードへ進む
            for child in object.children:
                self.parse_scene_recursive_json(json_object["children"], child, level + 1)


    def export(self):
        """"ファイルに出力"""


        print("シーン情報出力開始... %r % self.filepath")


        # ファイルをテキスト形式で書き出し用にオープン
        # スコープを抜けると自動でクローズされる
        with open(self.filepath, "wt") as file:
            # ファイルに文字を書き込む
            file.write("SCENE\n")
            # シーン内の全オブジェクトの名前を出力する
            for object in bpy.context.scene.objects:
                # 親オブジェクトがあるものはスキップ
                if(object.parent):
                    continue


                # シーン直下のオブジェクトをルートノード(深さ0)とし、再帰関数で捜査
                self.parse_scene_recursive(file, object, 0)


    def export_json(self):
        """"JSON形式でファイルに出力"""


        # 保存する情報をまとめるdict
        json_object_root = dict()


        # ノード名
        json_object_root["name"] = "scene"
        # オブジェクトリストを作成
        json_object_root["objects"] = list()


        for object in bpy.context.scene.objects:
            # 親オブジェクトがあるものはスキップ
            if(object.parent):
                continue


            # シーン直下のオブジェクトをルートノード（深さ０）とし、再帰関数で操作
            self.parse_scene_recursive_json(json_object_root["objects"], object, 0)


        # オブジェクトをJSON文字列にエンコード
        json_text = json.dumps(json_object_root, ensure_ascii=False, cls=json.JSONEncoder, indent=4)
        # コンソールに表示する
        print(json_text)


        # ファイルをテキスト形式で書き出し用にオープン
        # スコープを抜けると自動的にクローズされる
        with open(self.filepath, "wt", encoding="utf-8") as file:
            # ファイルに文字列を書き込む
            file.write(json_text)


    def execute(self, context):
        print ("シーン情報をエクスポートします")


        self.export_json()


        print("シーン情報をエクスポートしました")
        self.report({'INFO'}, "シーン情報をエクスポートしました")


        return {'FINISHED'}
   