This is the django project where magic should and hopefully will take place.  

Please look through the run.sh script to add environment variables as appropriate. 

The models currently in here are simply for testing.

The Project covers 3 exchanges. The NYSE, NASDAQ, and AMEX

The objectives for the MVP is as follows:
	1) Create an efficient database and code structure for extraction of information, and computation.
	2) Leverage news information, and other relevant sources.
	3) Create a system of predictive analytics.  Predict if a stock will go up or down in a given day.
	4) Create a system of back-testing, and programatic jobs that seek to improve the accuracy of the predictions made by the system.   
	5) Create a front end system to visualize the information created by the above tasks. 
	6) Create a front end system that allows users to run tests of their own creation. 

Because this is somewhat of a homegrown system, I'm going to take the liberty of inventing some metrics I believe will be helpful in describing what goes on in the system. 
For industries
* industry overall percent change (ind_pct_ov_ch) will be calculated as the sumproduct of the companies market cap and their daily % change divided by the sum of all market caps for the industry. 
* industry overall percent range (ind_pct_ov_rg) will be calculated as the sumproduct of the companies and their daily % range divided by the sum of the companies market caps for the industry
* Industry Percent Volume is an estimate of the total % of the total volume in the industry that was traded that given day. 

Note: because I'm doing this post-facto I'm only able to grab the market cap at a point in time. And without knowing the shares outstanding, my calculations may be subject to error because of the changing market cap. However, I'm going to make the assumption for this v1 that the change in market cap is nominal. 


First Test:
	Create a table of the fortune 500, changing the y variable for each test, and add in news about a single company. 
	PFE,PDCO,ETFC,NBL,RIG,KSS,PXD,SEE,ESRX,DOW
