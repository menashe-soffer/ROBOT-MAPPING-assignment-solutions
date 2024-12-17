
def read_world(filename):

    landmarks = []
    fd = open(filename, 'rt')

    ok = True
    while ok:
        try:
            line = fd.readline().split()
            landmarks.append({'id': int(line[0]), 'x': float(line[1]), 'y': float(line[2])})
        except:
            ok = False

    fd.close()
    return landmarks


if __name__ == '__main__':

    print(read_world('../../data/world.dat'))