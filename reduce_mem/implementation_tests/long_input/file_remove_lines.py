
"""
Load a file up and only keep 1 in 'divide' number of lines.

"""
divide = 20
file_in = 'java_par_site.csv'
file_out = 'java_par_site_small.csv'

# Used in testing
if False:
    start = 1 
    end = 81  # 1, 21, 41, 61, 81
    thelist = range(start,end)
    fout = open(file_in,'w')
    for item in thelist:
        fout.write("%s\n" % item)
        fout.close()


# read the data file in as a list
fin = open(file_in, "r" )
data_list = fin.readlines()
fin.close()

 

indexes = range(0,len(data_list), divide)
reduced_list = [data_list[i] for i in indexes]

 
# write the changed data (list) to a file
fout = open(file_out, "w")
fout.writelines(reduced_list)
fout.close()
