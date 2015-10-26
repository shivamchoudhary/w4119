import operator
test_input = {'u': {'x': 5, 'w': 3,'v':7},
        'x': {'u': 5, 'w': 4,'y':7,'z':9},
        'w': {'u': 3, 'x': 4,'v':3,'y':8},
            'v': {'u': 7, 'w': 3, 'y': 4},
            'y': {'w': 8, 'x': 7,'v':4,'z':2},
            'z': {'x': 9, 'y': 2}}
source = "u"
class Dijkstra(object):
    def __init__(self):
        self.dist_vector = {}
        self.vertices = test_input.keys()
        self.queue = self.vertices
        self.N = [source]
        for vertice in self.vertices:
            if vertice in test_input[source]:
                self.dist_vector[vertice] = test_input[source][vertice]
            else:
                self.dist_vector[vertice] = int(1000000)
        for node in self.N:
            # w = min(self.dist_vector, key=self.dist_vector.get)
            w = self.next_node()
            if w and w not in self.N:
                self.N.append(w)
                for vertice in test_input[w].keys():
                    if vertice not in self.N:
                        self.dist_vector[vertice] = min(self.dist_vector[w]
                                +test_input[w][vertice],self.dist_vector[vertice])
            else:
                self.dist_vector[source]=0
                print self.dist_vector
                break
    def next_node(self):
        local_vector = self.dist_vector.copy()
        for nodes in self.N:
            del(local_vector[nodes])
        try:
            w = min(local_vector, key=local_vector.get)
        except ValueError:
            return None

        return w
def main():
    Dijkstra()
if __name__=="__main__":
    main()



