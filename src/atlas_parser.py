from PIL import Image
import os

atlas_folder = r"C:\NonSYSFile\Gam\Mod\DarkestDungeon\ResolutionProject\atlas\anim"
png_folder = r"C:\NonSYSFile\Gam\Mod\DarkestDungeon\ResolutionProject\anim"
output_folder = r"C:\NonSYSFile\Gam\Mod\DarkestDungeon\ResolutionProject\output"

def process_atlas(atlas_path: str, png_folder: str, output_folder: str) -> None:
    """
    Process a single atlas file and its corresponding PNG.
    Parses the atlas file, calculates scale factor, resizes the PNG,
    and outputs both scaled files to the output folder.
    
    Args:
        atlas_path: Full path to the .atlas file
        png_folder: Folder containing the source PNG file
        output_folder: Folder where output files will be saved
    """
    with open(atlas_path) as f:
        atlas_name = os.path.basename(atlas_path)
        # Target size of PNG that fixes the aliasing
        TARGET_SIZE = 650
        # List of each line in the atlas file
        lines = f.readlines()
        # List of all sprites from one atlas file
        sprites = []
        # The name of the related PNG file
        png_file = lines[1].strip()
        # The width and height of the sprite sheet
        width, height = lines[2].split(":")[1].strip().split(",")
        sheet_width = int(width)
        sheet_height = int(height)
        # The width and height of the whole sprite sheet
        sprite_sheet = {"sheet_width": sheet_width, "sheet_height": sheet_height}

        if sheet_width > sheet_height:
            scale = TARGET_SIZE / sheet_width
        else:
            scale = TARGET_SIZE / sheet_height

        # line.startswith(" ") to check for leading space
        # ":" in line to check if a line contains a colon
        # "." in line to check if a line contains a period
        for index in range(len(lines)):
            if lines[index].strip() == "":
                continue 
            elif not lines[index].startswith(" "):
                if "." not in lines[index] and ":" not in lines[index]:
                    if index + 3 > len(lines):
                        break
                    else:
                        rotate = lines[index + 1].split(":")[1].strip()
                        x, y = lines[index + 2].split(":")[1].strip().split(", ")
                        width, height = lines[index + 3].split(":")[1].strip().split(", ")
                        sprite = {}
                        sprite["name"] = lines[index].strip()
                        sprite["rotate"] = rotate
                        sprite["x"] = int(x)
                        sprite["y"] = int(y)
                        sprite["width"] = int(width)
                        sprite["height"] = int(height)
                        sprites.append(sprite)

        for index in range(len(sprites)):
            sprite = sprites[index]
            for key in ["x", "y", "width", "height"]:
                sprite[key] = round(sprite[key] * scale)

        sprite_sheet["sheet_width"] = sheet_width * scale
        sprite_sheet["sheet_height"] = sheet_height * scale

    # Dynamic input and output paths
    png_input_path = os.path.join(png_folder, png_file)
    output_file_path = os.path.join(output_folder, png_file)
    output_atlas_path = os.path.join(output_folder, atlas_name)

    # Atlas file header format:
    # (empty line)
    # crusader.sprite.idle.png
    # size: 800,800
    # format: RGBA8888
    # filter: Linear,Linear
    # repeat: none
    with open(output_atlas_path, "w") as f:
        f.write("\n")
        f.write(f"{png_file}\n")
        f.write(f"size: {round(sprite_sheet['sheet_width'])},{round(sprite_sheet['sheet_height'])}\n")
        f.write("format: RGBA8888\n")
        f.write("filter: Linear,Linear\n")
        f.write("repeat: none\n")

        # Sprite entry format:
        # sprite name
        #   rotate: false
        #   xy: 2, 27
        #   size: 28, 56
        #   orig: 28, 56
        #   offset: 0, 0
        #   index: -1
        for sprite in sprites:
            f.write(f"{sprite['name']}\n")
            f.write(f"  rotate: {sprite['rotate']}\n")
            f.write(f"  xy: {sprite['x']}, {sprite['y']}\n")
            f.write(f"  size: {sprite['width']},{sprite['height']}\n")
            f.write(f"  orig: {sprite['width']},{sprite['height']}\n")
            f.write("  offset: 0, 0\n")
            f.write("  index: -1\n")

    # Resize the PNG
    img = Image.open(png_input_path)
    new_img = img.resize((round(sprite_sheet['sheet_width']), round(sprite_sheet['sheet_height'])))
    new_img.save(output_file_path)

def process_mod(atlas_folder: str, png_folder: str, output_folder: str) -> None:
    """
    Process all atlas files that are needed to fix.
    Walk through all of the atlas files in the provided folder,
    Parse only required atlas file through calling process_atlas.

    Args:
        atlas_folder: Folder that stores all atlas files.
        png_folder: Folder containing the source PNG files.
        output_folder: Folder where output files will be saved.
    """
    target_suffixes = [".sprite.combat.atlas", ".sprite.walk.atlas", ".sprite.idle.atlas"]
    files = os.listdir(atlas_folder)
    
    for f in files:
        if any(f.endswith(suffix) for suffix in target_suffixes):
            atlas_path = os.path.join(atlas_folder, f)
            process_atlas(atlas_path, png_folder, output_folder)

process_mod(atlas_folder)