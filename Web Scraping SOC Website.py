from bs4 import BeautifulSoup
import requests
import pandas as pd

main_page = requests.get('https://itc.gymkhana.iitb.ac.in/wncc/soc/').text
main_soup = BeautifulSoup(main_page, 'lxml')

# findind the div holding all projects
project_divs = main_soup.find_all('div', class_ = 'col-lg-4 col-6 mb-4 shuffle-item')

# list to hold various fields of data
project_names = []
domain_list = []
mentors_list = []
mentors_num_list = []
mentees_num_list = []
link_list = []

for elements in project_divs:                       # looping through the projects one by one

    domain = eval(elements['data-groups'])[0]       # domain of the project

    # link to the page of the individual project
    link = 'https://itc.gymkhana.iitb.ac.in/' + elements.div.a['href']
    project_page = requests.get(link).text
    project_soup = BeautifulSoup(project_page, 'lxml')

    # extracting the project name, from the heading tag h2
    project_name = project_soup.find('h2').get_text()

    # extracting all unordered list elements
    details = project_soup.find_all('ul')

    # in each project, the 4th unordered list element contains the mentors name(s)
    # and the 5th unordered list element contains the no. of mentees
    mentors_html = details[3].find_all('p')
    mentees_html = details[4].find_all('p')

    mentors = ''                                # string for mentors name(s)
    mentors_num = 0
    for mentor in mentors_html:
        name = mentor.get_text()

        # removing the roll no. from the name
        while '(' in name and ')' in name:
            start_index = name.index('(')
            end_index = name.index(')')
            name = name[:start_index] + name[end_index + 1:]
        
        name = name.replace(' &', ',')          # replacing '&' with ','

        mentors += (name).title() + ', '        # concatenating all mentor names together
        mentors_num += 1                        # incrementing mentor number by 1
    
    for mentee in mentees_html:
        mentees_num_list.append(mentee.get_text())
    
    mentors = mentors.strip(', "')              # removing the trailing , from mentors name

    # adding them up to their respective lists
    domain_list.append(domain)
    project_names.append(project_name)
    mentors_list.append(mentors)
    mentors_num_list.append(mentors_num)
    link_list.append(link)

# creating a pandas dataframe using the created lists
dataframe = pd.DataFrame({
    'Project Name': project_names,
    'Domain': domain_list,
    'Mentors': mentors_list,
    'Mentors Number': mentors_num_list,
    'Mentees Number': mentees_num_list,
    'Link': link_list
})

# some processing of data
dataframe = dataframe.replace('', '-')
dataframe = dataframe.drop_duplicates()
dataframe = dataframe.dropna()

# exporting the dataframe to a CSV file
dataframe.to_csv('SOC Data.csv')
