import bpy
import json

# Load measured dimensions from a file
with open('ukuran_benda.json', 'r') as f:
    dimensi_terukur = json.load(f)

# Retrieve the measured dimensions
x = dimensi_terukur['width']
y = dimensi_terukur['length']
z = dimensi_terukur['height']

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create the box
bpy.ops.mesh.primitive_cube_add(size=1.0)
box = bpy.context.active_object

# Set the dimensions
box.scale = (x / 2.0, y / 2.0, z / 2.0)

# Apply the scaling
bpy.ops.object.transform_apply(scale=True)

# Add a bevel modifier to round the corners
bevel_modifier = box.modifiers.new(name="Bevel", type='BEVEL')
bevel_modifier.width = 0.1  # Adjust the width of the bevel as needed
bevel_modifier.segments = 10  # Increase the number of segments for a smoother bevel

# Optionally, name the object
box.name = "MeasuredBox"

# Add a new material with a specific color
material = bpy.data.materials.new(name="BoxMaterial")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.1, 0.6, 0.8, 1.0)  # Set to a light blue color

# Load the logo image
logo_path = 'logo.jpeg'  # Update this path to your logo image file
logo_image = bpy.data.images.load(logo_path)

# Create an image texture node
texture_node = material.node_tree.nodes.new('ShaderNodeTexImage')
texture_node.image = logo_image

# Connect the image texture to the base color of the Principled BSDF
material.node_tree.links.new(bsdf.inputs['Base Color'], texture_node.outputs['Color'])

# Assign the material to the box
if box.data.materials:
    box.data.materials[0] = material
else:
    box.data.materials.append(material)

# Ensure UV mapping is applied to the box
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.smart_project()
bpy.ops.object.mode_set(mode='OBJECT')

# Add a plane for the floor
bpy.ops.mesh.primitive_plane_add(size=10)
floor = bpy.context.active_object
floor.location.z = -z / 2.0

# Add a new material to the floor
floor_material = bpy.data.materials.new(name="FloorMaterial")
floor_material.use_nodes = True
floor_bsdf = floor_material.node_tree.nodes["Principled BSDF"]
floor_bsdf.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1.0)  # Set to a neutral grey color
floor.data.materials.append(floor_material)

# Add lighting
bpy.ops.object.light_add(type='SUN', radius=1)
sun = bpy.context.active_object
sun.location = (5, -5, 10)
sun.data.energy = 3

# Add a camera
bpy.ops.object.camera_add()
camera = bpy.context.active_object
camera.location = (7, -7, 5)
camera.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = camera

# Print details of the created box
print("Created box with dimensions:", box.dimensions)
print("Box location:", box.location)

# Set the render settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 100

# Set the background color
bpy.context.scene.world.node_tree.nodes["Background"].inputs['Color'].default_value = (1, 1, 1, 1)

# Set the output settings
bpy.context.scene.render.filepath = '/tmp/render.png'
bpy.ops.render.render(write_still=True)
