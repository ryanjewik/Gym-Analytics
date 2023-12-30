#imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

#setting up dataframe and datetime objects
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

#cleaning of the weight column
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
        #exercisePlot.invert_yaxis()
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
            plt.legend(bbox_to_anchor=(1, .5, .1, .1), loc='center left', borderaxespad=0, ncol = 1, fontsize = 6)
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
for i in freqPlot.containers:
    freqPlot.bar_label(i,)
plt.savefig("type_frequency"+".png")
plt.figure("frequency by month")
plt.title("frequency by month")
freqByMonth = sns.countplot(data = df, x ="Type", hue = "mY", palette = 'magma')
for i in freqByMonth.containers:
    freqByMonth.bar_label(i,)
plt.legend(bbox_to_anchor=(1, .5, .1, .1), loc='center left', borderaxespad=0,fontsize = 6)
plt.savefig("frequency_by_month"+".png")

#getting the current month and will only include the most recent 3 months
currentMonth = datetime.now().month
recentMonths = []
for i in range(3):
    recentMonths.append((currentMonth - i)%13)

#creating the series that will be used to make the most recent rate of changes graphs
rateOfChange = []
for x in range(len(df['Name'].unique())):
    exerciseName = df['Name'].unique()[x]
    diff = []
    stack = []
    diff.append(1)
    for y in range(len(df)):
        if df['Name'][y] == exerciseName and df['month'][y] in recentMonths:
            stack.append(df['Weight (lbs)'][y])
            if len(stack) > 1:
                val = (stack[len(stack)-1]) - (stack[len(stack)-2])
                val = val / stack[len(stack)-1]
                diff.append(val)
    sum = 0
    for y in range(len(diff)):
        sum+= diff[y]
    rateOfChange.append(sum / len(diff))
rateOfChangeSeries = pd.Series(rateOfChange, df['Name'].unique())


#creating the graphs of the top and bottom 5 exercises where you are seeing the best/worst rate of change within the last 3 months
sortedROC = sorted(rateOfChangeSeries.items(), key=lambda x:x[1])
rocDF = pd.DataFrame(sortedROC)

rocDF['Exercises'] = rocDF[0]
rocDF['ROC'] = rocDF[1]
indexROC = rocDF[ (rocDF['ROC'] == 1) ].index
rocDF.drop(indexROC , inplace=True)
top5 = rocDF.tail()
bottom5 = rocDF.head()
#top5
plt.figure("top5")
plt.xticks(rotation = 20)
plt.title("Top 5 exercises with highest average rate of change within the last 3 months")
top5_plot = sns.barplot(data = top5, x = 'Exercises', y = 'ROC', palette = 'mako')
for i in top5_plot.containers:
    top5_plot.bar_label(i,)
plt.savefig("top5"+".png")
#bottom5
plt.figure("bottom5")
plt.xticks(rotation = 20)
plt.title("Bottom 5 exercises with lowest average rate of change within the last 3 months")
bottom5_plot = sns.barplot(data = bottom5, x = 'Exercises', y = 'ROC', palette = 'viridis')
for i in bottom5_plot.containers:
    bottom5_plot.bar_label(i,)
plt.savefig("bottom5"+".png")


print("Thank you!")
plt.show()


#want to have a rate of change function
