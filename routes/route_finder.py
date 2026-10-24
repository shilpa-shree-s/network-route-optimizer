def find_shortest_route(graph, source, destination):
    """Return (total_latency, path), or None if no path exists."""

    #every server starts at "infinity" (unknown distance),
    # except the source, which is 0 because we are already there
    distances = {node: float("inf") for node in graph}
    distances[source] = 0

    # to remembers which server we came from to reach X
    previous = {}

    unvisited = set(graph)

    while unvisited:
        # pick the unvisited server with the smallest distance
        current = min(unvisited, key=distances.get)

        # if the smallest is still infinity, the rest cannot be reached
        if distances[current] == float("inf"):
            break

        if current == destination:
            break

        unvisited.remove(current)

        for neighbour, latency in graph[current].items():
            new_distance = distances[current] + latency
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current

    #destination still at infinity means there is no route
    if distances[destination] == float("inf"):
        return None

    # walk backwards from the destination to build the path
    path = []
    node = destination
    while node != source:
        path.append(node)
        node = previous[node]
    path.append(source)
    path.reverse()

    return distances[destination], path