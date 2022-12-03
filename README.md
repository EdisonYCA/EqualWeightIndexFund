# EqualWeightIndexFund

This project allows a user to retrieve the number of shares to buy from a market capitalization-weighted S&P 500 index fund, in order to create an equal-weight S&P 500 index fund. 

The Python script preforms this functionality in three steps:
  1. Gather each stock price for each stock in the ```sp_500_stocks.csv``` file using the IEX Cloud API endpoint
  2. Retrieve the users portfolio amount
  3. Calculate the amount of shares to buy and format the output to ```recommended trades.xlsx```
 
 It's important to note that I used the free version of the IEX Cloud API. Thus, all of the data gathered for each stock price are *not* accucurate and are generated. Nevertheless,
 this limitation isn't an issue, as the program would function properly and accurately with real stock prices. 

Something else to note is that the *.csv* file containing the S&P 500 stocks is hard-coded, therefore the user can only use the stocks in this index. However, this program can
certainly be modified to prompt the user to enter the name of their own csv file containing the specific index they'd like to track. 

As a final note, each stock, stock price, market capitalization, and number of shares to buy were formatted using the ```pandas``` library which provided an easy strucure for this data
to be neatly formatted.

As mentioned, one of the modifications that can be made to improve this program is the ability for the user to enter their own S&P 500 index that they'd like to track. 

An improvement that can be to improve the readability of this code, is to remove lines **15-19, 32, and 33.** Essentially, these lines of code added the first stock data into the
pandas dataframe (which contains the tabular format of the data) which can all be done in one fell swoop using a for-loop. However, I faced some issues using the **.append**
method from the pandas library; I consistently got future-warnings. I found that the best way to remedy this was to use the **.concat** before the foor-loop on the data of
the first stock, and then add the remaining data.

Lastly, a challenge faced was that the data gathering of each stock using HTTP requests was incredibly slow when doing one stock at a time. However, the IEX Cloud API allowed
for batch calls, which allowed me to call only have to call 5 requests when splitting the stocks into sublists of 100 length each. As a result, this program became 5x more efficent.

```/EqualWeightIndexFund/equal_weight_s&p_500.py``` contains the source code for this program. *Please keep in mind that if you'd like to run this program, a free secret IEX Cloud API Token is required.*

![image](https://user-images.githubusercontent.com/116458652/205455578-4a6d8bcd-c811-4f8f-8abd-0e4314260c5b.png)
![image](https://user-images.githubusercontent.com/116458652/205455598-d3819795-51a6-4030-9ade-92ff9f62b01e.png)

**This program was created with the help of the Algorithim Trading Using Python Course from freeCodeCamp.org***
