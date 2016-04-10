import csv
import os.path

def csv2list(filename, skip_first_line=False):
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        result = list(reader)
        
    if not skip_first_line:
        return result
    
    return result[1:]



def csv2list_or_empty(filename, skip_first_line=False):
    if not os.path.isfile(filename):
        return []
    
    return csv2list(filename)




def list2csv(filename, data, headers=None):
    
    append_headers = False
    if headers and not os.path.isfile(filename):
        append_headers = True
    
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file)
        
        if append_headers:
            writer.writerow(headers)
        
        writer.writerows(data)
        
        
        
def append_row_to_csv_file(filename, data, headers=None):
    append_headers = False
    if headers and not os.path.isfile(filename):
        append_headers = True
    
    with open(filename, "a") as csv_file:
        writer = csv.writer(csv_file)
        
        if append_headers:
            writer.writerow(headers)
        
        writer.writerow(data)
        
        
        
def get_elements_from_tuples(tuples, num=0):
    
    def map_tuples(element):
        return element[num]
    
    return map(map_tuples, tuples)
        
    
    
def get_tuple_row_index_of(row, source, force_length=False):
    
    for i in range(len(source)):
        
        source_i = source[i] if not force_length else source[i][:len(row)]
        
        if len(source_i) != len(row):
            continue
        
        if all(a==b for a, b in zip(source_i, row)):
            return i

    return -1
            
            
        
    
    







