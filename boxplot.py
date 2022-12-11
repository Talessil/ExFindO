import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import csv

"""
data =  pd.read_csv('/home/tales/Downloads/ExFindO/results_until2019/result_all_time.csv', sep=";", header=0)
number_of_expertises = 14
re = np.empty(number_of_expertises, dtype=object)
re[0] = data['Memory'].sum()
re[1] = data['Performance'].sum()
re[2] = data['Security'].sum()
re[3] = data['ProjectManagement'].sum()
re[4] = data['CI'].sum()
re[5] = data['Testing'].sum()
re[6] = data['Updating'].sum()
re[7] = data['C++'].sum()
re[8] = data['Python'].sum()
re[9] = data['ES6+'].sum()
re[10] = data['NewFeature'].sum()
re[11] = data['CoreFeature'].sum()
re[12] = data['OperationalErrors'].sum()
re[13] = data['ProgrammerErrors'].sum()

print(re)

objects = ('Memory', 'Performance', 'Security', 'ProjectManagement', 'CI', 'Testing', 'Updating', 'C++', 'Python', 'ES6+', 'NewFeature', 'CoreFeature', 'OperationalErrors', 'ProgrammerErrors')
y_pos = np.arange(len(objects))

plt.bar(y_pos, re, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Weight')
plt.xlabel('Expertise')
plt.title('Total weight of each expertise')
plt.xticks(rotation=35)

plt.show()
"""




#core
updating_core = []
C_core = []
testing_core = []

with open('/home/tales/Downloads/ExFindO/results_until2019/result_core_time.csv', newline='\n') as csvfile:
    data = list(csv.reader(csvfile, delimiter=','))

updating_norm = 0
C_norm = 0
testing_norm = 0
#normalize
cont=0
for row in data:
    if cont != 0:
        if float(row[8]) > updating_norm:
            updating_norm = float(row[8])
        if float(row[9]) > C_norm:
            C_norm = float(row[9])
        if float(row[7]) > testing_norm:
            testing_norm = float(row[7])
    cont = cont + 1
cont=0
for row in data:
    if cont != 0:
        updating_core.append(float(row[8])/updating_norm)
        C_core.append(float(row[9])/C_norm)
        testing_core.append(float(row[7])/testing_norm)
    cont = cont + 1

updating_core = sorted(updating_core,reverse=True)
C_core = sorted(C_core,reverse=True)
testing_core = sorted(testing_core,reverse=True)

#no core
updating_nocore = []
C_nocore = []
testing_nocore = []

with open('/home/tales/Downloads/ExFindO/results_until2019/result_nocore_time.csv', newline='\n') as csvfile:
    data = list(csv.reader(csvfile, delimiter=','))


cont=0
for row in data:
    if cont > 0:
        updating_nocore.append(float(row[8])/updating_norm)
        C_nocore.append(float(row[9])/C_norm)
        testing_nocore.append(float(row[7])/testing_norm)
    cont = cont + 1

updating_nocore = sorted(updating_nocore,reverse=True)
C_nocore = sorted(C_nocore,reverse=True)
testing_nocore = sorted(testing_nocore,reverse=True)

updating_nocore = updating_nocore[:24]
C_nocore = C_nocore[:24]
testing_nocore = testing_nocore[:24]

#BOXPLOT
a = []
a.append(updating_core)
a.append(updating_nocore)
a.append(C_core)
a.append(C_nocore)
a.append(testing_core)
a.append(testing_nocore)
#print(a)

box_plot_data=[updating_core,updating_nocore,C_core,C_nocore,testing_core,testing_nocore]
plt.boxplot(box_plot_data,patch_artist=False,labels=['Updating_core','Updating_non-core','C++_core','C++_non-core','Testing_core','Testing_non-core'])
plt.xticks(rotation=20)
plt.title('Cores and non-cores\' expertise weight')
plt.xlabel('Expertise')
plt.ylabel('Expertise Weight')
plt.show() 
