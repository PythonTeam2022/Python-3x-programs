from statistics import median
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo
from sklearn.metrics import confusion_matrix
import tkinter as tk
from turtle import title
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import tksheet

    ### Manolis ###
def loadDataset():
    colHeaders = ['id', 'diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean',
        'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean',
        'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
        'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
        'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
        'fractal_dimension_se', 'radius_worst', 'texture_worst',
        'perimeter_worst', 'area_worst', 'smoothness_worst',
        'compactness_worst', 'concavity_worst', 'concave points_worst',
        'symmetry_worst', 'fractal_dimension_worst']

    # Εισαγωγή dataset σε pandas dataframe
    data = pd.read_table('C:/Users/user/Desktop/ΕΑΠ/ΠΛΗΠΡΟ/Project/wdbc.data', sep=',', names=colHeaders)


### Isaak ###
    # Ψάχνουμε για τον αριθμό των 80% των εγγραφών
    num = int(len(data) * 0.8)
    # 80% Δεδομένα εκπαίδευσης
    train = data[:num]
    # 20% Δεδομένα δοκιμών
    test = data[num:]
    print("Data:", len(data), ", Train:", len(train), ", Test:", len(test))
    return data



### Isaak ###
# συνάρτηση datasetStatistics
def datasetStatistics(dataset):
    # μετατροπή της στήλης diagnosis σε binary (0 = benign - B, 1 = malign - M)
    ord_enc = OrdinalEncoder()
    dataset['diagnosis'] = ord_enc.fit_transform(dataset[['diagnosis']]).astype(int)

    # min value
    minValue = dataset["diagnosis"].min()
    # max value
    maxValue = dataset["diagnosis"].max()
    # Αριθμητικός Μέσος
    meanValue = dataset["diagnosis"].mean()
    # μέσος όρος
    medianValue = dataset["diagnosis"].median()
    # τυπική απόκλιση
    stdValue = dataset["diagnosis"].std()
    # variance
    varValue = dataset["diagnosis"].var()
    # διακύμανση του δείγματος
    return minValue, maxValue, meanValue, medianValue, stdValue, varValue

### Manolis ###
def runLogisticRegression(dataset):
    # δημιουργία διανύσματος
    y = dataset.diagnosis.values

    # αφαίρεση της στήλης diagnosis από τις μεταβλητές. Axis = 1 για διαβάζει τα στοιχειά κατά μήκος
    x_data = dataset.drop("diagnosis", axis=1)

    # normalise with min - max normalisation
    x = (x_data - np.min(x_data)) / (np.max(x_data) - np.min(x_data))

    # split train / test set
    x_train, x_test, y_train, y_test = train_test_split(x, y)

    # fit LogisticRegression model
    lr = LogisticRegression(max_iter=200)
    lr.fit(x_train, y_train)
    result = "our accuracy is\n:{}".format(lr.score(x_test, y_test))
    return result


### Manolis ###
def generateBarplot(dataset):
    ax = sns.countplot(dataset['diagnosis'], label="Count")
    fig = ax.get_figure()
    fig.savefig("C:/Users/user/Desktop/ΕΑΠ/ΠΛΗΠΡΟ/Project/barplot.png")


### Manolis ###
# Δημιουργία κουμπιού για να γίνει load το dataset σε pandas dataframe
root = tk.Tk()
root.geometry('1000x800')
root.configure(bg='#A877BA')
root.title('Μοντέλο Πρόβλεψης Κασσάνδρα')
#root.resizable(False, False)
#   frames
frameTitle = tk.Frame(root)
frameTitle.place(anchor='n', width=900, height=200)
frameTitle.pack(side='top')
lblTitle = tk.Label(frameTitle, text="Μοντέλο Πρόβλεψης Διάγνωσης καρκίνου του μαστού", font='Times 25')
lblTitle.place(anchor="n", width=180, height=600)
lblTitle.pack(side="top")

frameConsole = tk.Frame(root)
frameConsole.place(anchor='w')
frameConsole.pack(side='left', fill='both')

### Manolis ###
# Δημιουργία κουμπιού για να εμφανίσει statistics

def importButtonFunction():
    data = loadDataset()
    messagebox.showinfo('Success!', 'Finished importing the breast cancer dataset\nwith ' + str(len(data)) +
                        ' rows \nand ' + str(len(data.columns)) + ' columns!')
    cnvInsert.create_text(300, 300, text=data, justify='left')
    return data

### ANTONIOU ####
frameShow = tk.Frame(root)
frameShow.place(anchor='e', width=1000, height=600)
frameShow.pack(side='right', fill='both')
#  ******  import dataset   ******************
scrollbarY = tk.Scrollbar(frameShow, orient='vertical', width=20)
scrollbarY.pack(side='right', fill='y')
scrollbarX = tk.Scrollbar(frameShow, orient='horizontal', width=20)
scrollbarX.pack(side='bottom', fill='x')
draft = loadDataset()

cnvInsert = tk.Canvas(frameShow, bg="lightblue", width=1000, height=800, yscrollcommand=scrollbarY.set,
                      xscrollcommand=scrollbarX.set)

cnvInsert.pack(expand=0, fill='y')

scrollbarY.config(command=cnvInsert.yview)
scrollbarX.config(command=cnvInsert.xview)

#  *********  import dataset    *******************

dataImportButton = ttk.Button(frameConsole, text='Import dataset', width=35, command=importButtonFunction)
dataImportButton.place(width=80, height=60, x=250, y=150)
dataImportButton.grid(row=5, sticky="nw")

### Manolis ###
# Δημιουργία κουμπιού button για να εκτελέσει την λογιστική παλινδρόμηση
def statsButtonFunction():
    data = loadDataset()
    stats = datasetStatistics(data)
    generateBarplot(data)
    result = 'Minimum value:  ' + str(stats[0]) + '\nMaximum value:  ' + str(stats[1]) + ' \nMean value:  ' + \
             str(stats[2]) + '\nMedian value:  ' + str(stats[3]) + ' \nStd, deviation:  ' + str(stats[4]) + \
             ' \nVariance:  ' + str(stats[5])
    messagebox.showinfo('Success!', result)

statsButton = ttk.Button(frameConsole, text='Dataset statistics', width=35, command=statsButtonFunction)
statsButton.place(width=80, height=60, x=250, y=150)
statsButton.grid(row=7, sticky="nw")

# button to perform logistic regression
def LRButtonFunction():
    data = loadDataset()
    lr = runLogisticRegression(data)
    img = tk.PhotoImage(file="C:/Users/user/Desktop/ΕΑΠ/ΠΛΗΠΡΟ/Project/barplot.png")
    cnvInsert.create_image(350, 350, image=img)
    messagebox.showinfo('Finished linear regression', 'The model achieved accuracy\n of ' + lr)

### ANTONIOU ####
LRButton = ttk.Button(frameConsole, text='Run linear regression', width=35, command=LRButtonFunction)
LRButton.place(width=80, height=60, x=250, y=150)
LRButton.grid(row=9, sticky="nw")

ButtonExit = ttk.Button(frameConsole, text='Έξοδος προγράμματος', width=35, command=root.destroy)
ButtonExit.place(anchor='center', width=80, height=60, x=250, y=150)
ButtonExit.grid(row=12, sticky="nw")

root.mainloop()
