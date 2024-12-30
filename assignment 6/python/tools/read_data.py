
def read_data(filename):

    # read odometry and sensor readings from a file

    data = []
    fd = open(filename, 'rb')
    ok = True
    timestep = 0

    while ok:
        try:
            line = fd.readline().split()
            if line[0] == b'ODOMETRY':
                timestep += 1
                odometry = {'r1': float(line[1]), 't': float(line[2]), 'r2': float(line[3])}
                #print(odometry)
                data.append({'odom': odometry, 'sensor': []})
            if line[0] == b'SENSOR':
                #print(line)
                data[-1]['sensor'].append({'id': int(line[1]), 'range': float(line[2]), 'bearing': float(line[3])})
        except:
            ok = False
            fd.close()

    return data


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

    print(read_data('../../data/sensor_data.dat'))
    print(read_world('../../data/world.dat'))