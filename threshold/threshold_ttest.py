import pandas as pd
from threshold_return_path import path
from scipy.stats import ttest_ind
import numpy as np

def check_for_statistical_significance():
    def check_files(file_path1, file_path2):
        with open(file_path1, 'r') as file1:
            header_row1 = file1.readline().strip().split('\t')
            row_count1 = sum(1 for line in file1 if line.strip())
        with open(file_path2, 'r') as file2:
            header_row2 = file2.readline().strip().split('\t')
            row_count2 = sum(1 for line in file2 if line.strip())

            if header_row1 == ['Nth Gene Included', 'Incremental Saturation', 'Overall Saturation'] and header_row2 == ['Nth Gene Included', 'Incremental Saturation', 'Overall Saturation']:
                if row_count1 == row_count2:
                    return True
                else:
                    return False
            else:
                return False

    if check_files(path+"stat1.txt",path+"stat2.txt") == True:
        def extract_columns(file_path, column):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                sat_column = [float(line.strip().split('\t')[column]) for line in lines[1:]]
                return sat_column
                
        inc1 = extract_columns(path+"stat1.txt",1)
        ove1 = extract_columns(path+"stat1.txt",2)

        inc2 = extract_columns(path+"stat2.txt",1)
        ove2 = extract_columns(path+"stat2.txt",2)

        def run_t_test(dataA, dataB, type_of_sat):

            data = {
                'Data A': dataA,
                'Data B': dataB
            }

            df = pd.DataFrame(data)

            t_stat, p_value = ttest_ind(df['Data A'], df['Data B'])

            n = len(df) 
            dof = n*2 - 2  
            mean1 = df['Data A'].mean()
            mean2 = df['Data B'].mean()
            sd1 = np.std(df['Data A'], ddof=1)
            sd2 = np.std(df['Data B'], ddof=1)
            sp = np.sqrt(((dof/2) * (sd1**2) + (dof/2) * (sd2**2)) / dof)
            se = sp*np.sqrt(2/n)


            
            if p_value < 0.05:
                interpretation = f"There is a statistically significant difference between the datasets."
            else:
                interpretation = f"There is not a statistically significant difference between the datasets."

            output = [type_of_sat,n, dof, mean1, mean2, sd1, sd2, sp, se, t_stat, p_value,interpretation]
            return output

        return run_t_test(inc1, inc2,"Incremental Saturation"), run_t_test(ove1, ove2,"Overall Saturation")
    else: 
        return "Error"


