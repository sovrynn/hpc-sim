import bpy
me=bpy.data.meshes.new("t")
me.from_pydata([(0,0,0),(1,0,0),(0,1,0)], [], [(0,1,2)])
obj=bpy.data.objects.new("t", me)
bpy.context.collection.objects.link(obj)