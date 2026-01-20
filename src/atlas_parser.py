from PIL import Image
import os
import numpy as np
import shutil

# mod_folder = r"C:\NonSYSFile\Gam\Mod\DarkestDungeon\ResolutionProject\2979505704"
# mod_folder = r"C:\NonSYSFile\Gam\Mod\DarkestDungeon\ResolutionProject\Profaned Knight NSFW Test"

def find_skin_mod_structure(mod_folder: str) -> dict:
    """
    Analyze a hero reskin mod folder and return its structure.
    
    Args:
        mod_folder: Path to the root of the mod folder
        
    Returns:
        Dictionary containing:
        - atlas_folder: Path to atlas files
        - png_variant_folders: List of paths to PNG variant folders
        - is_type_a: Whether this mod has custom atlas files
    """
    png_variant_folders = []
    atlas_folder = None

    for root, dirs, files in os.walk(mod_folder):
            if 'backup' in dirs:
                dirs.remove('backup')
            elif any(f.endswith('.atlas') for f in files) and os.path.basename(root) == "anim":
                atlas_folder = root
            elif any(f.endswith('_portrait_roster.png') for f in files):
                png_folder = os.path.join(root, "anim")
                png_variant_folders.append(png_folder)

    return {
        "atlas_folder": atlas_folder,
        "png_variant_folders": png_variant_folders,
        "is_type_a": atlas_folder is not None
    }

def process_atlas(atlas_path: str) -> dict:
    """
    Process a single atlas file.
    Parses the atlas file, calculates scale factor,
    and outputs the scaled atlas file to the output folder.
    
    Args:
        atlas_path: Full path to the .atlas file

    Returns:
        Dict that stores the information of an atlas file

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

        print(f"Processing: {atlas_name}")
        print(f"  Original size: {sheet_width} x {sheet_height}")

        larger_dimension = max(sheet_width, sheet_height)

        if larger_dimension <= TARGET_SIZE:
            print(f"Skipping {atlas_name}: resolution already small enough")
            return
        
        scale = TARGET_SIZE / larger_dimension

        print(f"  Scale factor: {scale:.3f}")

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
        sprite_sheet["scale"] = scale
        sprite_sheet["png_file"] = png_file

    # Dynamic input and output paths
    # output_atlas_folder = os.path.join(atlas_path, "anim")
    # os.makedirs(output_atlas_folder, exist_ok=True)
    # output_atlas_path = os.path.join(output_atlas_folder, atlas_name)

    # Atlas file header format:
    # (empty line)
    # crusader.sprite.idle.png
    # size: 800,800
    # format: RGBA8888
    # filter: Linear,Linear
    # repeat: none
    with open(atlas_path, "w") as f:
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

    print(f"  Output size: {round(sprite_sheet['sheet_width'])} x {round(sprite_sheet['sheet_height'])}")
    print(f"  Atlas Saved to: {atlas_path}")

    return sprite_sheet

def resize_png(png_folder: str, sprite_sheet: dict) -> None:
    """
    Process the corresponding PNG of an atlas file.
    Resize the PNG with the sprite sheet info provided by the atlas file.

    Args:
        png_folder: Folder containing the source PNG file
        output_folder: Folder where output files will be saved
        sprite_sheet: Dict that stores the information of an atlas file
    """
    # Dynamic input and output paths
    output_png_path = os.path.join(png_folder, sprite_sheet.get("png_file"))
    
    # Resize PNG
    png_input_path = os.path.join(png_folder, sprite_sheet.get("png_file"))
    img = Image.open(png_input_path).convert('RGBA')
    arr = np.array(img)

    transparent_mask = arr[:, :, 3] < 255
    arr[transparent_mask, 0] = 0  # R
    arr[transparent_mask, 1] = 0  # G
    arr[transparent_mask, 2] = 0  # B

    low_alpha_mask = arr[:, :, 3] < 32
    arr[low_alpha_mask, 3] = 0

    img = Image.fromarray(arr, 'RGBA')

    new_img = img.resize((round(sprite_sheet['sheet_width']), round(sprite_sheet['sheet_height'])))
    new_img.save(output_png_path)

    print(f"  Image Saved to: {output_png_path}")

def create_backup(mod_folder: str) -> None:
    """
    Create backup of the heroes folder before processing.
    
    Args:
        mod_folder: Root folder of the mod
    
    Returns:
        True if backup was created, False if backup already exists
    """
    heroes_folder = os.path.join(mod_folder, "heroes")
    backup_folder = os.path.join(mod_folder, "backup")
    
    if os.path.exists(backup_folder):
        print(f"Backup already exists at {backup_folder}, skipping backup")
        return False
    
    shutil.copytree(heroes_folder, backup_folder)
    print(f"Backup created at {backup_folder}")
    return True

def restore_backup(mod_folder: str) -> None:
    """
    Restore the heroes folder from backup.
    
    Args:
        mod_folder: Root folder of the mod
    
    """
    heroes_folder = os.path.join(mod_folder, "heroes")
    backup_folder = os.path.join(mod_folder, "backup")

    create_backup(mod_folder)
    shutil.rmtree(heroes_folder)
    shutil.copytree(backup_folder, heroes_folder)
    shutil.rmtree(backup_folder)

    print("Mod restored!")

def process_mod(mod_folder: str) -> dict:
    """
    Process all atlas files and its corresponding PNG that are needed to fix in a mod.
    Walk through all of the atlas files in the mod folder,
    parse only required atlas file through calling process_atlas.
    Resize all corresponding PNG by calling resize_png.

    Args:
        mod_folder: Path to the root of the mod folder

    Returns:
        Dict with status: "success", "skipped", or "error"
    """

    mod_name = os.path.basename(mod_folder)

    try:
        create_backup(mod_folder)
        mod_structure = find_skin_mod_structure(mod_folder)

        if not mod_structure.get("is_type_a"):
            print("Skin does not have custom spine, no need to fix!")
            return {"status": "skipped", "mod_name": mod_name, "reason": "No custom spine"}
        else:
            atlas_folder = mod_structure.get("atlas_folder")
            png_variant_folders = mod_structure.get("png_variant_folders")
            target_suffixes = [".sprite.combat.atlas", ".sprite.walk.atlas", ".sprite.idle.atlas"]
            atlas_files = os.listdir(atlas_folder)

            for atlas in atlas_files:
                if any(atlas.endswith(suffix) for suffix in target_suffixes):
                    atlas_path = os.path.join(atlas_folder, atlas)
                    sprite_sheet = process_atlas(atlas_path)
                    
                    if sprite_sheet is None:
                        continue

                    for png_folder in png_variant_folders:
                        resize_png(png_folder, sprite_sheet)
            
            print(f"Success: '{mod_name}' processed")
            return {"status": "success", "mod_name": mod_name}
                        
    except OSError as e:
        print(f"Error '{mod_name}': File system error - {e}")
        return {"status": "error", "mod_name": mod_name, "reason": str(e)}
    except (ValueError, IndexError) as e:
        print(f"Error '{mod_name}': Invalid mod structure - {e}")
        return {"status": "error", "mod_name": mod_name, "reason": str(e)}
    except Exception as e:
        print(f"Error '{mod_name}': Unexpected error - {e}")
        return {"status": "error", "mod_name": mod_name, "reason": str(e)}

def process_multiple_mods(mod_folders: list) -> dict:
    """
    Process all the mods in the provided mod folder

    Args:
        mod_folders: list of single mod folders in the whole mod folder

    Returns:
        Dict with status: "success", "skipped", or "error"
    """
    results = {"success": [], "skipped": [], "error": []}

    for mod_folder in mod_folders:
        result = process_mod(mod_folder)
        results[result["status"]].append(result)