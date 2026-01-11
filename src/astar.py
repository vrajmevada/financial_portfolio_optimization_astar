import heapq

class Node:
    def __init__(self,state ,g,h,parent=None):
        self.state=state
        self.g=g
        self.h=h
        self.f=g+h
        self.parent=parent

    def __lt__(self,other):
        return self.f<other.f

def reconstruct_path(node):
    path=[]
    while node is not None:
        path.append(node.state)
        node=node.parent
    return path[::-1]

def astar(start_state,neighbor_fn,cost_fn,heuristic_fn,max_iterations=10000):
    open_list=[]
    closed_set=set()

    start_h=heuristic_fn(start_state)
    start_node=Node(start_state,g=cost_fn(start_state),h=start_h)

    heapq.heappush(open_list,start_node)

    iterations=0

    while open_list and iterations<max_iterations:
        current_node=heapq.heappop(open_list)
        current_state=current_node.state

        if current_state in closed_set:
            continue

        closed_set.add(current_state)
        for neighbor in neighbor_fn(current_state):
            if neighbor in closed_set:
                continue
            g=cost_fn(neighbor)
            h=heuristic_fn(neighbor)

            neighbor_node=Node(
                state=neighbor,
                g=g,
                h=h,
                parent=current_node
            )
            heapq.heappush(open_list,neighbor_node)
        iterations+=1
    return reconstruct_path(current_node),current_node