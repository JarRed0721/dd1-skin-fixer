with open(r"C:\NonSYSFile\Gam\Mod\DarkestDungeon\ResolutionProject\atlas\anim\crusader.sprite.idle.atlas") as f:
    
    #list lines: list of each lines in the atlas file
    lines = f.readlines()
    #list sprites: list of all sprites from one atlas file
    sprites = []
    #String pngFile: the name of the related PNG file
    pngFile = lines[1].strip()
    #String width, height: the width and the height of the spritesheet
    width, height = lines[2].split(":")[1].strip().split(",")
    sheetWidth = int(width)
    sheetHeight = int(height)
    #dict spriteSheet: the width and length of the whole spritesheet
    spriteSheet = {"sheetWidth" : sheetWidth, "sheetHeight" : sheetHeight}

    if sheetWidth > sheetHeight:
        scale = 800 / sheetWidth
    else:
        scale = 800 / sheetHeight

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

    spriteSheet["sheetWidth"] = sheetWidth * scale
    spriteSheet["sheetHeight"] = sheetHeight * scale

# (empty line)
# crusader.sprite.idle.png
# size: 800,800
# format: RGBA8888
# filter: Linear,Linear
# repeat: none
with open("output.atlas", "w") as f:
    f.write("\n")
    f.write(f"{pngFile}\n")
    f.write(f"size: {round(spriteSheet['sheetWidth'])},{round(spriteSheet['sheetHeight'])}\n")
    f.write("format: RGBA8888\n")
    f.write("filter: Linear,Linear\n")
    f.write("repeat: none\n")

#   sprite name
#     rotate: false
#     xy: 2, 27
#     size: 28, 56
#     orig: 28, 56
#     offset: 0, 0
#     index: -1
    for sprite in sprites:
        f.write(f"{sprite["name"]}\n")
        f.write(f"  rotate: {sprite["rotate"]}\n")
        f.write(f"  xy: {sprite["x"]}, {sprite["y"]}\n")
        f.write(f"  size: {sprite["width"]},{sprite["height"]}\n")
        f.write(f"  orig: {sprite["width"]},{sprite["height"]}\n")
        f.write("  offset: 0, 0\n")
        f.write("  index: -1\n")