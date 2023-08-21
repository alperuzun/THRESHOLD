from collections import Counter
import numpy as np
import ujson
from threshold_return_path import path as path1

path = path1

global data



def top50(top):
    sorted_list = dict(sorted(toplist.items(), key=lambda item: item[1], reverse=True))

    top50_array = list(sorted_list.keys())

    text = ""
    for i in range(0,top):
        text = text + f"{i+1}. {top50_array[i]}, {toplist[top50_array[i]]}\n"
    return text

def go(elements, mode, factor1):
    global data
    global factor
    with open(path + 'ranks.json', 'r') as file:
        data = ujson.load(file)
        factor = factor1
    
    incremental_saturation(elements, "all")
    overall_saturation(elements, "all")
    
def occurrence(limit, lst, target):

    lst.extend(target)


    global item_counts
    global toplist

    item_counts = Counter(lst)

    toplist = Counter(lst)


    total_multiplicity = 0

    for item in target:
        if item_counts[item] >= limit:
            total_multiplicity = total_multiplicity + 1 
            item_counts[item] = item_counts[item] - 1
    
    return total_multiplicity

def multiplicity(limit, lst):
    unique, indices, counts = np.unique(lst, return_index=True, return_counts=True)
    total_multiplicity = 0
    for count in counts:
        if count >= limit:
            total_multiplicity += (count - limit + 1)

    return total_multiplicity
    
def calculate_incremental_saturation(data, argument):
    up_to_nth_genes = []
    nth_genes = []
        
    for item in data:
        nth_genes.append(item[argument - 1][1])
        for i in range(argument - 1):
            up_to_nth_genes.append(item[i][1])
    
    value = occurrence(factor, up_to_nth_genes, nth_genes) / len(nth_genes)

    return value

def incremental_saturation(rows, mode):   
    if mode == "all":
        value_list = ["Incremental Saturation"]
        
        for n in range(1, rows + 1):
            saturation = calculate_incremental_saturation(data, n)
            value_list.append(saturation)

            new_lines = []

        for i in range(len(value_list)):
            if i == 0:
                line = "Nth Gene Included"
            else:
                line = i

            new_line = f"{line}\t{value_list[i]}\n"
            new_lines.append(new_line)

        with open(path + 'graph.txt', 'w') as file:
            file.writelines(new_lines)
        
        return value_list
    
    if mode == "single":
        return calculate_incremental_saturation(data, rows)
    
    if mode == "find_threshold":
        desired = rows
        if 0 <= desired <= 1:
            n = 1
            reached = False
            check = 0

            while not reached:
                value = calculate_incremental_saturation(data, n)
                if value >= desired and check < 2:
                    check += 1
                elif value >= desired and check == 2:
                    reached = True
                    return n - 2
                elif value < desired and check > 0:
                    check = 0
                else:
                    n += 1
        else:
            return "invalid"

def calculate_overall_saturation(data, argument):
    up_to_nth_genes = []
    for i in range(argument):
        for item in data:
            up_to_nth_genes.append(item[i][1])
    saturation = multiplicity(factor, up_to_nth_genes) / len(up_to_nth_genes)

    return saturation

def overall_saturation(rows, mode):
    if mode == "all":
        saturation_list = ["Overall Saturation"]
        
        for n in range(1, rows + 1):
            saturation = calculate_overall_saturation(data, n)
            saturation_list.append(saturation)
        
        with open(path + 'graph.txt', 'r') as file:
            lines = file.readlines()
        
        new_lines = []
        
        for i in range(len(lines)):
            line = lines[i].strip()
            new_line = f"{line}\t{saturation_list[i]}\n"
            new_lines.append(new_line)
        
        with open(path + 'graph.txt', 'w') as file:
            file.writelines(new_lines)
        
        return saturation_list
    
    if mode == "single":
        return calculate_overall_saturation(data, rows)
    
    if mode == "find_threshold":
        desired = rows
        if 0 <= desired <= 1:
            reached = False
            i = 0
            up_to_nth_genes = []
            while not reached:
                for item in data:
                    up_to_nth_genes.append(item[i][1])
                saturation = multiplicity(factor, up_to_nth_genes) / len(up_to_nth_genes)
                if saturation >= desired:
                    reached = True
                    return i + 1
                else:
                    i += 1
        else:
            return "invalid"