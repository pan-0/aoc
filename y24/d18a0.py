# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import heapq
import utils
from typing import Collection, Iterator, Mapping

Grid = utils.MutGrid[str]
Vec2 = utils.Vec2[int]

Vertex = Vec2
Graph  = Mapping[Vertex, Collection[Vertex]]

def parse(itr) -> Iterator[Vec2]:
    return map(lambda line: Vec2(*map(int, line.strip().split(','))), itr)

def dijkstra(graph: Graph, S: Vertex, E: Vertex, inf_dist: int) \
        -> Mapping[Vertex, int]:
    dists = {v: inf_dist for v in graph}
    dists[S] = 0
    heap = [(0, S)]
    while heap:
        _, v = heapq.heappop(heap)
        dist = dists[v]
        for adj in graph[v]:
            total_dist = dist + 1
            if total_dist < dists[adj]:
                dists[adj] = total_dist
                heapq.heappush(heap, (total_dist, adj))
        if v == E:
            break
    return dists

def build_graph(grid: Grid, S: Vec2) -> Graph:
    graph = {}
    visited = set()
    stack = [(S, S)]
    while stack:
        prev, pos = stack.pop()
        if (prev, pos) not in visited:
            visited.add((prev, pos))
            edges = graph[pos] = []
            for adj in grid.adjacent_cross(pos):
                if grid[adj] != '#':
                    edges.append(adj)
                    stack.append((pos, adj))
    return graph

def build_grid(bytez: Iterator[Vec2]) -> Grid:
    grid = Grid.empty(71, 71, '.')
    for byte in utils.take(bytez, 1024):
        grid[byte] = '#'
    return grid

def main():
    bytez = parse(fileinput.input())
    grid = build_grid(bytez)
    S = Vec2(0, 0)
    graph = build_graph(grid, S)
    E = Vec2(grid.cols - 1, grid.rows - 1)
    dists = dijkstra(graph, S, E, len(graph) * 2)
    r = dists.get(E)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
