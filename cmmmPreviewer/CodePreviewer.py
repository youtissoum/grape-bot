import math
from PIL import Image

TEXTURE_PATH = __file__.removesuffix("CodePreviewer.py").replace("\\", "/") + "textures/"
TEXTURE_SIZE = 16
FINAL_SIZE = 500

def b74_decode(chars: str, /) -> int:
    b74_key = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&+-.=?^{}"
    result = 0

    for char in chars:
        result *= 74
        if (b74_char := b74_key.find(char)) == -1:
            raise ValueError(f"Invalid character in base 74 number: {char}")
        else:
            result += b74_char

    return result

def parse_v1(code_str: str) -> tuple[tuple[int, int], list[tuple[int, int, int, int]], list[tuple[int, int]], str]:
    code: list[str] = code_str.split(";")

    width = int(code[1])
    height = int(code[2])

    # print(width, height)

    cells: list[str] = code[4].split(',')
    
    parsedCells: list[tuple[int, int, int, int]] = []

    if cells:
        for cell_str in cells:
            # id, rot, x, y
            cell: tuple[int, int, int, int] = tuple(map(int, cell_str.split(".")))
            parsedCells.append(cell)

    placeables: list[str] = code[3].split(',')

    parsedPlaceables: list[tuple[int, int]] = []

    if placeables[0] != '':
        for placeable_str in placeables:
            # x, y
            placeable: tuple[int, int] = tuple(map(int, placeable_str.split('.')))
            parsedPlaceables.append(placeable)

    return(((width, height), parsedCells, parsedPlaceables, code[5]))

def parse_v3(code_str: str) -> tuple[tuple[int, int], list[tuple[int, int, int, int]], list[tuple[int, int]], str]:
    arguments = code_str.split(';')

    rawCells: list[tuple[int, int]] = []

    gridWidth = b74_decode(arguments[1])
    gridHeight = b74_decode(arguments[2])

    length = 0
    dataIndex = 0
    gridIndex = 0
    temp = ""

    cellDataHistory = [0] * (gridWidth * gridHeight)
    offset = 0

    while dataIndex < len(arguments[3]):
        if arguments[3][dataIndex] == ')' or arguments[3][dataIndex] == '(':
            if arguments[3][dataIndex] == ')':
                dataIndex += 2
                offset = b74_decode(arguments[3][dataIndex - 1])
                length = b74_decode(arguments[3][dataIndex])
            else:
                dataIndex += 1
                temp = ""
                while arguments[3][dataIndex] != ')' and arguments[3][dataIndex] != '(':
                    temp += arguments[3][dataIndex]
                    dataIndex += 1
                offset = b74_decode(temp)
                if arguments[3][dataIndex] == ')':
                    dataIndex += 1
                    length = b74_decode(arguments[3][dataIndex])
                else:
                    dataIndex += 1
                    temp = ""
                    while arguments[3][dataIndex] != ')':
                        temp += arguments[3][dataIndex]
                        dataIndex += 1
                    length = b74_decode(temp)
            for i in range(length):
                rawCells.append((cellDataHistory[gridIndex - offset - 1], gridIndex))
                cellDataHistory[gridIndex] = cellDataHistory[gridIndex - offset - 1]
                gridIndex += 1
        else:
            rawCells.append((b74_decode(arguments[3][dataIndex]), gridIndex))
            cellDataHistory[gridIndex] = b74_decode(arguments[3][dataIndex])
            gridIndex += 1
        dataIndex += 1

    newCells: list[tuple[int, int, int, int]] = []
    placeables: list[tuple[int, int]] = []

    for rawCell in rawCells:
        if rawCell[0] >= 72:
            continue
        cellX = math.floor(rawCell[1] % gridWidth)
        cellY = math.floor(rawCell[1] / gridWidth)
        if rawCell[0] % 2 == 1:
            placeables.append((cellX, cellY))
        cellType = math.floor((rawCell[0] / 2) % 9)
        cellDirection = math.floor(rawCell[0] / 18)
        newCells.append((cellType, cellDirection, cellX, cellY))

    return(((gridWidth, gridHeight), newCells, [], arguments[4]))

def parse_any(code: str):
    if code.startswith("V1"):
        level = parse_v1(code)
    elif code.startswith("V2"):
        raise NotImplementedError("V2 codes have not been implemented yet")
    elif code.startswith("V3"):
        level = parse_v3(code)
    else:
        return

    return level

def preview_level(code: tuple[tuple[int, int], list[tuple[int, int, int, int]], list[tuple[int, int]], str], scale=2):
    bg = Image.open(f'{TEXTURE_PATH}background.png')
    generator = Image.open(f"{TEXTURE_PATH}generator.png").transpose(Image.FLIP_TOP_BOTTOM)
    C_spinner = Image.open(f"{TEXTURE_PATH}C_spinner.png").transpose(Image.FLIP_TOP_BOTTOM)
    CC_spinner = Image.open(f"{TEXTURE_PATH}CC_spinner.png").transpose(Image.FLIP_TOP_BOTTOM)
    mover = Image.open(f"{TEXTURE_PATH}mover.png").transpose(Image.FLIP_TOP_BOTTOM)
    slide = Image.open(f"{TEXTURE_PATH}slide.png").transpose(Image.FLIP_TOP_BOTTOM)
    push = Image.open(f"{TEXTURE_PATH}push.png").transpose(Image.FLIP_TOP_BOTTOM)
    immobile = Image.open(f"{TEXTURE_PATH}immobile.png").transpose(Image.FLIP_TOP_BOTTOM)
    enemy = Image.open(f"{TEXTURE_PATH}enemy.png").transpose(Image.FLIP_TOP_BOTTOM)
    trash = Image.open(f"{TEXTURE_PATH}trash.png").transpose(Image.FLIP_TOP_BOTTOM)
    placeable = Image.open(f"{TEXTURE_PATH}placeable.png").transpose(Image.FLIP_TOP_BOTTOM)
    all_cells = [generator, C_spinner, CC_spinner, mover, slide, push, immobile, enemy, trash]

    width, height = code[0]

    width  *= TEXTURE_SIZE
    height *= TEXTURE_SIZE

    img = Image.new(mode="RGB", size=(int(width), int(height)))

    for i in range(0, width, TEXTURE_SIZE):
        for j in range(0, height, TEXTURE_SIZE):
            img.paste(bg, (i, j))

    for placeable_data in code[2]:
        img.paste(placeable, (placeable_data[0] * TEXTURE_SIZE, placeable_data[1] * TEXTURE_SIZE))

    for cell in code[1]:
        cell_to_paste = all_cells[cell[0]]

        img.paste(cell_to_paste.rotate(cell[1] * 90), (cell[2] * TEXTURE_SIZE, cell[3] * TEXTURE_SIZE))

    bg.close()
    generator.close()
    C_spinner.close()
    CC_spinner.close()
    mover.close()
    slide.close()
    push.close()
    immobile.close()
    enemy.close()
    trash.close()
    placeable.close()

    if scale == 0:
        return(img)
    else:
        nextWidth = math.floor(width * scale)
        nextHeight = math.floor(height * scale)
        scaledImg = img.resize(size=(nextWidth, nextHeight), resample=Image.NEAREST)
        return(scaledImg.transpose(1))