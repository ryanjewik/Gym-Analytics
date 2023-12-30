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

#will ask for bodyweight
bodyweight = input("What is your bodyweght?")
for x in range(len(df['Weight (lbs)'])):
    if df['Weight (lbs)'][x] == 'bodyweight' or df['Weight (lbs)'][x] == 'Bodyweight':
        df['Weight (lbs)'][x] = bodyweight


#choose a specific exercise
userChoice = input("Would you like to see the trend of a specific exercise? (y/n)")
while userChoice != 'y' and userChoice != 'n':
    userChoice =input("Please enter a valid option (y/n)")
while userChoice == 'y':
    exerciseInput = input("What exercise would you like to check your progress in? (an exercise name, 'list' to show all exercises, or 'all' to show all of them at once)")
    if exerciseInput in df['Name'].unique():
        exercise = df[df['Name'] == exerciseInput]
        figureString = exerciseInput + " weight trend"
        plt.figure(figureString, figsize = (12,6))
        exercisePlot =sns.lineplot(data = exercise, x = 'Date', y = 'Weight (lbs)')
        exercisePlot.invert_yaxis()
        plt.savefig(exerciseInput+"_trend.png")
        userChoice = input("Would you like to continue? (y/n)")
    elif exerciseInput == 'list':
        print("Exercises list:")
        for x in range(len(df['Name'].unique())):
            print(" - " + df['Name'].unique()[x])
        userChoice = input("Would you like to continue? (y/n)")
    elif exerciseInput == 'all':
        print("working...")
        plt.figure(figsize = (12,6))
        for x in range(len(df['Name'].unique())):
            exerciseName = df['Name'].unique()[x]
            exercise = df[df['Name'] == exerciseName]
            plot =sns.lineplot(data = exercise, x = 'Date', y = 'Weight (lbs)', label = exerciseName)
        plot.invert_yaxis()
        N=20
        plt.xticks(df['Date'].unique(), rotation = 'vertical') # add loads of ticks
        plt.yticks(df['Weight (lbs)'].unique())
        plt.grid()
        plt.gca().margins(x=0)
        plt.gcf().canvas.draw()
        tl = plt.gca().get_xticklabels()
        maxsize = max([t.get_window_extent().width for t in tl])
        m = 0.2 # inch margin
        s = maxsize/plt.gcf().dpi*N+2*m
        margin = m/plt.gcf().get_size_inches()[0]
        plt.gcf().subplots_adjust(left=margin, right=1.-margin)
        plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
        #saving to file
        plt.savefig("all_exercises_trends"+".png")
        #plt.show()
        plt.legend(bbox_to_anchor=(1.02, 1, .5, .5), loc='best', borderaxespad=0)
        userChoice = input("Would you like to continue? (y/n)")
    else:
        print("Please enter a valid option.")
    

#exercise type frequency
plt.figure("type frequency")
freqPlot = sns.countplot(data = df, x ="Type", palette = 'flare')
plt.savefig("type_frequency"+".png")
plt.figure("frequency by month")
freqByMonth = sns.countplot(data = df, x ="Type", hue = "mY", palette = 'flare')
plt.savefig("frequency_by_month"+".png")
print("Thank you!")
plt.show()


#want to have a rate of change function
