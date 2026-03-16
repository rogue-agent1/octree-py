"""Octree — 3D spatial subdivision."""
class Octree:
    def __init__(self, cx, cy, cz, size, cap=8):
        self.cx,self.cy,self.cz,self.size = cx,cy,cz,size
        self.cap = cap; self.points = []; self.children = None
    def contains(self, p):
        s = self.size/2
        return all(self.__dict__[k]-s <= p[i] < self.__dict__[k]+s for i,k in enumerate(['cx','cy','cz']))
    def subdivide(self):
        s = self.size/4
        self.children = []
        for dx in (-1,1):
            for dy in (-1,1):
                for dz in (-1,1):
                    self.children.append(Octree(self.cx+dx*s, self.cy+dy*s, self.cz+dz*s, self.size/2, self.cap))
    def insert(self, p):
        if not self.contains(p): return False
        if len(self.points) < self.cap and self.children is None:
            self.points.append(p); return True
        if self.children is None: self.subdivide()
        for c in self.children:
            if c.insert(p): return True
        self.points.append(p); return True
    def count(self):
        n = len(self.points)
        if self.children:
            n += sum(c.count() for c in self.children)
        return n

if __name__ == "__main__":
    import random; random.seed(42)
    ot = Octree(50,50,50,100)
    pts = [(random.uniform(0,100),random.uniform(0,100),random.uniform(0,100)) for _ in range(500)]
    for p in pts: ot.insert(p)
    assert ot.count() == 500
    print(f"Octree: {ot.count()} points stored in 3D")
    print("All tests passed!")
