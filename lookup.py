"""
Pinpoints projection value for desired capture value
"""
import csv
import numpy as np

#automate crossection > plot

def open_csv():
    results = []
    with open("plot.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
        for row in reader: # each row is a list
            results.append(row)
    return np.asarray(results)

def lookup(table, desired_captured_intensity):#try dci for odd range, evenrange, and none

    if desired_captured_intensity<=table[-1][1]:
        x = np.where(table[:,1] == desired_captured_intensity)
        y = np.where(table[:,1] == 256)

        if len(x[0])==0:
            while len(x[0])==0 and len(y[0])==0:
                x = np.where(table[:,1] == desired_captured_intensity-1)
                y = np.where(table[:,1] == desired_captured_intensity+1)

            if len(x[0])<len(y[0]):
                x=y

        captured_loc=x[0][int(len(x[0])/2)]
        projected_loc=table[captured_loc][0]

    else:
        projected_loc=table[-1][0]

    return int(projected_loc)

if __name__ == "__main__":
    table=open_csv()
    desired_captured_intensity=input("Desired Capture Intensity: ")
    projected_loc=lookup(table, int(desired_captured_intensity))
    print("Corresponding Projected Intensity: " + str(projected_loc))
