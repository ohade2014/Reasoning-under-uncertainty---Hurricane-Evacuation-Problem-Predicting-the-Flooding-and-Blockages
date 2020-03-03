import math

class Node_bn:
    def __init__(self, fathers, num_fathers, typer, id, time, add_dea, Ppersistence):
        self.fathers = fathers
        self.num_fathers = num_fathers
        self.type = typer
        self.children = []
        self.id = id
        self.table_distrb = []
        self.time = time
        self.additional_details = add_dea
        self.Ppersistence = Ppersistence

    def create_table_roots(self, p_flooding):
        if self.num_fathers ==0:
            self.table_distrb.append([True, p_flooding])
            self.table_distrb.append([False, 1-p_flooding])

    def create_node_table(self):
        leads_0 = ""
        for j in range (self.num_fathers):
            leads_0 += leads_0 + "0"
        for i in range(int(math.pow(self.num_fathers+1, 2))):
            string_num = "{0:b}".format(i)
            string_num = leads_0 + string_num
            string_num = string_num[:self.num_fathers+1]
            lst = []
            for t in range(len(string_num)):
                if string_num[t] == '0':
                    lst.append(True)
                else:
                    lst.append(False)
            if self.type == "e":
                if i == 0 or i == 1:
                    p = 1 - math.pow((1-(0.6/self.additional_details[0])), 2)
                    if i == 1:
                        p = 1 - p
                elif i == 2 or i == 3 or i == 4 or i == 5:
                    p = 0.6/self.additional_details[0]
                    if i == 3 or i == 5:
                        p = 1 - p
                elif i == 6 or i == 7:
                    p = 0.001
                    if i == 7:
                        p = 1 - p
            else:
                if i == 0 or i == 1:
                    p = self.Ppersistence
                    if i == 1:
                        p = 1 - p
                elif i == 2 or i == 3:
                    node_temp = self
                    while node_temp.num_fathers > 0:
                        node_temp = node_temp.fathers[0]
                    p = node_temp.table_distrb[0][1]
                    if i == 3:
                        p = 1 - p
            lst.append(p)
            self.table_distrb.append(lst)









