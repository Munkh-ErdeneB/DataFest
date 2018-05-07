"""
    Author: Munkh-Erdene Baatarsuren 
    Data Source: Bureau of Labor Statistics 
    Date: 03/24/2018 
"""
import pandas as pd 
import sys 
import operator 
import csv
import pprint

class Dfest(object):
    
    def labor_data(self):
        labor_states = {} 
        labor_states["AL"] = 82378
        labor_states["AK"] = 26220
        labor_states["AZ"] = 157747
        labor_states["AR"] = 50413
        labor_states["CA"] = 866372
        labor_states["CO"] = 91834
        labor_states["CT"] = 86384
        labor_states["DE"] = 21694
        labor_states["DC"] = 23740
        labor_states["FL"] = 397032
        labor_states["GA"] = 228219
        labor_states["HI"] = 14670
        labor_states["ID"] = 25163
        labor_states["IL"] = 318122
        labor_states["IN"] = 113473
        labor_states["IA"] = 49267
        labor_states["KS"] = 52249
        labor_states["KY"] = 93188
        labor_states["LA"] = 99639
        labor_states["ME"] = 22048
        labor_states["MD"] = 130611
        labor_states["MA"] = 128878
        labor_states["MI"] = 230939
        labor_states["MN"] = 101630
        labor_states["MS"] = 60933
        labor_states["MO"] = 111386
        labor_states["MT"] = 21531
        labor_states["NE"] = 29309
        labor_states["NV"] = 71981
        labor_states["NH"] = 19431
        labor_states["NJ"] = 213490
        labor_states["NM"] = 55772
        labor_states["NY"] = 454939
        labor_states["NC"] = 221849
        labor_states["ND"] = 10905
        labor_states["OH"] = 281000
        labor_states["OK"] = 76235
        labor_states["OR"] = 87979
        labor_states["PA"] = 309542
        labor_states["RI"] = 25118
        labor_states["SC"] = 97879
        labor_states["SD"] = 15555
        labor_states["TN"] = 106726
        labor_states["TX"] = 537688
        labor_states["UT"] = 50150
        labor_states["VT"] = 10050
        labor_states["VA"] = 156280
        labor_states["WA"] = 176864
        labor_states["WV"] = 42251
        labor_states["WI"] = 100861
        labor_states["WY"] = 12105
        
        return labor_states

    def compute(self):
        indeed = pd.read_csv("dataFestReleaseFinal_3_23.csv")
        normalized_dict  = self.labor_data() 
        pro = "pro" 
        license = "license" 
        free = "free" 
        rate_dict = {} 
        number_dict = {} 
        for index, row in indeed.iterrows():
            if row["higherEducationRequirementsJob"] == 1:
                state_ = row["admin1"]
                if pro not in rate_dict:
                    rate_dict[pro] = {}
                    number_dict[pro] = {} 
                    if state_ in normalized_dict:
                        rate_dict[pro][state_] = row["applies"]
                        number_dict[pro][state_] = 1
                elif pro in rate_dict:
                    if state_ in normalized_dict and state_ in rate_dict[pro]:
                        rate_dict[pro][state_] += row["applies"]
                        number_dict[pro][state_] += 1
                    elif state_ in normalized_dict and state_ not in rate_dict[pro]:
                        rate_dict[pro][state_] = row["applies"]
                        number_dict[pro][state_] = 1
            elif row["higherEducationRequirementsJob"] == 0 and row["licenseRequiredJob"] == 1: 
                state_ = row["admin1"]
                if license not in rate_dict:
                    rate_dict[license] = {}
                    number_dict[license] = {} 
                    if state_ in normalized_dict:
                        rate_dict[license][state_] = row["applies"]
                        number_dict[license][state_] = 1
                elif license in rate_dict:
                    if state_ in normalized_dict and state_ in rate_dict[license]:
                        rate_dict[license][state_] += row["applies"]
                        number_dict[license][state_] += 1
                    elif state_ in normalized_dict and state_ not in rate_dict[license]:
                        rate_dict[license][state_] = row["applies"]
                        number_dict[license][state_] = 1
            elif row["higherEducationRequirementsJob"] == 0 and row["licenseRequiredJob"] == 0:    
                state_ = row["admin1"]
                if free not in rate_dict:
                    rate_dict[free] = {}
                    number_dict[free] = {} 
                    if state_ in normalized_dict:
                        rate_dict[free][state_] = row["applies"]
                        number_dict[free][state_] = 1
                elif free in rate_dict:
                    if state_ in normalized_dict and state_ in rate_dict[free]:
                        rate_dict[free][state_] += row["applies"]
                        number_dict[free][state_] += 1
                    elif state_ in normalized_dict and state_ not in rate_dict[free]:
                        rate_dict[free][state_] = row["applies"]
                        number_dict[free][state_] = 1
        
        for k in rate_dict:
            for st in rate_dict[k]:
                rate_dict[k][st] = rate_dict[k][st]/normalized_dict[st]
                number_dict[k][st] = number_dict[k][st]/normalized_dict[st] 
        """
        max_num = {} 
        max_rate = {} 
        for st_ in normalized_dict:
            d_num = {}
            d_rate = {}
            lic_num = "lic_num"
            lic_rate = "lic_rate" 
            pro_num = "pro_num"
            pro_rate = "pro_rate"
            free_num = "free_num"
            free_rate = "free_rate" 
            
            num_dict = {} 
            num_dict[lic_num] = 2 
            num_dict[pro_num] = 3 
            num_dict[free_num] = 1 

            r_dict = {} 
            r_dict[lic_rate] = 2 
            r_dict[pro_rate] = 3 
            r_dict[free_rate] = 1 

            if st_ in number_dict[license]:
                d_num[lic_num] = number_dict[license][st_]
                d_rate[lic_rate] = rate_dict[license][st_]
            else:
                d_num[lic_num] = 0 
                d_rate[lic_rate] = 0 

            if st_ in number_dict[pro]:
                d_num[pro_num] = number_dict[pro][st_]
                d_rate[pro_rate] = rate_dict[pro][st_]
            else:
                d_num[pro_num] = 0 
                d_rate[pro_rate] = 0 

            if st_ in number_dict[free]:
                d_num[free_num] = number_dict[free][st_]
                d_rate[free_rate] = rate_dict[free][st_]
            else:
                d_num[free_num] = 0 
                d_rate[free_rate] = 0 
            
            max_n = max(d_num.items(), key=operator.itemgetter(1))[0]
            max_r = max(d_rate.items(), key=operator.itemgetter(1))[0]
            
            max_num[st_] = num_dict[max_n]
            max_rate[st_] = r_dict[max_r]
        """
        
        num_rank = {}  
        rate_rank = {}
        list_help = ["pro", "license", "free"]

        for name in list_help:
            num_rank[name] = []
            rate_rank[name] = [] 
            for i in range(len(number_dict[name])):
                max_n = max(number_dict[name].items(), key=operator.itemgetter(1))[0]
                num_rank[name].append(max_n)
                del number_dict[name][max_n]
            for i in range(len(rate_dict[name])):
                max_r = max(rate_dict[name].items(), key=operator.itemgetter(1))[0]
                rate_rank[name].append(max_r)
                del rate_dict[name][max_r]
        
        loc_dict = {} 
        for namae in list_help:
            loc_dict[namae] = {} 
            for state in num_rank[namae]:
                loc_dict[namae][state] = num_rank[namae].index(state) - rate_rank[namae].index(state) 


        with open('easy.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["state", "more_app(+)|more_job(-)"])
            for key, value in loc_dict["free"].items():
                writer.writerow([key, value]) 
        with open('license.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["state", "more_app(+)|more_job(-)"])
            for key, value in loc_dict["license"].items():
                writer.writerow([key, value]) 

        with open('higher_education.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["state", "more_app(+)|more_job(-)"])
            for key, value in loc_dict["pro"].items():
                writer.writerow([key, value]) 

if __name__ == "__main__":
    wp = woop() 
    wp.compute()
