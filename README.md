## HealthCare.Gov-Webscraper
Install the python modules required to run the program.

 ```
 pip install -r requirements.txt
```

After running the file Healthcare.Gov.py, the following prompt would show up in the terminal, asking you to input the name of the .csv file where you'd like to store the results.

```
Please enter a file name to create a new csv file to store your scraped data: {file name}
```

After entering the input, a file of your chosen name would be created in your local directory and the following prompt would pop up asking you for the type of approach you want to use inorder to scrape the webpages.

```
Do you want a targeted approach? [y/n]: y
```
The above mentioned prompt takes input 'y' for targeted approach or 'n' for default approach. Targeted approach scrapes data from a specific page number to another specific page number of your choice. E.g. if you choose pg.20 to pg.40, The data will be scraped starting from page 20, all the way to page 40.

If you don't choose the targeted approach then the default approach would be used which will scrape data starting from page 1, all the way to the final page til the end of results. Choosing the targeted approach by inputting 'y' will pop up the following prompt which will take a numeric input corresponding to the page number from where you would like to start scraping.

For example: lets start scraping from page 10 so the prompt and its input would be as follows.
```
Which page would you like to start scraping from?: 10
```
Similarly, the following prompt will ask for a numeric input corresponding to the page number where you would like to end your scraping session in case of targeted approach. The default approach shows no such prompts but instead uses default values.

In this example, we'll end our scraping session on page 40.
```
Which page would you like to end scraping at?: 40
```
Once the desired approach has been selected, The filter prompts will appear asking for the types of results you would like to search for. 

The below mentioned prompt takes in states name as input such as:

Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina, South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming

In this example, we'd use Texas as our input.

```
Please enter the name of state for which you would like to scrape results for?: Texas
```
Once the input has been entered, the 2nd prompt for filter would show up, asking for the coverage type.

In this example, we'd choose 1 for individual or family.

```
What kind coverage are you looking for? Please enter:
'1' for individual or family
'2' for Medicaid or CHIP
'3' for Small businesses
1
```
Afterwards, the 3rd prompt for filter would pop up, asking for the type of help you'd like to select.

In this examaple, We'd select 2 to search for health insurance agents or broker.

```
What type of help are you looking for? Please enter:
'1' for All help
'2' for Agent or broker
'3' for Assister
2
```
The 4th filter prompt will ask you for the number of years of service you'd like your search results to have. The input value should be between 1 to 10.

For example, Select 10 as input. 
```
Please enter the number of years served by the service provider. Entry must be between 1 to 10 or enter any other number for default filter: 10
```
On 5th filter prompt, you'd be asked for the days you'd want your searched service provider to be available on.

In this example, we'd select 1 as our input because we want our searched service providers to be available on weekdays.

```
What days would you like for service provider to be available on? Please enter:                                     
'1' for Weekdays
'2' for Weekends
'3' for Both Weekdays and Weekends
1
```
On the last filter prompt, you'd be asked for the time you'd want your searched service providers to be available on.

In this example, we'd select 2 as our input because we want our searched service providers to be available from 9am to 5pm.

```
What days would you like for service provider to be available on? Please enter:                                     
'1' for Weekdays
'2' for Weekends
'3' for Both Weekdays and Weekends
2
```
Once the input has been entered to the above mentioned prompt, the scraping process will begin. Starting from page 10, all the way til page 40.

If incase for whatever reason the scraping process is interrupted before completion, you can start the program again and it will ask you if you want to continue scraping from where you left off earlier or start a new scraping session altogether. An example of this prompt is shown as follows.

```
Some progress from last scraping session is detected, Would you like to continue from last session?[y/n]: 
```

This was made possible by saving the required information on PROGRESS_REPORT.save file during each iteration of page scraping session. The information stored in the PROGRESS_REPORT.save includes the file name where results are to be stored from the earlier scraping session, the URL with all the inputted filters, the last page number that was scraped at the time of interruption, the scraping approach (targeted or default) and final page number where you'd want your session to end (In case of targeted approach).

Once the scraping process is completed, the results are stored in .csv format as shown below.

```
NAME,PHONE,EMAIL,TYPE,YEARS_SERVED
**** Siska,(979) 282 - XXXX,****@yahoo.com,Agent/Broker,11 years
**** Locke,(936) 598 - XXXX,****@jbafinancial.com,Agent/Broker,10 years
**** Trevino,(210) 659 - XXXX,****@yahoo.com,Agent/Broker,10 years
**** Fristoe,(940) 322 - XXXX,****e@wf.net,Agent/BrokerMultiple States,10 years
**** Gunnels,(979) 774 - XXXX,****@anco.com,Agent/Broker,10 years
**** Clark,(832) 527 - XXXX,****@yahoo.com,Agent/Broker,10 years
**** Watters,(409) 883 - XXXX,****@msn.com,Agent/Broker,10 years
**** Goodson,(903) 838 - XXXX,****@aol.com,Agent/BrokerMultiple States,10 years
**** Swain,(254) 314 - XXXX,****@swaininsurance.net,Agent/Broker,10 years
**** Bell,(817) 469 - XXXX,****@hotmail.com,Agent/Broker,10 years
**** Sathaye,(972) 556 - XXXX,****@givemeinsurance.com,Agent/Broker,10 years
**** McCarty,(937) 620 - XXXX,****@gmail.com,Agent/BrokerMultiple States,11 years
**** Quintero,(210) 328 - XXXX,****@yahoo.com,Agent/Broker,10 years
**** Watters,(409) 883 - XXXX,****@msn.com,Agent/Broker,10 years
```
The contact information of the service providers above has been omitted as it is for demonstration purposes only.
