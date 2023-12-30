#imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

#setting up dataframe
df = pd.read_csv("gym.csv")
df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%Y')
df['month'] = pd.DatetimeIndex(df['Date']).month
df['year'] = pd.DatetimeIndex(df['Date']).year
mY = []
for x in range(len(df['month'])):
    mY.append(str(df['month'][x]) + '/' + str(df['year'][x]))
df['mY'] = mY
df['mY'] = pd.to_datetime(df['mY'],format='%m/%Y')

#will ask for bodyweight
bodyweight = input("What is your bodyweight?")
for x in range(len(df['Weight (lbs)'])):
    if df['Weight (lbs)'][x] == 'bodyweight' or df['Weight (lbs)'][x] == 'Bodyweight':
        df['Weight (lbs)'][x] = bodyweight
for x in range(len(df)):
    df['Weight (lbs)'][x] = str(df['Weight (lbs)'][x])
df['Weight (lbs)'] = pd.to_numeric(df['Weight (lbs)'])
for x in range(len(df)):
    df['Weight (lbs)'][x] = int(df['Weight (lbs)'][x])



#choose a specific exercise
userChoice = input("Would you like to see the trend chart of your exercises? (y/n)")
while userChoice != 'y' and userChoice != 'n':
    userChoice =input("Please enter a valid option (y/n)")
while userChoice == 'y':
    exerciseInput = input("What exercise would you like to check your progress in? (an exercise name, 'list' to show all exercises, or 'all' to show all of them at once)")
    if exerciseInput in df['Name'].unique(): #prints the trend of an individual exercise
        exercise = df[df['Name'] == exerciseInput]
        figureString = exerciseInput + " weight trend"
        plt.figure(figureString, figsize = (12,6))
        exercisePlot =sns.lineplot(data = exercise, x = 'Date', y = 'Weight (lbs)')
        exercisePlot.invert_yaxis()
        plt.title(exerciseInput + " trend plot")
        plt.savefig(exerciseInput+"_trend.png")
        userChoice = input("Would you like to continue? (y/n)")
    elif exerciseInput == 'list': #prints a list of all of the exercises
        print("Exercises list:")
        for x in range(len(df['Name'].unique())):
            print(" - " + df['Name'].unique()[x])
        userChoice = input("Would you like to continue? (y/n)")
    elif exerciseInput == 'all': #prints charts for all of your exercises
        print("working...")
        types = df['Type'].unique()
        for y in range(len(types)):
            typeDF = df[df['Type'] == types[y]]
            typeDF = typeDF.sort_values(by = 'Weight (lbs)', ascending = True)
            plt.figure(figsize = (12,6))
            for x in range(len(typeDF['Name'].unique())):
                exerciseName = typeDF['Name'].unique()[x]
                exercise = typeDF[typeDF['Name'] == exerciseName]
                exercise = exercise.sort_values(by = 'Weight (lbs)', ascending=True)
                plot =sns.lineplot(data = exercise, x = 'Date', y = 'Weight (lbs)', label = exerciseName)
            #plot.invert_yaxis()
            N=20
            plt.legend(bbox_to_anchor=(1.05, 1.3, .5, .5), loc='upper right', borderaxespad=0)
            plt.xticks(typeDF['mY'].unique(), rotation = 'vertical') # add loads of ticks
            plt.yticks(range(0 ,300, 10))
            plt.grid()
            plt.gca().margins(x=0)
            plt.gcf().canvas.draw()
            plt.title(types[y] + " trends plot")
            
            #saving to file
            plt.savefig(types[y] + "_trends"+".png")
            #plt.show()
        userChoice = input("Would you like to continue? (y/n)")
    else:
        print("Please enter a valid option.")
    

#exercise type frequency
plt.figure("type frequency")
plt.title("frequency plot by type")
freqPlot = sns.countplot(data = df, x ="Type", palette = 'flare')
plt.savefig("type_frequency"+".png")
plt.figure("frequency by month")
plt.title("frequency by month")
freqByMonth = sns.countplot(data = df, x ="Type", hue = "mY", palette = 'flare')
plt.savefig("frequency_by_month"+".png")
print("Thank you!")
plt.show()


#want to have a rate of change function
