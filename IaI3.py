import math
import Node_BNs
import random
import copy
import pickle

def read_from_file (a):
    file=open(a, "r")
    file_by_lines= file.readlines()
    return file_by_lines


def build_graph():
    lines = read_from_file("C:\\Users\\ohadelyahu\\PycharmProjects\\IaI3\\data.txt")
    adj_graph = {}
    vertex_info = {}
    adj_list = {}
    Ppersistence = 0
    init_v =[]
    for line in lines:
        if(line=="\n"):
            continue
        elif (line[:2]=="#N"):
            number_of_vertexs=line[3]
            for i in range(int(number_of_vertexs)):
                init_v.append(False)
                adj_graph[i+1] = []
                adj_list[i + 1] = []
        elif (line[0:2]=="#V"):
            ###############
            row_splitted = line.split(' ')
            number_of_vertex = int(row_splitted[0][2])
            is_flooding = row_splitted[1]
            prob_flood = float(row_splitted[2])
            vertex_info[number_of_vertex] = [is_flooding, prob_flood]
            init_v[number_of_vertex-1] = True
        elif (line[0:2]=="#E"):
            row_splitted = line.split(' ')
            edge = int(row_splitted[0][2:])
            vertex_from = int(row_splitted[1])
            vertex_to = int(row_splitted[2])
            vertex_weight = int(row_splitted[3][1:-1])
            adj_graph[edge] = [vertex_from, vertex_to, vertex_weight]
            adj_list[vertex_from].append(vertex_to)
            adj_list[vertex_to].append(vertex_from)
        elif line[0:2] == "#P":
            line_splited = line.split(' ')
            Ppersistence = float(line_splited[1])
    for i in range(int(number_of_vertexs)): # init vertex that dont mentioned in the text file
        if not init_v[i]:
            number_of_vertex = i+1
            is_flooding = "N"
            prob_flood = float(0)
            vertex_info[number_of_vertex] = [is_flooding, prob_flood]
            init_v[number_of_vertex - 1] = True
    return [adj_graph, vertex_info, Ppersistence, adj_list]


def build_bayes_nets(graph, info, Pper, time):
    net = []
    nodes = {}
    for vertex in info:
        id = str(vertex) + "_0_v"
        node = Node_BNs.Node_bn([], 0, "v", id, 0, [], Pper)
        node.create_table_roots(info[vertex][1])
        net.append(node)
        nodes[id] = node
        for j in range(1,time):
            id = str(vertex) + "_" + str(j) + "_v"
            node1 = Node_BNs.Node_bn([node], 1, "v", id, j, [], Pper)
            node1.create_node_table()
            node.children.append(node1)
            nodes[id] = node1
            node = node1
    for edge in graph:
        for j in range(time):
            id1 = str(graph[edge][0]) + "_" + str(j) + "_v"
            id2 = str(graph[edge][1]) + "_" + str(j) + "_v"
            id = str(edge) + "_" + str(j) + "_e"
            node = Node_BNs.Node_bn([nodes[id1],nodes[id2]], 2, "e", id, j, [graph[edge][2]], Pper)
            nodes[id] = node
            nodes[id1].children.append(node)
            nodes[id2].children.append(node)
            node.create_node_table()
    return [net, nodes]


def print_Bayes_Nets(nodes):
    for n in nodes:
        node = nodes[n]
        st = node.id.split('_')
        if node.type == "v":
            print("VERTEX " + st[0] + ", time " + st[1] + ":")
            if node.time == 0:
                print("P(Flooding) = " + str(node.table_distrb[0][1]))
                print("P(not Flooding) = " + str(node.table_distrb[1][1]))
                print("")
                print("")
            else:
                print("P(Flooding | Flooding in time " + str(int(st[1])-1) + ") = " + str(node.table_distrb[0][2]))
                print("P(not Flooding | Flooding in time " + str(int(st[1]) - 1) + ") = " + str(node.table_distrb[1][2]))
                print("P(Flooding | not Flooding in time " + str(int(st[1]) - 1) + ") = " + str(node.table_distrb[2][2]))
                print("P(not Flooding | not Flooding in time " + str(int(st[1]) - 1) + ") = " + str(node.table_distrb[3][2]))
                print("")
                print("")
        else:
            id_f1 = node.fathers[0].id.split("_")
            id_f2 = node.fathers[1].id.split("_")
            st = node.id.split('_')
            print("Edge " + st[0] + ", time " + st[1] + ":")
            print("P(Blockage 1 | Flooding " + id_f1[0] + ", Flooding " + id_f2[0] + ") = " + str(node.table_distrb[0][3]))
            print("P(Blockage 0 | Flooding " + id_f1[0] + ", Flooding " + id_f2[0] + ") = " + str(node.table_distrb[1][3]))
            print("P(Blockage 1 | Flooding " + id_f1[0] + ", not Flooding " + id_f2[0] + ") = " + str(node.table_distrb[2][3]))
            print("P(Blockage 0 | Flooding " + id_f1[0] + ", not Flooding " + id_f2[0] + ") = " + str(node.table_distrb[3][3]))
            print("P(Blockage 1 | not Flooding " + id_f1[0] + ", Flooding " + id_f2[0] + ") = " + str(node.table_distrb[4][3]))
            print("P(Blockage 0 | not Flooding " + id_f1[0] + ", Flooding " + id_f2[0] + ") = " + str(node.table_distrb[5][3]))
            print("P(Blockage 1 | not Flooding " + id_f1[0] + ", not Flooding " + id_f2[0] + ") = " + str(node.table_distrb[6][3]))
            print("P(Blockage 0 | not Flooding " + id_f1[0] + ", not Flooding " + id_f2[0] + ") = " + str(node.table_distrb[7][3]))
            print("")
            print("")


def print_add_evidence_menu(result):
    print("Choose evidence type: ")
    print("1. Flooding vertex")
    print("2. Not flooding vertex")
    print("3. Blockage edge")
    print("4. Not Blockage edge")
    choose = int(input())
    while choose < 0 or choose > 4:
        print("Illegal input please insert again number between 1 to 4")
        choose = int(input())
    print("Choose number of vertex/ edge: ")
    num = int(input())
    print("Choose time: ")
    time = int(input())
    if choose == 1 or choose == 2:
        id = str(num) + "_" + str(time) + "_v"
    else:
        id = str(num) + "_" + str(time) + "_e"
    if choose == 1 or choose == 3:
        choose = 0
    else:
        choose = 1
    result[id] = choose


def menu(network, nodes, graph, info, V, adj_list):
    evidence = {}
    while True:
        print("")
        print("Choose action from the following list: ")
        print("1. Reset evidence list to empty")
        print("2. Add evidence")
        print("3. Do reasoning")
        print("4. Quit")
        print("5. Print evidence")
        choose = int(input("Enter here: "))
        while  choose < 0 or choose > 5:
            print("Illegal input please insert again number between 1 to 4")
            choose = int(input())
        if choose == 1:
            evidence = {}
        elif choose == 2:
            print_add_evidence_menu(evidence)
        elif choose == 3:
            print("Choose Action: ")
            print("1. Probability of vertex/edge flooded/blocked")
            print("2. Probability for certain path")
            print("3. Path between 2 giveמ vertices that has the highest probability of being free from blockages at time 1")
            action = int(input("Enter here: "))
            if action == 1:
                print("Enter vertex or edge (v\e): ")
                var = input()
                print("Enter number of vertex or edge: ")
                num = int(input())
                print("Enter time brother: ")
                time = int(input())
                if var == "v":
                    print("Choose evidence type: ")
                    print("1. Flooding vertex")
                    print("2. Not flooding vertex")
                elif var == "e":
                    print("Choose evidence type: ")
                    print("1. Blockage edge")
                    print("2. Not Blockage edge")
                typeo = int(input())
                if typeo == 2:
                    typeo = 1
                else:
                    typeo = 0
                result = reasoning(network, evidence, nodes, [var, num, time, typeo])
                print("The result for your query is: " + str(result))
            elif action == 2:
                print("Enter set of edges: (For Example: 1,2,3)")
                edges_str = input("Enter Here: ")
                print("")
                edges = edges_str.split(',')
                for i in range(len(edges)):
                    edges[i] = int(edges[i])
                input_time = int(input("Enter time: "))
                print("")
                print("Choose evidence type: ")
                print("1. Blockage edge")
                print("2. Not Blockage edge")
                typoo = int(input("Enter Here: "))
                if typoo == 2:
                    typoo = 1
                else:
                    typoo = 0
                final_prob = 1
                copy_evi = copy.deepcopy(evidence)
                for edge in edges:
                    res = reasoning(network, copy_evi, nodes, ["e", edge, input_time, typoo])
                    final_prob = final_prob*res
                    id = str(edge) + "_" + str(input_time) + "_e"
                    if id in copy_evi:
                        if not copy_evi[id] == typoo:
                            final_prob = 0
                            break
                    copy_evi[id] = typoo
                print("The result for your query is: " + str(final_prob))
            else:
                v_from = int(input("Enter from where the path start: "))
                v_to = int(input("Enter where the path ends: "))
                print("")
                input_time = int(input("Enter time: "))
                print("")
                # print("Choose evidence type: ")
                # print("1. Blockage edge")
                # print("2. Not Blockage edge")
                # typoo = int(input("Enter Here: "))
                # if typoo == 2:
                #     typoo = 1
                # else:
                #     typoo = 0
                typoo = 1
                paths = Bonus_Build_Paths(V, adj_list, v_from, v_to)
                p_max = 0
                path_max = []
                for path in paths:
                    # ---- Find Edges ----
                    edges_path = []
                    for i in range(len(path)-1):
                        for e in graph:
                            if (graph[e][0] == path[i] and graph[e][1] == path[i+1]) or (graph[e][0] == path[i+1] and graph[e][1] == path[i]):
                                edges_path.append(e)
                                break
                    # ---- Find Edges ----

                    # ---- Calculate Prob for edges like in number 3 ----
                    final_prob = 1
                    copy_evi = copy.deepcopy(evidence)
                    for edge in edges_path:
                        res = reasoning(network, copy_evi, nodes, ["e", edge, input_time, typoo])
                        final_prob = final_prob * res
                        id = str(edge) + "_" + str(input_time) + "_e"
                        if id in copy_evi:
                            if not copy_evi[id] == typoo:
                                final_prob = 0
                                break
                        copy_evi[id] = typoo
                    # ---- End of calculate prob for edges ----

                    # --- Add to final prob the probs of vertices ----
                    # for v in path:
                    #     final_prob = final_prob*reasoning(network, copy_evi, nodes, ["v", v, input_time, typoo])
                    # ---- End Of Calculation ----

                    if final_prob > p_max:
                        p_max = final_prob
                        path_max = path

                print("Best Path is: " + str(path_max) + " in probability of: " + str(p_max))
                print("")

        elif choose == 4:
            print("The program will close soon")
            break
        else:
            print_evidence(evidence)


def calculate_prob(node, evidence, non_evi):
    totval = 0
    p3 = 1
    p4 = 1
    for father in node.fathers:
        if father.id in evidence:
            val = evidence[father.id]
        else:
            val = non_evi[father.id]
        totval = totval*2 +val
    totval *= 2
    p1 = node.table_distrb[totval][-1]
    p2 = node.table_distrb[totval+1][-1]
    for child in node.children:
        totval = 0
        for father in child.fathers:
            if father.id == node.id:
                totval = totval*2
            else:
                if father.id in evidence:
                    val = evidence[father.id]
                else:
                    val = non_evi[father.id]
                totval = totval*2 + val
        if child.id in evidence:
            val = evidence[child.id]
        else:
            val = non_evi[child.id]
        totval = totval*2 + val
        p3 *= child.table_distrb[totval][-1]
    for child in node.children:
        totval = 0
        for father in child.fathers:
            if father.id == node.id:
                totval = totval * 2 + 1
            else:
                if father.id in evidence:
                    val = evidence[father.id]
                else:
                    val = non_evi[father.id]
                totval = totval * 2 + val
        if child.id in evidence:
            val = evidence[child.id]
        else:
            val = non_evi[child.id]
        totval = totval * 2 + val
        p4 *= child.table_distrb[totval][-1]
    res = (p1 * p3) / (p1 * p3 + p2 * p4)
    return res


def reasoning(network, evidences, nodes, Q):
    non_evi = {}
    samples = []
    counter = 10
    for node in nodes:
        if node not in evidences:
            number = random.random()
            if number <= 0.5:
                non_evi[node] = 1
            else:
                non_evi[node] = 0
    while len(samples) < 10000:
        for node in non_evi:
            if counter == 0:
                sample = copy.deepcopy(evidences)
                sample.update(non_evi)
                samples.append(sample)
                counter = 5
            prob = calculate_prob(nodes[node], evidences, non_evi)
            number = random.random()
            if number <= prob:
                non_evi[node] = 0
            else:
                non_evi[node] = 1
            counter -= 1
    id = str(Q[1]) + "_" + str(Q[2]) + "_" + Q[0]
    count_good_samples = 0
    for sample in samples:
        if sample[id] == Q[3]:
            count_good_samples += 1
    return count_good_samples/len(samples)


def print_evidence(evidence):
    print(evidence)


def main():
    graphs = build_graph()
    graph = graphs[0]
    info = graphs[1]
    adj_list = graphs[3]
    V= []
    for i in info:
        V.append(i)

    Ppersistence = graphs[2]
    time = 2
    network = build_bayes_nets(graph, info, Ppersistence, time)
    print_Bayes_Nets(network[1])
    menu(network[0], network[1], graph, info, V, adj_list)


'''A recursive function to print all paths from 'u' to 'd'.
visited[] keeps track of vertices in current path.
path[] stores actual vertices and path_index is current
index in path[]'''



def findAllPathsUtil(u, d, visited, path, paths, graph, filehandler):
    # Mark the current node as visited and store in path
    visited[u] = True
    path.append(u)
    # If current vertex is same as destination, then print
    # current path[]
    if u == d:
        paths.append(path)
        pickle.dump(path, filehandler)
    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        for i in graph[u]:
            if visited[i] == False:
                findAllPathsUtil(i, d, visited, path, paths, graph, filehandler)

    # Remove current vertex from path[] and mark it as unvisited
    path.pop()
    visited[u] = False


# Prints all paths from 's' to 'd'
def findAllPaths(s, d, V, graph, filehandler):
    # Mark all the vertices as not visited
    visited = [False] * (len(V) + 1)
    paths = []
    # Create an array to store paths
    path = []
    return findAllPathsUtil(s, d, visited, path, paths, graph, filehandler)


def Bonus_Build_Paths(V, adj_list, u, d):
    filehandler = open("try", 'wb')
    findAllPaths(u, d, V, adj_list, filehandler)
    filehandler.close()
    filehandler = open("try", 'rb')
    paths = []
    while True:
        try:
            r = pickle.load(filehandler)
            paths.append(r)
        except:
            break
    return paths


if __name__ =="__main__":
    main()

