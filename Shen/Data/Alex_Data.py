import csv

with open("Solar_Radiation.csv", mode= 'r') as solar_rad:
	reader = csv.reader(solar_rad)
	Solar_Data_List = list(reader)



print("\n \n")
print(Solar_Data_List[1][0][0:3])
print("\n \n")
print(Solar_Data_List[1][0][123:130])

JDA_RAD_List = []

for item in Solar_Data_List[7295:15936]:
	JDA_RAD_List.append([item[0][0:3], item[0][4:9] ,item[0][123:130]])


print(JDA_RAD_List)

