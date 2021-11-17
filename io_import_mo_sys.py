bl_info = {
    "name": "Import mo-sys camera data (.txt)",
    "author": "SnowCat",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "File > Import > Import mo-sys camera data",
    "category": "Import-Export",
}

import bpy

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

from math import radians

def floatLocation(value):
    return float(value)/10

def floatEuler(value):
    return radians(float(value))

def import_mo_sys_camera(context, filepath):
    print("Open camera data...")
    f = open(filepath, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()

    camera_data = bpy.data.cameras.new(name='Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)
    camera_object.rotation_mode = 'XYZ'
    bpy.context.scene.collection.objects.link(camera_object)
    
    # would normally load the data here
    frameNumber = 1
    frames = {}
    
    for line in lines:
        line = [i.strip() for i in line.split('\t')]
        time, x, z, y, rx, ry, rz = line[:7]
        
        if time in frames: continue
        frames[time] = True        

        camera_object.location.x = floatLocation(x)
        camera_object.location.y = floatLocation(y)
        camera_object.location.z = floatLocation(z)
        
        camera_object.rotation_euler[0] = floatEuler(rx)+radians(90)
        camera_object.rotation_euler[1] = floatEuler(ry)
        camera_object.rotation_euler[2] = floatEuler(rz)
        
        camera_object.keyframe_insert(data_path="location", frame=frameNumber)
        camera_object.keyframe_insert(data_path="rotation_euler", frame=frameNumber)
        frameNumber += 1     

    camera_object.select_set(True)    
    bpy.context.view_layer.objects.active = objectToSelect = camera_object
    
    return {'FINISHED'}

class ImportMoSysCameraData(Operator, ImportHelper):
    """Import camera dtat from mo-sys file format"""
    bl_idname = "import_mo_sys.camera"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import mo-sys camera data"

    # ImportHelper mixin class uses this
    filename_ext = ".txt"

    filter_glob: StringProperty(
        default="*.txt",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return import_mo_sys_camera(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportMoSysCameraData.bl_idname, text=bl_info["name"])


def register():
    bpy.utils.register_class(ImportMoSysCameraData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportMoSysCameraData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.import_mo_sys.camera('INVOKE_DEFAULT')
