import csv
import ujson
from threshold_return_path import path as path1

path = path1

def rank(reverseTF):
    data = []
    with open(path + 'cleaned_data.txt', 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        headers = next(reader)
        for line in reader:
            data.append(line)  

    num_columns = len(headers)

    def highly(column_index):
        ranking = []
        for row in data: 
            if row[0] != "Hugo_Symbol" and row[column_index] != "NA":
                ranking.append((float(row[column_index]), row[0]))
        ranking.sort(reverse=reverseTF)
        return ranking

    ranks = [highly(i) for i in range(2, num_columns)] 
    with open(path + "ranks.json", 'w') as file:
        ujson.dump(ranks, file)

def max_columns():
    with open(path + 'cleaned_data.txt', 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        num_columns = len(next(reader)) 
        return num_columns
    


    