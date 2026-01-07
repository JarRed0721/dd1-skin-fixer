with open(r"C:\NonSYSFile\Gam\Mod\DarkestDungeon\ResolutionProject\atlas\anim\crusader.sprite.idle.atlas") as f:
    lines = f.readlines()
    # line.startswith(" ") to check for leading space
    # ":" in line to check if a line contains a colon
    # "." in line to check if a line contains a period
    for index in range(len(lines)):
        if lines[index].strip() == "":
            continue 
        elif not lines[index].startswith(" "):
            if "." not in lines[index] and ":" not in lines[index]:
                print(index, lines[index])