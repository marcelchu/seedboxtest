# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 12:07:06 2018

@author: Marcel Chu
Title: SeedBox Technologies Test
"""
#Importing the libraries
import matplotlib.pyplot as plt
import pandas as pd

#Read the files
testsamples = pd.read_csv("testSamples.csv")
transData = pd.read_csv("transData.csv")

"""
1.What is the aproximate probability distribution between the test group 
and the control group?
"""
#Make new list with unique test group (1) and control group (0)
test_group_list = testsamples.loc[testsamples['test_group'] == 1]
control_group_list = testsamples.loc[testsamples['test_group'] == 0]


#Calculating the probability distribution
p_test_group = len(test_group_list)/len(testsamples)
p_control_group = 1-p_test_group

print("\n1.What is the aproximate probability distribution between the test group and the control group?\n")

print("The aproximate probability distribution for the test group (must call-in) is " 
      + str("{0:.2f}".format(p_test_group)) + " and " 
      + str("{0:.2f}".format(p_control_group)) 
      + " for the control group (web-form). Indeed, there are " 
      + str(len(test_group_list)) 
      + " people placed in the must call-in to cancel test group and "
      + str(len(control_group_list)) 
      + " people placed in the web form test group. The total population studied is "
      + str(len(testsamples)) + ".\n\n")

#Data to plot.
labels = 'Must call-in', 'Web-form'
sizes = ["{0:.2f}".format(p_test_group),"{0:.2f}".format(p_control_group)]
colors = ['yellowgreen','lightskyblue']
explode = (0.1,0)
 
# Pie chart for the probability distribution.
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()

"""
2 Is a user that must call-in to cancel more likely to generate at least 1 addition REBILL?
"""

#Make new list with only rebill
rebill_list = transData.loc[transData['transaction_type'] == "REBILL"]

#Merging all the sample_id with the correct test_group
rebill_merged_list = rebill_list.merge(testsamples, left_on='sample_id', 
                                       right_on='sample_id' )

#Making a new list for rebill test group and rebill control group
rebill_test = rebill_merged_list.loc[rebill_merged_list['test_group'] == 1]
del rebill_test['transaction_amount']
del rebill_test['transaction_id']

rebill_control = rebill_merged_list.loc[rebill_merged_list['test_group'] == 0]
del rebill_control['transaction_amount']
del rebill_control['transaction_id']

#Returning a list with the unique sample_id. Count the number of REBILL for each sample_id.
rebill_test = rebill_test.groupby(rebill_test.columns.tolist()).size().reset_index().rename(columns={0:'rebill_count'})
rebill_control = rebill_control.groupby(rebill_control.columns.tolist()).size().reset_index().rename(columns={0:'rebill_count'})

#Calculate the average REBILL count for each test group.
total_rebill_count_control = rebill_control.loc[rebill_control['test_group'] == 0, 'rebill_count'].sum()
average_rebill_control = total_rebill_count_control/len(control_group_list)

total_rebill_count_test = rebill_test.loc[rebill_test['test_group'] == 1, 'rebill_count'].sum()
average_rebill_test = total_rebill_count_test/len(test_group_list)

#Number of REBILL difference.
difference = (total_rebill_count_test/len(test_group_list))-(total_rebill_count_control/len(control_group_list))


print("2 Is a user that must call-in to cancel more likely to generate at least 1 addition REBILL?\n")

print("With the given data, we know that "
      + str(len(control_group_list)) + " web-form users do in total "
      + str(total_rebill_count_control) + " REBILLS. Furthermore, "
      + str(len(test_group_list)) + " call-in users do in total "
      + str(total_rebill_count_test) + " REBILLS. The average amount of REBILLs for web-form users is " 
      + str("{0:.2f}".format(average_rebill_control))
      + " REBILLs per user and the average amount of REBILLs for must call-in users is " 
      + str("{0:.2f}".format(average_rebill_test)) 
      + " REBILLs per user. If we do a substraction between the amounts, we can see that"
      + " the must call-in to cancel generate in average "
      + str("{0:.2f}".format(difference)) 
      + " more REBILLS than the web-form."
      + "It is not 1 additionnal REBILL, but this value shows that the must call-in group helps the company make more profit, because they don't want to call to make an cancellation.\n\n")

"""
3 Is a user that must call-in to cancel more likely to generate more revenues?
"""

#Merging all the sample_id with the correct test_group
transaction_merged = transData.merge(testsamples, left_on='sample_id', 
                                       right_on='sample_id' )

#Sum all the transaction amounts of the specific test group
totaltransAmount_controlGroup = transaction_merged.loc[transaction_merged['test_group'] == 0, 'transaction_amount'].sum()
totaltransAmount_testGroup = transaction_merged.loc[transaction_merged['test_group'] == 1, 'transaction_amount'].sum()

#Calculate the average revenue for each test group.
AVGtransAmount_controlGroup = totaltransAmount_controlGroup/len(control_group_list)
AVGtransAmount_testGroup = totaltransAmount_testGroup/len(test_group_list)


#Revenu difference
revenue_difference = AVGtransAmount_testGroup - AVGtransAmount_controlGroup

print("3 Is a user that must call-in to cancel more likely to generate more revenues?\n")

print("In total, the web-form users generate "
      + str("{0:.2f}".format(totaltransAmount_controlGroup)) + "$ and the must call-in users generate "
      + str("{0:.2f}".format(totaltransAmount_testGroup)) + "$." 
      + "The average revenue amount is "
      + str("{0:.2f}".format(AVGtransAmount_controlGroup))
      + "$ per web-form user and the average revenue amount is "
      + str("{0:.2f}".format(AVGtransAmount_testGroup))
      + "$ per must call-in user. With this information,"
      + "we can confirm that the must call-in to cancel user is more likely "
      + "to generate more revenues than the web-form to cancel user."
      + "In fact, with a simple substraction, the must-call in to cancel test group generate in average "
      + str("{0:.2f}".format(revenue_difference)) + "$ more per user than the web form test group."
      + "People don't want to call-in to cancel their subscription therefore they still have to pay.\n\n")

CallIn_transactions = transaction_merged.loc[transaction_merged['test_group'] == 1]

#Data to plot.
labels = 'REBILL', 'CHARGEBACK', 'REFUND'
sizes = [len(CallIn_transactions[CallIn_transactions["transaction_type"]=='REBILL']),
         len(CallIn_transactions[CallIn_transactions["transaction_type"]=='CHARGEBACK']),
         len(CallIn_transactions[CallIn_transactions["transaction_type"]=='REFUND'])]
colors = ['yellowgreen','lightskyblue','red']
 
# Plot for call-in transactions
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()

WebForm_transactions = transaction_merged.loc[transaction_merged['test_group'] == 0]

#Data to plot.
labels = 'REBILL', 'CHARGEBACK', 'REFUND'
sizes = [len(WebForm_transactions[WebForm_transactions["transaction_type"]=='REBILL']),
         len(WebForm_transactions[WebForm_transactions["transaction_type"]=='CHARGEBACK']),
         len(WebForm_transactions[WebForm_transactions["transaction_type"]=='REFUND'])]
colors = ['yellowgreen','lightskyblue','red']
 
# Plot for web-form transaction.
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()

print("By comparing the 2 pie charts, we can also see that the call-in users generate more percentage rebill than web-form users.\
      Also, we can notice that the number of Chargeback and refund are higher when it comes to web-form users.")

"""
4 Is a user that must call-in more likely to produce a higher chargeback rate(CHARGEBACKs/REBILLs)?
"""

#Making respective list for each test group regrouping all transactions.
CallIn_list = transaction_merged.loc[transaction_merged['test_group'] == 1]
WebForm_list = transaction_merged.loc[transaction_merged['test_group'] == 0]

#Count the total number of REBILL for each test group.
totalRebill_CallIn = len(CallIn_list[CallIn_list["transaction_type"]=='REBILL'])
totalRebill_WebForm = len(WebForm_list[WebForm_list["transaction_type"]=='REBILL'])

#Count the total number of CHARGEBACK for each test group.
totalChargeBack_CallIn= len(CallIn_list[CallIn_list["transaction_type"]=='CHARGEBACK'])
totalChargeBack_WebForm = len(WebForm_list[WebForm_list["transaction_type"]=='CHARGEBACK'])

#Calculate the chargeback rate for each test group.
ChargebackRate_CallIn = (totalChargeBack_CallIn/totalRebill_CallIn)*100
ChargebackRate_WebForm = (totalChargeBack_WebForm/totalRebill_WebForm)*100
Chargeback_difference = ChargebackRate_WebForm - ChargebackRate_CallIn

print("4 Is a user that must call-in more likely to produce a higher chargeback rate(CHARGEBACKs/REBILLs)\n")

print("With the informations, we know that the must call-in users get in total "
      + str(totalRebill_CallIn) + " rebills and " + str(totalChargeBack_CallIn)
      + " chargebacks. The chargeback rate for the must call-in test group is "
      + str("{0:.2f}".format(ChargebackRate_CallIn))
      + "%. Also, we can also confirm the web-form users get in total "
      + str(totalRebill_WebForm) + " rebills and " + str(totalChargeBack_WebForm)
      + " chargebacks. The chargeback rate for this test group is "
      + str("{0:.2f}".format(ChargebackRate_WebForm)) + "%. As we can see, "
      + "it is more likely for a web-form user to have a higher chargeback rate. "
      + "We notice that web-form have "
      + str("{0:.2f}".format(Chargeback_difference)) + "% more chance to produce a higher chargeback rate."
      + " This result proves that web-form users are more prone to find a way to get their money back.")