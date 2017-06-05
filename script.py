import re
import csv


def create_graphml(file_name):
    node_id = 1
    id_node_map = {}
    edge_attr = {}
    node_attr = {}
    f = open("categories.csv", "r")
    csv_iter = csv.reader(f)
    dic_categories = {}
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_category = dict(zip(header[:-1] + ['labelV'], row[:-1] + ['category']))
            dic_categories[m[0]] = dic_category
            print((m[0]))
            id_node_map["cate%s"%(row[0])] = node_id
            node_id+=1

    f = open("customers.csv", "r")
    csv_iter = csv.reader(f)
    dic_customers = {}
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_customer = dict(zip(header + ['labelV'], row + ['customer']))
            dic_customers[m[0]] = dic_customer
            id_node_map["cust%s"%(row[0])] = node_id
            node_id+=1


    f = open("employees.csv", "r")
    csv_iter = csv.reader(f)
    dic_employees = {}
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_employee = dict(zip(header[:-2] + [header[-1], 'labelV'], row[:-2] + [row[-1], 'employee']))
            dic_employees[m[0]] = dic_employee
            id_node_map["empl%s"%(row[0])] = node_id
            node_id+=1


    f = open("orders.csv", "r")
    csv_iter = csv.reader(f)
    dic_orders = {}
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_order = dict(zip([header[0]] + header[3:6] + header[7:] + ['labelV'], [row[0]] + row[3:6] + row[7:] + ['order']))
            dic_orders[m[0]] = dic_order
            id_node_map["orde%s"%(row[0])] = node_id
            node_id+=1

    f = open("products.csv", "r")
    csv_iter = csv.reader(f)
    dic_products = {}
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_product = dict(zip(header[:2] + header[4:] + ['labelV'], row[:2] + row[4:] + ['product']))
            dic_products[m[0]] = dic_product
            print(dic_product)
            id_node_map["prod%s"%(row[0])] = node_id
            node_id+=1


    f = open("regions.csv", "r")
    csv_iter = csv.reader(f)
    dic_regions = {}
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_item = dict(zip(header + ['labelV'], row + ['region']))
            dic_regions[m[0]] = dic_item
            id_node_map["regi%s"%(row[0])] = node_id
            node_id+=1

    f = open("shippers.csv", "r")
    csv_iter = csv.reader(f)
    dic_shippers = {}
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_shipper = dict(zip(header + ['labelV'], row + ['shipper']))
            dic_shippers[m[0]] = dic_shipper
            id_node_map["ship%s"%(row[0])] = node_id
            node_id+=1

    f = open("suppliers.csv", "r")
    csv_iter = csv.reader(f)
    dic_suppliers = {}
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_item = dict(zip(header + ['labelV'], row + ['suppplier']))
            dic_suppliers[m[0]] = dic_item
            id_node_map["supp%s"%(row[0])] = node_id
            node_id+=1

    f = open("territories.csv", "r")
    csv_iter = csv.reader(f)
    dic_territories = {}
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_territory = dict(zip(header + ['labelV'], row + ['territory']))
            dic_territories[m[0]] = dic_territory
            id_node_map["terr%s"%(row[0])] = node_id
            node_id+=1
    print(node_id)
    
    l = [dic_territories, dic_shippers, dic_suppliers, dic_regions, dic_orders, dic_employees, dic_categories, dic_customers, dic_products]
    m = ['terr', 'ship', 'supp', 'regi', 'orde', 'empl', 'cate', 'cust', 'prod']
    
    graph_file = open(file_name, "w")
    graph_file.write("""<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
        http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n""")

    write_attrs(graph_file)
    graph_file.write("""\t<graph id="G" edgedefault="directed">\n""")
    #Writing Nodes to File
    for i in range(len(l)):
        each_dic = l[i]
        first_four = m[i]
        for each in each_dic:
            graph_file.write(create_format(each_dic[each], id_node_map[first_four+each],node_attr))

    #Creating Edges
    dic_employees_2 = {}
    f = open("employees.csv", "r")
    csv_iter = csv.reader(f)
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            for each in row:
                header.append(each)
            first_row = False
        else:
            m = row
            dic_employee = dict(zip(header, row))
            dic_employees_2[m[0]] = dic_employee

    edges = []
    dic_edge_attributes = {}
    for each in dic_employees_2:
        if dic_employees_2[each]['reportsTo']!='NULL':
            edges.append((node_id, id_node_map['empl'+each],id_node_map['empl' + dic_employees_2[each]['reportsTo']]))
            dic_edge_attributes[node_id] = {'labelE': 'reportsTo'}
            node_id+=1


    f = open("employee-territories.csv", "r")
    csv_iter = csv.reader(f)
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            first_row = False
        else:
            edges.append((node_id, id_node_map['empl'+row[0]],id_node_map['terr' + row[1]]))
            dic_edge_attributes[node_id] = {'labelE': 'assignedTerritory'}
            node_id+=1
    
    f = open("order-details.csv", "r")
    csv_iter = csv.reader(f)
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            first_row = False
        else:
            edges.append((node_id, id_node_map['orde'+row[0]],id_node_map['prod' + row[1]]))
            dic_edge_attributes[node_id] = {'labelE': 'has', 'unitPrice': row[2], 'quantity':row[3], 'discount':row[4]}
            node_id+=1
    
    f = open("products.csv", "r")
    csv_iter = csv.reader(f)
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            first_row = False
        else:
            m = row
            edges.append((node_id, id_node_map['prod'+row[0]],id_node_map['supp' + row[2]]))
            dic_edge_attributes[node_id] = {'labelE': 'suppliedBy'}
            node_id+=1
            edges.append((node_id, id_node_map['prod'+row[0]],id_node_map['cate' + row[3]]))
            dic_edge_attributes[node_id] = {'labelE': 'hasCategory'}
            node_id+=1

    f = open("orders.csv", "r")
    csv_iter = csv.reader(f)
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            first_row = False
        else:
            m = row
            edges.append((node_id, id_node_map['orde'+row[0]],id_node_map['cust' + row[1]]))
            dic_edge_attributes[node_id] = {'labelE': 'orderedBy'}
            node_id+=1
            edges.append((node_id, id_node_map['orde'+row[0]],id_node_map['empl' + row[2]]))
            dic_edge_attributes[node_id] = {'labelE': 'takenBy'}
            node_id+=1
            edges.append((node_id, id_node_map['orde'+row[0]],id_node_map['ship' + row[6]]))
            dic_edge_attributes[node_id] = {'labelE': 'shippedBy'}
            node_id+=1

    f = open("territories.csv", "r")
    csv_iter = csv.reader(f)
    first_row = True
    header = []
    for row in csv_iter:
        if first_row:
            first_row = False
        else:
            m = row
            edges.append((node_id, id_node_map['terr'+row[0]],id_node_map['regi' + row[2]]))
            dic_edge_attributes[node_id] = {'labelE': 'hasRegion'}
            node_id+=1
    
    for i in range(len(edges)):
        graph_file.write(create_format_edge(dic_edge_attributes[edges[i][0]], edges[i], edge_attr))     
    
    graph_file.write("\t</graph>\n")
    graph_file.write("</graphml>")

def create_format(node, _id, node_attr):
    s = '\t\t<node id="%d">\n' % (_id)
    for each in node:
        if each not in node_attr:
            node_attr[each] = "string|" + node[each]
#        ukey=each.decode("utf-8")
 #       asciikey=ukey.encode("ascii","ignore")
  #      uvalue=node[each].decode("utf-8")
   #     asciivalue=uvalue.encode("ascii","ignore")
        asciikey = re.sub(r'[^\x00-\x7F]+',' ', each)
        asciikey = asciikey.replace("&", "amp;")
        asciivalue = re.sub(r'[^\x00-\x7F]+',' ', node[each])
        asciivalue = asciivalue.replace("&", "amp;")
        s = s + '\t\t\t<data key="%s">%s</data>\n' %(asciikey, asciivalue)
    s = s + "\t\t</node>\n"
    return s

def create_format_edge(details, tup,edge_attr):
    s = '\t\t<edge id="%d" source="%d" target="%d" label="%s">\n' % (tup[0], tup[1], tup[2], details['labelE'])
    for each in details:
        if each not in edge_attr:
            edge_attr[each] = "string" + "|" + details[each]
        if each != "label":        
            s = s + '\t\t\t<data key="%s">%s</data>\n' %(each, details[each])
    s = s + "\t\t</edge>\n"
    return s

def write_attrs(filehandler):
    f = open("edge_attr", "r").readlines()
    for each in f:
        m = each.strip().split(" ")
        filehandler.write("""\t<key id ="%s" for="edge" attr.name="%s" attr.type="%s"/>\n"""%(m[0], m[0], m[1]))
    f = open("node_attr", "r").readlines()
    for each in f:
        m = each.strip().split(" ")
        filehandler.write("""\t<key id ="%s" for="node" attr.name="%s" attr.type="%s"/>\n"""%(m[0], m[0], m[1]))

if __name__=='__main__':
    create_graphml("northwind.graphml")
