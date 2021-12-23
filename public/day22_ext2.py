import re

class Cuboid:
    def __init__(self, x, y, z, op=1):
        self.x = x
        self.y = y
        self.z = z
        self.op = op

    def size(self):
        x = self.x[1] - self.x[0] + 1
        y = self.y[1] - self.y[0] + 1
        z = self.z[1] - self.z[0] + 1
        if x <= 0 or y <= 0 or z <= 0:
            print("size error")
            exit()
        return x * y * z * self.op

    def __repr__(self):
        return "{} {} {}".format(self.x, self.y, self.z)

def createCuboid(p):
    if len(p) != 7:
        print("bad parameter number: " + str(p))
        exit()
    if p[0] == "on":
        op = 1
    else:
        op = -1
    params = list(map(int, p[1:]))
    if params[0] > params[1] or params[2] > params[3] or params[4] > params[5]:
        print("wrong order: " + str(p))
    x = (params[0], params[1])
    y = (params[2], params[3])
    z = (params[4], params[5])
    return Cuboid(x, y, z, op)

def lineIntersection(a, b):
    left = max(a[0], b[0])
    right = min(a[1], b[1])
    if right - left <= 0:
        return False
    return (left, right)

def intersection(a, b):
    x = lineIntersection(a.x, b.x)
    y = lineIntersection(a.y, b.y)
    z = lineIntersection(a.z, b.z)
    if x and y and z:
        return Cuboid(x, y, z)
    return False

#f = open("i", "rt")
f = open("input_d_22.txt", "rt")
content = f.read()
splt = content.splitlines()
line_re = re.compile("((?:on)|(?:off)) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)")
cuboids = []
for line in splt:
    m = line_re.match(line)
    if not m:
        print("error: " + line)
        exit()
    c = createCuboid(m.groups())
    cuboids.append(c)
out = [cuboids[0]]
for i in cuboids[1:]:
    for j in out.copy():
        c = intersection(i, j)
        if c:
            if j.op == 1:
                c.op = -1
            out.append(c)
    if i.op == 1:
        out.append(i)
count = 0
print(len(out))
for i in out:
    count += i.size()
print(count)
