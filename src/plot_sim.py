from matplotlib import pyplot as plt
import collections

def import_data2(file):
    d = collections.defaultdict(list)
    with open(file, 'r') as f:
        # Skip header
        next(f)

        for line in f:
            columns = line.split()
            for i, c in enumerate(columns):
                d[i].append(float(c))
    return d

def plot(file):
    d = import_data2(file)

    plt.figure()
    u, = plt.plot(d[0], d[1], 'g', label="u")
    y, = plt.plot(d[0], d[2], 'b', label="true response")
    y_sim, = plt.plot(d[0], d[3], 'r--', label="simulated response")
    plt.legend(handles=[u, y, y_sim])

    plt.draw()
    plt.show()


if __name__ == "__main__":
    plot("sim.txt")
