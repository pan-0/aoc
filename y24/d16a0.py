# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import heapq
import utils
from typing import Collection, Mapping

Grid = utils.Grid[str]
Vec2 = utils.Vec2[int]

Weight = int
Vertex = tuple[Vec2, Vec2]      # (Position, Orientation)
Edge   = tuple[Weight, Vertex]  # `Vertex` is the destination
Graph  = Mapping[Vertex, Collection[Edge]]

def parse(itr) -> Grid:
    return Grid([*map(str.strip, itr)])

def dijkstra(graph: Graph, S: Vertex, inf_dist: Weight) \
        -> Mapping[Vertex, Weight]:
    dists = {v: inf_dist for v in graph}
    dists[S] = 0
    heap = [(0, S)]
    while heap:
        _, v = heapq.heappop(heap)
        dist = dists[v]
        for weight, adj in graph[v]:
            total_dist = dist + weight
            if total_dist < dists[adj]:
                dists[adj] = total_dist
                heapq.heappush(heap, (total_dist, adj))
    return dists

def build_graph(grid: Grid, start: Vec2) -> Graph:
    graph = {}
    visited = set()
    stack = [(start, start)]
    while stack:
        prev, pos = stack.pop()
        if (prev, pos) not in visited:
            visited.add((prev, pos))
            vec = pos - prev
            edges = graph[pos, vec] = []
            for adj in grid.adjacent_cross(pos):
                if grid[adj] != '#':
                    new_vec = adj - pos
                    weight = 1 if new_vec == vec else 1001
                    edges.append((weight, (adj, new_vec)))
                    stack.append((pos, adj))
    return graph

def main():
    grid = parse(fileinput.input())
    S = grid.find('S')
    graph = build_graph(grid, S)
    dists = dijkstra(graph, (S, Vec2()), len(graph) * 1001)
    E = grid.find('E')
    r = min(filter(lambda dist: dist is not None,
                   map(lambda vec: dists.get((E, vec)), grid.ADJACENT_CROSS)))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
