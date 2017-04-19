import bs4,re
node_id_map = {}
node_details_map = {}
all_edges = []
edge_attributes = {}

def foo2(bs_element, ttt):
    z = bs_element.findChildren()
    model = {}
    for each in z:
        if each.parent != bs_element:
            continue
        try:
            if len(each.findChildren()) == 0:
                try:
                    tttttt = each["rdf:resource"]
                except:
                    model[each.name.split(":")[-1]] = each.text
            zzz = each["rdf:datatype"]                
            model[each.name.split(":")[-1]] = each.text
        except Exception as e:
            pass
    if len(model)!=0:
        model[ttt.split("/")[-1].split("-")[0]+"Id"] = ttt.split("/")[-1].split("-")[1] 
        return model
        
def foo(filename, write_filename = "made_from_rdf.graphml"):
    l = []
    dic = {}
    dic_2 = {}
    soup = bs4.BeautifulSoup(open(filename, "r").read())
    node_id = 0
    dic_orders = {}
    dic_employees = {}
    dic_suppliers = {}
    dic_products = {}
    dic_shippers = {}

    for each in soup.findChildren():
        if each.name == "model:orderdetail":
            continue        
        try:
            ttt = (each['rdf:about'])
            model = foo2(each, ttt)
            if model is not None:
                node_id_map[ttt] = node_id
                node_details_map[ttt] = model
                node_id+=1
        except Exception as e:
            pass
    

    for each in soup.findChildren():
    #Employee reports to employee
        if each.name == "model:employee":
            try:
                ttt = each['rdf:about']
                z = each.find('model:reportsto')
                if len(z.findChildren()) == 0:
                    all_edges.append((ttt, "reportsTo", z["rdf:resource"]))
                else:
                    pp = z.find("model:employee")
                    all_edges.append((ttt, "reportsTo", pp["rdf:about"]))
            except Exception as e:
                pass        


    #Territory assigned to employee
            try:
                ttt = each['rdf:about']
                z = each.find_all('model:territory')
                for each_terr in z:
                    try:
                        #print(each.parent.parent["rdf:about"])
                        if each_terr.parent.parent["rdf:about"] == ttt:
                            all_edges.append((ttt, "assignedTerritory", each_terr["rdf:about"]))
                    except Exception as e:
                        pass
            except Exception as e:
                pass        

    print(len(all_edges))

    for each in soup.find_all("model:product"):
    #Product Suppliers

        try:
            ttt = each["rdf:about"]
            suppliers = each.find_all("model:supplier")
            for each_suppl in suppliers:
                try:
                    mmm = each_suppl["rdf:about"]
                    all_edges.append((mmm, "supplies", ttt))
                except Exception as e:
                    pass        
                try:
                    mmm = each_suppl["rdf:resource"]
                    all_edges.append((mmm, "supplies", ttt))
                except Exception as e:
                    pass        

        except Exception as e:
            pass    

    #Product Category
        try:
            ttt = each["rdf:about"]
            category = each.find_all("model:category")
            for each_cat in category:
                try:
                    mmm = each_cat["rdf:about"]
                    all_edges.append((ttt, "belongsTo", mmm))
                except Exception as e:
                    pass        
                try:
                    mmm = each_cat["rdf:resource"]
                    all_edges.append((ttt, "belongsTo", mmm))
                except Exception as e:
                    pass        

        except Exception as e:
            pass    


    print(len(all_edges))

    count_c = 0
    count_e = 0
    count_s = 0
    for each in soup.find_all("model:order"):
    #Order Customers
        try:
            ttt = each["rdf:about"]
            customers = each.find_all("model:customer")
            
            for each_cust in customers:
                try:
                    mmm = each_cust["rdf:about"]
                    all_edges.append((mmm, "ordered", ttt))
                    count_c+=1    
                except Exception as e:
                    pass        
                try:
                    mmm = each_cust["rdf:resource"]
                    all_edges.append((mmm, "ordered", ttt))
                    count_c+=1
                except Exception as e:
                    pass        

        except Exception as e:
            pass    

    #Order Employee
        try:
            ttt = each["rdf:about"]
            employees = each.find_all("model:employee")
            for each_emp in employees:
                try:
                    mmm = each_emp["rdf:about"]
                    all_edges.append((mmm, "took", ttt))
                    count_e+=1
                    break    
                except Exception as e:
                    pass        
                try:
                    mmm = each_emp["rdf:resource"]
                    all_edges.append((mmm, "took", ttt))
                    count_e+=1    
                    break
                except Exception as e:
                    pass        

        except Exception as e:
            pass    

    #Order Shipper
        try:
            ttt = each["rdf:about"]
            shipper = each.find_all("model:shipvia")
            mmm = None            
            try:
                mmm = shipper[0]["rdf:resource"]
            except:
                mmm = shipper[0].find_all("model:shipper")[0]["rdf:about"]
                
            all_edges.append((mmm, "shipped", ttt))
            count_s+=1    
   
        except Exception as e:
            pass

    print(len(all_edges))

    for each in soup.find_all("model:territory"):
    #Territory Region
        try:
            ttt = each["rdf:about"]
            regions = each.find_all("model:region")
            
            for each_regi in regions:
                try:
                    mmm = each_regi["rdf:about"]
                    all_edges.append((mmm, "belongsTo", ttt))
                except Exception as e:
                    pass        
                try:
                    mmm = each_regi["rdf:resource"]

                    all_edges.append((mmm, "belongsTo", ttt))
                except Exception as e:
                    pass        

        except Exception as e:
            pass    

    for each in soup.find_all("model:orderdetail"):
    #Territory Region
        order = each.find_all("model:order")
        product = each.find_all("model:product")
        orderid = None
        productid = None
        discount = "0"
        qty = "0"
        unit_price = "0"

    

        try:
            discount = each.find("model:discount").text
        except:
            pass  

        try:
            qty = each.find("model:quantity").text
        except:
            pass    

        try:
            unit_price = each.find("model:unitprice").text        
        except:
            pass    

        if len(order) == 1:
            orderid = order[0]["rdf:resource"]
        else:
            for each_order in order:
                try:
                    orderid = each_order["rdf:about"]
                except:
                    pass


        if len(product)==1:
            productid = product[0]["rdf:resource"]
        else:
            for each_prod in product:
                try:
                    productid = each_prod["rdf:about"]
                except:
                    pass

        if orderid is None or productid is None:
            continue    

        all_edges.append((orderid, "has", productid))
        edge_attributes[(orderid, "has", productid)] = { "discount" : discount, "quantity" : qty, "unitPrice" :unit_price }
        print(len(all_edges))
    
    file_ = open(write_filename, "w")
    write_initial(file_)    
    write_to_file(file_, node_id)
    write_final(file_)
    file_.close()
    #print(len(node_id_map))

def write_initial(filehandler):
    filehandler.write("""<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
        http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n""")
    f = open("edge_attr", "r").readlines()
    for each in f:
        m = each.strip().split(" ")
        filehandler.write("""\t<key id ="%s" for="edge" attr.name="%s" attr.type="%s"/>\n"""%(m[0], m[0], m[1]))
    f = open("node_attr", "r").readlines()
    for each in f:
        m = each.strip().split(" ")
        filehandler.write("""\t<key id ="%s" for="node" attr.name="%s" attr.type="%s"/>\n"""%(m[0], m[0], m[1]))
    filehandler.write("""\t<graph id="G" edgedefault="directed">\n""")

def write_final(filehandler):
    filehandler.write("\t</graph>\n")
    filehandler.write("</graphml>")

def create_format(node, _id):
    s = '\t\t<node id="%d">\n' % (_id)
    for each in node:
        asciikey = re.sub(r'[^\x00-\x7F]+',' ', each)
        asciikey = asciikey.replace("&", "amp;")
        asciivalue = re.sub(r'[^\x00-\x7F]+',' ', node[each])
        asciivalue = asciivalue.replace("&", "amp;")
        s = s + '\t\t\t<data key="%s">%s</data>\n' %(asciikey, asciivalue)
    s = s + "\t\t</node>\n"
    return s

def create_format_edges(node, edge_id, node_attr = None):
    print(node)
    destination = node_id_map[node[2]]
    source = node_id_map[node[0]]

    label = node[1]
    s = '\t\t<edge id="%d" source="%d" target="%d" label="%s">\n' % (edge_id, source, destination, label)
    if node_attr is not None:    
        for each in node_attr:
            if each != "label":        
                s = s + '\t\t\t<data key="%s">%s</data>\n' %(each, node_attr[each])
    s = s + '\t\t</edge>'
    return s

def write_to_file(filehandler, node_id):
    for each in node_details_map:
        filehandler.write(create_format(node_details_map[each], node_id_map[each]))
    for each in all_edges:
        if each in edge_attributes:
            filehandler.write(create_format_edges(each, node_id, edge_attributes[each]))
        else:
            filehandler.write(create_format_edges(each, node_id))
        node_id+=1

        
if __name__ == "__main__":
    foo("northwind.data.v1.rdf")


