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
    if df['Weight (lbs)'][x] == 'bodyweight':
        df['Weight (lbs)'][x] = bodyweight


#choose a specific exercise
userChoice = input("Would you like to see the trend of a specific exercise? (y/n)")
while userChoice != 'y' and userChoice != 'n':
    userChoice =input("Please enter a valid option (y/n)")
while userChoice == 'y':
    exerciseInput = input("What exercise would you like to check your progress in?")
    exercise = df[df['Name'] == exerciseInput]
    figureString = exerciseInput + " weight trend"
    plt.figure(figureString, figsize = (12,6))
    exercisePlot =sns.lineplot(data = exercise, x = 'Date', y = 'Weight (lbs)')
    exercisePlot.invert_yaxis()
    userChoice = input("Would you like to continue? (y/n)")

#exercise type frequency
plt.figure("type frequency")
freqPlot = sns.countplot(data = df, x ="Type", palette = 'flare')
plt.figure("frequency by month")
freqByMonth = sns.countplot(data = df, x ="Type", hue = "mY", palette = 'flare')
plt.show()


#want to have a rate of change function
