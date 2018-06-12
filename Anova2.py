# Anova2 is a project developed for the biologist students of the HAN to
# do a QTL analysis without having to do all the anova calculations by hand.
# 
# Author: Rogier Stegeman
# Created: 25/04/2018
# Last modified: 09/06/2018
# Known bugs:
#   None

# Imports
# Importing the anova one-way function from the scipy package
# Importing tkinter for the file opener
from scipy.stats import f_oneway
import tkinter as tk
from tkinter import filedialog


# main asks the user for the two necessary files and calls the other functions
def main():
    root = tk.Tk()
    root.withdraw()
    qua_file_path = filedialog.askopenfilename(title="Select Qua File", filetypes= (("Qua files", "*.qua"),
                                                                                    ("All files", "*.*")))
    loc_file_path = filedialog.askopenfilename(title="Select Loc File", filetypes= (("Loc files", "*.loc"),
                                                                                    ("All files", "*.*")))
    # Read the 2 files and perform calculations
    quaData = openQuaData(qua_file_path)
    results = openLocData(quaData, loc_file_path)
    # Write results to a file
    writeFile(results)
    print("="*30, "\nThe results have been written to AnovaData.csv")


# Opens and parses the Qua Data
def openQuaData(file_path):
    quaData = []
    try:
        file = open(file_path, 'r')
        preQuaData = file.readlines()
        try:
            for i in range(8):
                preQuaData.pop(0)
            for item in preQuaData:
                quaData.append(item.split("\t")[1].strip("\n"))
            return quaData
        except IndexError as IE:
            print("ERROR: {}\nIndex was out of range. Please check if your files are formatted correctly.\n"
                  "You also might've switched up the two files.".format(IE))
            quit()
    except FileNotFoundError as FNFE:
        print("ERROR: {} | While searching for Qua data\nPlease select the files and open them. Don't close the file opener screen. "
              "If all else fails please check the validity of your file.".format(FNFE))
        quit()



# Opens and parses the Loc Data
def openLocData(quaData, loc_file_path):
    locData = []
    try:
        file = open(loc_file_path, 'r')
        data = ""
        lines = file.readlines()
        for line in lines:
            if line.__contains__("(a,b)"):
                # Retrieving Anova one-way results
                F, p = checkMarker(data, quaData)
                if p < 0.05:
                    locData.append([name, F, p])
                temp = line.split("(a,b)")[0]
                name = temp[:len(temp)-1]
                data = ""
            else:
                for mark in line:
                    if mark == "a" or mark == "b":
                        data += mark
        print(">>>", locData)
    except FileNotFoundError as FNFE:
        print("ERROR: {} | While searching for Loc data\nPlease select the files and open them. "
              "Don't close the file opener screen. "
              "If all else fails please check the validity of your file.".format(FNFE))
    return locData


# Divides the data over two lists. One list with plants that do contain the marker, one list
# with plants that don't contain the marker.
def checkMarker(data, quaData):
    listA = []
    listB = []
    for i in range(len(data)):
        try:
            if quaData[i] != "-":
                if data[i] == "a":
                    listA.append(float(quaData[i]))
                elif data[i] == "b":
                    listB.append(float(quaData[i]))
                else:
                    print("ERROR")
        except IndexError:
            print("\n>>>=====================<<<\nIndex Error at marker:",i,"\nmarker length", len(data),
                  "\nqua list length:", len(quaData),
                  "\nMarker list:", data, "\nQua list:", data, "\n>>>=====================<<<\n\n")
    print("A:", listA, "\n", listB)
    F, p = calculateAnova(listA, listB)
    return F, p


# Uses the two lists to calculate F and p using Anova one-way from scipy.
# If the resulting p < 0.05 the result is saved
def calculateAnova(listA, listB):
    F, p = f_oneway(listB, listA)
    print("F:", F)
    print("p:", p)

    return F, p


# Write the results to a csv file for MS Excel compatibility.
def writeFile(results):
    try:
        file = open("AnovaData.csv","w")
        file.write("Marker,F,p")
        for list in results:
            file.write("\n{},{},{}".format(list[0], list[1], list[2]))
        file.close()
    except PermissionError as pe:
        print("\nERROR: {}\nPlease close any program using the file AnovaData.csv".format(pe))


if __name__ == '__main__':
    main()
