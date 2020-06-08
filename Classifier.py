"""
Monash University Malaysia
FIT3162 Computer Science Project 2

Author 1: Daniel Ng Yit Yang
Author 2: Chong Jia Voon
Tested by: Justin Ang Wei-Shen

Last Edited Date: 05/06/2020

This file is to have an algorithm to calculate the best advertisement to show at that time based
on the array that is given.
"""

from Database import *


def get_age(age):
    """
    returns the age in string for comparison
    """
    if age <= 10:
        return '0-10'
    elif 10 < age <= 20:
        return '10-20'
    elif 20 < age <= 30:
        return '20-30'
    elif 30 < age <= 40:
        return '30-40'
    elif 40 < age <= 50:
        return '40-50'
    elif 50 < age <= 60:
        return '50-60'
    elif 60 < age <= 70:
        return '60-70'
    elif 70 < age <= 80:
        return '70-80'
    elif 80 < age <= 90:
        return '80-90'
    else:
        return '90-100'


def classify(people):
    """
    Function to classify majority in a group and return the appropriate ad
    """
    # For when there is nothing in the table
    string = "SELECT COUNT(*) FROM MST_AD;"
    db = database()
    for c in db.runsql(string):
        # checks if the value returned exists.
        if c[0] == 0:
            return

    # Set initial values
    maj_list = []
    prm = None
    ad = None

    # Sets the database and selects all non deleted values
    db = database()
    cursor = db.select()

    # checks for the premium ad
    for c in cursor:
        if c[5] == 'Y':
            prm = c

    # aggregate based on same type of people
    for i in range(len(people)):
        flag = True
        person = people[i]
        person.append(get_age(person[1]))  # person = [gender, age, ageGroup]

        # checks in the list for any existing same category
        for j in range(len(maj_list)):
            if person[0] == maj_list[j][0] and person[2] == maj_list[j][2]:
                maj_list[j][-1] += 1
                flag = False

        # if the do not exist adds them into the list
        if flag:
            person.append(1)  # person = [gender, age, ageGroup, majorityCount]
            maj_list.append(person)

    # sets the initial values for getting the right group
    max_num = 0
    gen = ""
    age = ""

    # gets the majority
    for maj in maj_list:
        if max_num < maj[-1]:
            max_num = maj[-1]
            gen = maj[0]
            age = maj[2]

    # counts if there a few majority
    count = 0
    for maj in maj_list:
        print("maj: ", maj)
        if max_num == maj[-1]:
            count += 1

    # initialise for backups ads
    backup = None
    adcount = 0
    cursor = db.select()

    # checks the database for a match of category
    for ads in cursor:
        backup = ads
        # age and gender classification
        if ads[3] == age and ads[4] == gen:
            ad = ads
            adcount += 1

    # if there are more than one category or there is no one that exist
    # give the premium advertisement
    if people == [] or count > 1:
        ad = prm
    else:
        # no ad that matches give premium
        if adcount > 1 or adcount == 0:
            ad = prm

    # if there isn't any ad that matches it
    if ad is None:
        ad = backup

    # return the filename for the ad
    return ad[2]

