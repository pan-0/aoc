# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import heapq
import utils
from typing import Collection, Mapping
from pprint import pprint

Grid = utils.Grid[str]
Vec2 = utils.Vec2[int]

Weight = int
Vertex = tuple[Vec2, Vec2]      # (Position, Orientation)
Edge   = tuple[Weight, Vertex]  # `Vertex` is the destination
Graph  = Mapping[Vertex, Collection[Edge]]

Distances = Mapping[Vertex, Weight]
Paths = Mapping[Vertex, set[Vertex]]

def parse(itr) -> Grid:
    return Grid([*map(str.strip, itr)])

def dijkstra(graph: Graph, S: Vertex, inf_dist: Weight) -> tuple[Distances,
                                                                 Paths]:
    dists = {v: inf_dist for v in graph}
    dists[S] = 0
    paths = {S: {}}
    heap = [(0, S)]
    while heap:
        _, v = heapq.heappop(heap)
        dist = dists[v]
        for weight, adj in graph[v]:
            total_dist = dist + weight
            if total_dist < dists[adj]:
                dists[adj] = total_dist
                paths[adj] = {v}
                heapq.heappush(heap, (total_dist, adj))
            elif total_dist == dists[adj]:
                paths[adj].add(v)
    return (dists, paths)

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

def tiles_n(graph: Graph, S: Vec2, E: Vec2) -> int:
    inf_dist = len(graph) * 1001
    dists, paths = dijkstra(graph, (S, Vec2()), inf_dist)

    stack = []
    best = (inf_dist, Vec2())
    for vec in Grid.ADJACENT_CROSS:
        if (dist := dists.get((E, vec))) is not None:
            if dist < best[0]:
                best = (dist, vec)
                stack = [(E, vec)]
            elif dist == best[0]:
                stack.append((E, vec))

    tiles = set()
    while stack:
        tile, vec = stack.pop()
        tiles.add(tile)
        stack.extend(paths[tile, vec])

    return len(tiles)

def main():
    grid = parse(fileinput.input())
    S = grid.find('S')
    graph = build_graph(grid, S)
    E = grid.find('E')
    r = tiles_n(graph, S, E)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
