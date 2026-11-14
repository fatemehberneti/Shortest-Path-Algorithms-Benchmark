import random


class Graph:
    """Random undirected weighted graph generator using an adjacency list."""
    def __init__(self, num_vertices, edge_prob=1/3, weights=(1, 5, 20)):
        self.num_vertices = num_vertices
        self.edge_prob = edge_prob
        self.weights = weights
        self.adjacency_list = {i: [] for i in range(num_vertices)}
        self.generate_edges()

    def generate_edges(self):
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if random.random() < self.edge_prob:
                    weight = random.choice(self.weights)
                    self.adjacency_list[i].append((j, weight))
                    self.adjacency_list[j].append((i, weight))


class MinBiHeap:
    """Custom Min Binary Heap implementation for Dijkstra's priority queue."""
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def insert(self, item):
        self.heap.append(item)
        self.sift_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.sift_down(0)
        return min_item

    def sift_up(self, i):
        while i > 0:
            parent_i = (i - 1) // 2
            if self.heap[i] < self.heap[parent_i]:
                self.heap[i], self.heap[parent_i] = self.heap[parent_i], self.heap[i]
                i = parent_i
            else:
                break

    def sift_down(self, i):
        n = len(self.heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != i:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break


class ShortestPath:
    """Implementation of Single-Source and All-Pairs Shortest Path algorithms."""
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, source):
        distances = [float('inf')] * self.graph.num_vertices
        distances[source] = 0
        min_heap = MinBiHeap()
        min_heap.insert((0, source))

        while not min_heap.is_empty():
            current_distance, current_vertex = min_heap.extract_min()
            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self.graph.adjacency_list[current_vertex]:
                distance = distances[current_vertex] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    min_heap.insert((distance, neighbor))

        return distances

    def dijkstra_all_pairs(self):
        return [self.dijkstra(source) for source in range(self.graph.num_vertices)]

    def bellman_ford(self, source):
        distance = [float('inf')] * self.graph.num_vertices
        distance[source] = 0

        for _ in range(self.graph.num_vertices - 1):
            changed = False
            for u in range(self.graph.num_vertices):
                for v, w in self.graph.adjacency_list[u]:
                    if distance[u] != float('inf') and distance[u] + w < distance[v]:
                        distance[v] = distance[u] + w
                        changed = True
            if not changed:
                break

        # Negative cycle check
        for u in range(self.graph.num_vertices):
            for v, w in self.graph.adjacency_list[u]:
                if distance[u] != float('inf') and distance[u] + w < distance[v]:
                    raise ValueError("Graph contains a negative weight cycle")

        return distance

    def bellman_ford_all_pairs(self):
        return [self.bellman_ford(source) for source in range(self.graph.num_vertices)]

    def floyd_warshall(self):
        v_count = self.graph.num_vertices
        distance = [[float('inf')] * v_count for _ in range(v_count)]

        for i in range(v_count):
            distance[i][i] = 0

        for u in range(v_count):
            for v, w in self.graph.adjacency_list[u]:
                if w < distance[u][v]:
                    distance[u][v] = w

        for k in range(v_count):
            for i in range(v_count):
                for j in range(v_count):
                    if distance[i][k] + distance[k][j] < distance[i][j]:
                        distance[i][j] = distance[i][k] + distance[k][j]

        for i in range(v_count):
            if distance[i][i] < 0:
                raise ValueError("Graph contains a negative weight cycle")

        return distance
