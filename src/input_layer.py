def parse_plateau(text):
    parts = text.split()

    max_x = int(parts[0])
    max_y = int(parts[1])

    return {"max_x": max_x, "max_y": max_y}


def parse_position(text):
    parts = text.split()

    x = int(parts[0])
    y = int(parts[1])
    direction = parts[2]

    return {"x": x, "y": y, "direction": direction}
