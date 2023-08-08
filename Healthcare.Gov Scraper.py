from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from csv import DictWriter
import undetected_chromedriver as uc
import os
import os.path

############################################### - DataCollector Class - ##################################################################################
# This class is just a collection of staticmethods that cleans data from the webpage and extracts the only useful information that we need. 

class DataCollector:

    @staticmethod
    def text_list(info):
        profile=info.text
        profile_contents=profile.split('\n')
        return profile_contents

    @staticmethod
    def name(profile_contents):
        return profile_contents[0]

    @staticmethod
    def years_served(profile_contents):
        years_of_service=''
        for content in profile_contents:
            if 'years of service' in content:
                years_of_service=content[:-12]
        return years_of_service
    
    @staticmethod
    def help_type(profile_contents):
        type_of_help=''
        for content in profile_contents:
            if 'Agent/Broker' in content or 'Assister' in content:
                type_of_help=content
        return type_of_help

    @staticmethod
    def phone_number(profile_contents):
        phone=''
        for content in profile_contents:
            if len(content)==16 and '(' in content and ')' in content and '-' in content:
                    phone=content
        return phone

    @staticmethod
    def email(profile_contents):
        email_address=''
        for content in profile_contents:
            if '@' in content:
                email_address=content
        return email_address
    
    @staticmethod
    def page_initialization(web_driver):
        try:
            WebDriverWait(web_driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@id='status-summary']")))
            status_summary=(web_driver.find_element(By.XPATH,"//div[@id='status-summary']").text).split('\n')
        except TimeoutException:
            return 'Unable to load web element.'
        tries=0
        while "Showing 0 results" in status_summary[0] and tries<5:
            time.sleep(5)
            status_summary=(web_driver.find_element(By.XPATH,"//div[@id='status-summary']").text).split('\n')
            tries+=1
        if "Showing 0 results" in status_summary[0]:
            return 'No results available.'
        return 'initialization Complete!'
    
    @staticmethod
    def total_pages(web_driver):
        try:
            pages=web_driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div[2]/div[4]/div/nav/ul/li[7]/a').text
            if ',' in pages:
                return int(pages.replace(',','').strip())
            else:
                return int(pages.strip())
        except:
            return 'ERROR: No results available'
        
    @staticmethod
    def page_contents(web_driver):
        try:
            WebDriverWait(web_driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='ds-l-row ds-u-margin-bottom--2']")))
            return web_driver.find_elements(By.XPATH,"//div[@class='ds-l-row ds-u-margin-bottom--2']")
        except:
            return []

    @classmethod
    def compile_record(cls,info):
        profile_contents=cls.text_list(info)
        name=cls.name(profile_contents)
        phone=cls.phone_number(profile_contents)
        email_address=cls.email(profile_contents)
        type_of_help=cls.help_type(profile_contents)
        years_of_service=cls.years_served(profile_contents)
        return name,phone,email_address,type_of_help,years_of_service

############################################### - HealthCare.gov URL Class - ##################################################################
# This class allows you to add filters of your choice to your search results by returning a URL string adjusted for those filters.

class HealthcareGovURL:
    
    def __init__(self,state,page_from):
        self.state=state
        self.states_dict={'Alabama':'AL', 'Alaska':'AK', 'Arizona':'AZ', 'Arkansas':'AR', 'California':'CA', 'Colorado':'CO', 'Connecticut':'CT', 'Delaware':'DE', 'Florida':'FL', 'Georgia':'GA', 'Hawaii':'HI', 'Idaho':'ID', 'Illinois':'IL', 'Indiana':'IN', 'Iowa':'IA', 'Kansas':'KS', 'Kentucky':'KY', 'Louisiana':'LA', 'Maine':'ME', 'Maryland':'MD', 'Massachusetts':'MA', 'Michigan':'MI', 'Minnesota':'MN', 'Mississippi':'MS', 'Missouri':'MO', 'Montana':'MT', 'Nebraska':'NE', 'Nevada':'NV', 'New Hampshire':'NH', 'New Jersey':'NJ', 'New Mexico':'NM', 'New York':'NY', 'North Carolina':'NC', 'North Dakota':'ND', 'Ohio':'OH', 'Oklahoma':'OK', 'Oregon':'OR', 'Pennsylvania':'PA', 'Rhode Island':'RI', 'South Carolina':'SC', 'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX', 'Utah':'UT', 'Vermont':'VT', 'Virginia':'VA', 'Washington':'WA', 'West Virginia':'WV', 'Wisconsin':'WI', 'Wyoming':'WY'}
        self.page_from=page_from
        self.URL=f'https://localhelp.healthcare.gov/results?q={state.upper()}&lat=0&lng=0&city=&state={self.states_dict[state.title()]}&zip_code=&mp=FFM&page={page_from}'
        self.coverage_filter="&coverage="
        self.type_filter="&type="
        self.years_filter='&yearsOfService='
        self.days_filter='&days='
        self.time_filter='&hours='

    def coverage_type(self,selection):
        if selection==2:
            self.URL+=f'{self.coverage_filter}medicaid'
        elif selection==3:
            self.URL+=f'{self.coverage_filter}shop'
        else:
            self.URL+=f'{self.coverage_filter}individual'
        return self.URL

    def help_type(self,selection):
        if selection==2:
            self.URL+=f'{self.type_filter}agent{self.type_filter}multistate'
        elif selection==3:
            self.URL+=f'{self.type_filter}assister{self.type_filter}statewide'
        else:
            self.URL+=f'{self.type_filter}agent{self.type_filter}multistate{self.type_filter}assister{self.type_filter}statewide'
        return self.URL
    
    def years_served(self,years):
        if type(years)==int:
            if years>=1 and years<=10:
                self.URL+=f'{self.years_filter}{years}'
        return self.URL
    
    def days_available(self,selection):
        if selection==1:
            self.URL+=f'{self.days_filter}mon{self.days_filter}tue{self.days_filter}wed{self.days_filter}thu{self.days_filter}fri'
        elif selection==2:
            self.URL+=f'{self.days_filter}sat{self.days_filter}sun'
        elif selection==3:
            self.URL+=f'{self.days_filter}mon{self.days_filter}tue{self.days_filter}wed{self.days_filter}thu{self.days_filter}fri{self.days_filter}sat{self.days_filter}sun'
        return self.URL
    
    def time_available(self,selection):
        if selection==1:
            self.URL+=f'{self.time_filter}morning'
        elif selection==2:
            self.URL+=f'{self.time_filter}afternoon'
        elif selection==3:
            self.URL+=f'{self.time_filter}night'
        elif selection==4:
            self.URL+=f'{self.time_filter}morning{self.time_filter}afternoon'
        elif selection==5:
            self.URL+=f'{self.time_filter}afternoon{self.time_filter}night'
        elif selection==6:
            self.URL+=f'{self.time_filter}morning{self.time_filter}night'
        elif selection==7:
            self.URL+=f'{self.time_filter}morning{self.time_filter}afternoon{self.time_filter}night'
        return self.URL
    
    def apply_filters(self,coverage,help,years,days,time):
        self.coverage_type(coverage)
        self.help_type(help)
        self.years_served(years)
        self.days_available(days)
        self.time_available(time)
        return self.URL

############################################### - PROGRESS SAVING SYSTEM - ##################################################################################################################################################################
# In case the program shuts down unexpectedly, this section of the code checks if there is any saved progress from the last scraping session to allow you to continue from where you left off or start a new scraping session altogether.

file_name,URL,from_page,to_page,mode="","",1,0,0
continue_mode="n"

if os.path.isfile("PROGRESS_REPORT.save") is False:
    with open('PROGRESS_REPORT.save','w') as save_progress:
        save_file_lines=save_progress.write(f"{file_name}\n{URL}\n{from_page}\n{to_page}\n{mode}")
        save_progress.close()
else:
    with open("PROGRESS_REPORT.save",'r') as rd:
        saved_line=rd.readlines()
        previous_file=saved_line[0].replace("\n","")
        if len(saved_line)==5 and os.path.isfile(f"{previous_file}.csv"):
            while True:
                continue_from=input("Some progress from last scraping session is detected, Would you like to continue from last session?[y/n]: ").strip()
                if continue_from.lower()=='y':
                    continue_mode="y"
                    file_name=previous_file
                    URL=saved_line[1].replace("\n","")
                    if int(saved_line[2])>1:
                        from_page=int(saved_line[2])+1
                    if int(saved_line[3])>from_page and int(saved_line[4])==1:
                        to_page=int(saved_line[3])
                        targeted=True
                        mode=1
                    elif int(saved_line[4])==0:
                        targeted=False
                        mode=0
                    break
                elif continue_from.lower()=='n':
                    continue_mode="n"
                    break
                else:
                    print("Invalid input: Please enter a 'y' or 'n' in order to continue.")
                    continue
        else:
            with open('PROGRESS_REPORT.save','w') as save_progress:
                save_file_lines=save_progress.write(f"{file_name}\n{URL}\n{from_page}\n{to_page}\n{mode}")
                save_progress.close()

if continue_mode=="n":
    x='w'
    file_name=input("Please enter a file name to create a new csv file to store your scraped data: ").strip()
    while True:
        approach=input("Do you want a targeted approach? [y/n]: ").strip()
        if approach.lower()=='y':
            from_page=int(input('Which page would you like to start scraping from?: '))
            to_page=int(input('Which page would you like to end scraping at?: '))
            targeted=True
            mode=1
            break
        elif approach.lower()=='n':
            from_page=1
            to_page=0
            targeted=False
            mode=0
            break
        else:
            print('Please provide valid input.')
            continue
    name_of_state=input('Please enter the name of state for which you would like to scrape results for?: ').strip()
    type_of_coverage=int(input("What kind coverage are you looking for? Please enter:\n'1' for individual or family\n'2' for Medicaid or CHIP\n'3' for Small businesses\n").strip())
    type_of_help=int(input("What type of help are you looking for? Please enter:\n'1' for All help\n'2' for Agent or broker\n'3' for Assister\n").strip())
    number_of_years=int(input("Please enter the number of years served by the service provider. Entry must be between 1 to 10 or enter any other number for default filter: ").strip())
    days_of_availability=int(input("What days would you like for service provider to be available on? Please enter:\n'1' for Weekdays\n'2' for Weekends\n'3' for Both Weekdays and Weekends\n").strip())
    times_of_availability=int(input("What time would you like for service provider to be available on? Please enter:\n'1' for before 9am\n'2' for 9am to 5pm\n'3' for after 5pm\n").strip())

elif continue_mode=="y":
    x='a'

############################################### - SCRAPING INITIALIZATION - #######################################################################################
# This part of the code configures the webdriver,URL,creates a .csv file to save the results and also sets up other initial conditions to begin scraping.

options = uc.ChromeOptions()
options.add_experimental_option('prefs', { 'extensions.ui.developer_mode': True })
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
options.add_argument("--start-maximized")
driver = uc.Chrome(use_subprocess=True, options=options)

page_number=from_page

if continue_mode=="n":
    URL=HealthcareGovURL(name_of_state,page_number).apply_filters(type_of_coverage,type_of_help,number_of_years,days_of_availability,times_of_availability)

driver.get(URL)
DataCollector.page_initialization(driver)
total_pages=DataCollector.total_pages(driver)

page_to=to_page
if targeted==True:
    if page_number>total_pages or page_to>total_pages or page_to<=page_number or page_to<1 or page_number<1:
        print('Pages out of range.')
        exit()

with open(f'{file_name}.csv',x,newline="") as f:
    csv_writer=DictWriter(f, fieldnames=['NAME','PHONE','EMAIL','TYPE','YEARS_SERVED'])
    if continue_mode=='n':
        csv_writer.writeheader()

############################################### - SCRAPING DATA FROM THE WEBPAGE - ######################################################################################################################################
# This part of the code collects data from the wepages, one after another using the DataCollector class and saves it in .csv file. It also tracks and saves progress of the scraping session in a .save file format.

    while True:
        info_list=DataCollector.page_contents(driver)
        if len(info_list)==0:
            print("No elemnts found.")
            break
        for info in info_list:
            profile_info=DataCollector.compile_record(info)
            csv_writer.writerow({'NAME':profile_info[0],'PHONE':profile_info[1],'EMAIL':profile_info[2],'TYPE':profile_info[3],'YEARS_SERVED':profile_info[4]})
        with open('PROGRESS_REPORT.save','w') as save_progress:
            URL=f'https://localhelp.healthcare.gov/results?q=LOUISIANA&lat=0&lng=0&city=&state=LA&zip_code=&mp=FFM&page={page_number+1}&coverage=individual&type=agent&type=multistate&type=assister&type=statewide&yearsOfService=5&days=mon&days=tue&days=wed&days=thu&days=fri&days=sat&days=sun&hours=night'
            save_file_lines=save_progress.write(f"{file_name}\n{URL}\n{page_number}\n{page_to}\n{mode}")

        if targeted==True:
            if page_number>=page_to:
                os.remove('PROGRESS_REPORT.save')
                break
        elif targeted==False:
            if page_number==total_pages:
                os.remove('PROGRESS_REPORT.save')
                break

        driver.find_element(By.TAG_NAME,"body").send_keys(Keys.END)
        time.sleep(2)
        try:
            page_number+=1
            WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//span[@class='ds-c-button ds-c-button--ghost ds-c-pagination__current-page']")))
            current_page=int(driver.find_element(By.XPATH,"//span[@class='ds-c-button ds-c-button--ghost ds-c-pagination__current-page']").text.replace(',','').strip())
            WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//a[@aria-label='Next Page']")))
            driver.find_element(By.XPATH,"//a[@aria-label='Next Page']").click()
            tries=0
            while tries>=5:
                if current_page==page_number:
                    break
                time.sleep(3)
                current_page=int(driver.find_element(By.XPATH,"//span[@class='ds-c-button ds-c-button--ghost ds-c-pagination__current-page']").text)
                tries+=1
        except:
            break
