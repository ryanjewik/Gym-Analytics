Using the gym csv thee gym-analytics.py script will return info on:
 - the top 5 exercises in terms of average rate of change over the past 3 months
 - the bottom 5 exercises in terms of average rate of change over the past 3 months
 - the frequency of push, pull, legs, and core exercises
 - the frequency of push, pull, legs and, core exercises by month
Additionally, the user will be asked if they would like a trend chart of an exercise in which the user has a few options:
 - they may call for a specific exercise, in which then a lineplot will be created for that specific exercise
 - they can call 'list', which will return a list of all of the possible exercises
 - they can call 'all' which will return a lineplot for all of the exercises and put them into one figure, based on type (push/pull/legs/core)
   
It will also prompt the user for "bodyweight" to substitute in the event the weight column value returns 'bodyweight'

to run: gym-analytics.py

installations: 
pip install pandas
pip install numpy
pip install seaborn
pip install datetime
