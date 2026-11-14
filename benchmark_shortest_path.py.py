from shortest_path import ShortestPath, Graph
import random
import time
import matplotlib.pyplot as plt

vertex_counts = [10, 25, 50, 75]
runs = 20

single_dijkstra_times = []
single_bellman_times = []
all_dijkstra_times = []
all_bellman_times = []
floyd_times = []

for n in vertex_counts:
    sd_sum = sb_sum = ad_sum = ab_sum = fw_sum = 0

    for _ in range(runs):
        graph = Graph(n)
        sp = ShortestPath(graph)
        source = random.randint(0, n - 1)

        # Single-Source Dijkstra
        t0 = time.time()
        sp.dijkstra(source)
        sd_sum += time.time() - t0

        # Single-Source Bellman-Ford
        t0 = time.time()
        sp.bellman_ford(source)
        sb_sum += time.time() - t0

        # All-Pairs Dijkstra
        t0 = time.time()
        sp.dijkstra_all_pairs()
        ad_sum += time.time() - t0

        # All-Pairs Bellman-Ford
        t0 = time.time()
        sp.bellman_ford_all_pairs()
        ab_sum += time.time() - t0

        # Floyd-Warshall
        t0 = time.time()
        sp.floyd_warshall()
        fw_sum += time.time() - t0

    single_dijkstra_times.append(sd_sum / runs)
    single_bellman_times.append(sb_sum / runs)
    all_dijkstra_times.append(ad_sum / runs)
    all_bellman_times.append(ab_sum / runs)
    floyd_times.append(fw_sum / runs)

# Plot 1: All-Pairs Shortest Path Comparison
plt.figure(figsize=(8, 6))
plt.plot(vertex_counts, all_dijkstra_times, label="Dijkstra (All-Pairs)", color="orange", marker="o")
plt.plot(vertex_counts, all_bellman_times, label="Bellman-Ford (All-Pairs)", color="blue", marker="s")
plt.plot(vertex_counts, floyd_times, label="Floyd-Warshall", color="green", marker="^")
plt.title("All-Pairs Shortest Path Algorithms Runtime Comparison")
plt.xlabel("Number of Vertices (|V|)")
plt.ylabel("Average Runtime (s)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.savefig("all_pairs_comparison.png", dpi=300, bbox_inches="tight")
plt.show()

# Plot 2: Single-Source Shortest Path Comparison
plt.figure(figsize=(8, 6))
plt.plot(vertex_counts, single_dijkstra_times, label="Dijkstra (Single-Source)", color="red", marker="o")
plt.plot(vertex_counts, single_bellman_times, label="Bellman-Ford (Single-Source)", color="purple", marker="s")
plt.title("Single-Source Shortest Path Algorithms Runtime Comparison")
plt.xlabel("Number of Vertices (|V|)")
plt.ylabel("Average Runtime (s)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.savefig("single_source_comparison.png", dpi=300, bbox_inches="tight")
plt.show()