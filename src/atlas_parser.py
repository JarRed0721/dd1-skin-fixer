with open(r"C:\NonSYSFile\Gam\Mod\DarkestDungeon\ResolutionProject\atlas\anim\crusader.sprite.idle.atlas") as f:
    lines = f.readlines()
    sprites = []
    pngFile = lines[1].strip()
    sheetWidth, sheetHeight = lines[2].split(":")[1].strip().split(",")
    spriteSheet = {"sheetWidth" : int(sheetWidth), "sheetHeight" : int(sheetHeight)}

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
                    x, y = lines[index + 2].split(":")[1].strip().split(", ")
                    width, height = lines[index + 3].split(":")[1].strip().split(", ")
                    sprite = {}
                    sprite["name"] = lines[index].strip()
                    sprite["x"] = int(x)
                    sprite["y"] = int(y)
                    sprite["width"] = int(width)
                    sprite["height"] = int(height)
                    sprites.append(sprite)
    print(pngFile)
    print(spriteSheet)
    print(sprites)