def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


import xlrd
import xlsxwriter

#L=Matrix = [[0 for x in range(228226)] for x in range(15980)] 
L=Matrix = [[0 for x in range(100)] for x in range(15980)]

file_location = "C:\\Users\\mitadm\\Desktop\\levenshtein.xlsx"
workbook=xlrd.open_workbook(file_location)
sheet=workbook.sheet_by_index(0)
for i in range(1,15980):
    for j in range(100,200):
        L[i-1][j-100]=levenshtein(sheet.cell_value(i,0),sheet.cell_value(j,1))
    if (i%100==0):
        print (i)

from operator import itemgetter
M=[0]*15980
for k in range(15980):
    M[k]=min(L[k][:99])
index1, element = min(enumerate(M[:15979]), key=itemgetter(1))
index2, element = min(enumerate(L[index1][:99]), key=itemgetter(1))

levenshtein(sheet.cell_value(index1+1,0),sheet.cell_value(index2+100,1))


for i in range(1,15980):
    for j in range(5000,8000):
        a=levenshtein(str(sheet.cell_value(i,0)),str(sheet.cell_value(j,1)))
        if (a<=3):
            L.append((i,j,a))
    if (i%100==0):
	print(i)
