def parse_plateau(text):
    parts = text.split()

    max_x = int(parts[0])
    max_y = int(parts[1])

    return {"max_x": max_x, "max_y": max_y}
