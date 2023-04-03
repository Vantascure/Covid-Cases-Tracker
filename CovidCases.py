import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

url = 'https://www.worldometers.info/coronavirus/'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# t = table
t_class = 'table table-bordered table-hover main_table_countries'
t_query = soup.find_all('table', class_=t_class)[0]
t_body_query = t_query.find('tbody')
t_row_query = t_body_query.find_all('tr')

countries_list = []
country_info_list = []

# Add information to lists
for x in range(8, 229):
    countries_list.append(t_row_query[x].find_all('td')[1].text)
    country_info_list.append({
        'Name': t_row_query[x].find_all('td')[1].text,
        'Confirmed': t_row_query[x].find_all('td')[2].text,
        'Deaths': t_row_query[x].find_all('td')[4].text,
        'Recovered': t_row_query[x].find_all('td')[6].text,
        'Infected': t_row_query[x].find_all('td')[8].text
    })

# Search list for case numbers
def search_info(*args):
    country_entry.selection_clear()
    for x in range(len(country_info_list)):
        if country_info_list[x]['Name'] == country_var.get():
            num_of_cases = country_info_list[x]
            def percent(case_type):
                num_1 = num_of_cases[case_type].strip(' ')
                num_2 = num_of_cases['Confirmed'].strip(' ')

                if ',' in num_1:
                    num_1 = num_1.replace(',', '')
                
                if ',' in num_2:
                    num_2 = num_2.replace(',', '')

                if num_1.isdigit() and num_2.isdigit():
                    answer = round((int(num_1) / int(num_2)) * 100, 1)
                    return f"({answer}%)"
                else:
                    return ""

            confirmed_var.set(f"Confirmed: {num_of_cases['Confirmed']}")
            infected_var.set(f"Infected: {num_of_cases['Infected']} {percent('Infected')}")
            deaths_var.set(f"Deaths: {num_of_cases['Deaths']} {percent('Deaths')}")
            recovered_var.set(f"Recovered: {num_of_cases['Recovered']} {percent('Recovered')}")

countries_list.sort()

root = tk.Tk()
root.title("Covid Cases Tracker")

mainframe = ttk.Frame(root, padding='5 5 5 5')
mainframe.grid(row=0, column=0, sticky='N, E, W, S')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

country_var = tk.StringVar()
country_entry = ttk.Combobox(mainframe, textvariable=country_var)
country_entry['values'] = countries_list
country_entry.state(['readonly'])
country_entry.bind('<<ComboboxSelected>>', search_info)
country_entry.current(countries_list.index('Malaysia'))
country_entry.grid(row=0, column=0)

confirmed_var = tk.StringVar()
confirmed_label = ttk.Label(mainframe, textvariable=confirmed_var)
confirmed_label.grid(row=1, column=0)

infected_var = tk.StringVar()
infected_label = ttk.Label(mainframe, textvariable=infected_var)
infected_label.grid(row=2, column=0)

deaths_var = tk.StringVar()
deaths_label = ttk.Label(mainframe, textvariable=deaths_var)
deaths_label.grid(row=3, column=0)

recovered_var = tk.StringVar()
recovered_label = ttk.Label(mainframe, textvariable=recovered_var)
recovered_label.grid(row=4, column=0)

# Call function to search case numbers for default country
search_info()

root.mainloop()