def last(x: int, offset=0):
    return int(x * (x + 2 * offset + 1) / 2)


def n_pairing(x: int, y: int, c=50):
    start = last(x, 1)
    step = last(int(y/c), x)
    return (start + step) * c + (y % c)


def reverse_n_pairing(z: int, c=50):
    x = 0
    y = 0
    current_value = n_pairing(x, y, c)

    while current_value < z:
        while current_value < z:
            y += c
            current_value = n_pairing(x, y, c)

        if current_value > z:
            y -= c
            current_value = n_pairing(x, y, c)

        while current_value < z and y > 0:
            x += 1
            y -= c
            current_value = n_pairing(x, y, c)

        if current_value > z:
            x -= 1
            y += c
            current_value = n_pairing(x, y, c)

        if n_pairing(x, y + c, c) > z:
            while current_value < z:
                y += 1
                current_value = n_pairing(x, y, c)
    return x, y
