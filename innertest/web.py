import requests
from bs4 import BeautifulSoup
import re
import psycopg2

res = requests.get('https://blog.python.org/')
soup = BeautifulSoup(res.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
data=soup.find(re.compile(r'div'),attrs={'class':"post-body"})
# print(data.find("lorem"))



# postgress database
try:
    conn = psycopg2.connect(
        host="0.0.0.0",
        database="pythondata",
        user="postgres",
        password="admin")
    print("sucessfull created database")
except:
    print("I am unable to connect to the database") 

cursor = conn.cursor()






# db_name = 'pythondata'
# db_user = 'postgres'
# db_pass = 'admin'
# db_host = 'postgres_service'
# db_port = '5432'

# # Connecto to the database
# db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
# cursor = create_engine(db_string)




# qes_list=[]
# ans_list=[]
# for row in data.findAll("div"):
#     qes_list.append(row.h2.text)
#     tempstring=""
#     counter=0
#     for i in row.findAll("p"):
#         tempstring=tempstring+"\n"+i.text
#     ans_list.append(tempstring)
# tempstring=""
# for i in range(len(qes_list)):
#     tempstring=tempstring+"\n"+qes_list[i]+"\n"+ans_list[i]+"\n--------------------------------------------------------------------------------------------------\n\n"
#     print(tempstring)

sib = data.find("h3").findNext("p").contents[0]

version_list = []
content_list = []

for row in data.findAll("h3") :
    version_list.append(row.text)
for col in data.findAll("h3") :
    content_list.append(col.find_next_sibling("p").text)

# print(version_list)
# print(content_list)

for i in range(len(version_list)):
    print(version_list[i],"\n",content_list[i],"\n-------------------------------------\n")

# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
try:
    cursor.execute("CREATE TABLE test(id INTEGER PRIMARY KEY,version varchar,content varchar);")   
except:
    print("I can't drop our test database!")


try:
    for i in range(len(version_list)):
        cursor.execute("INSERT INTO test values(%s,%s,%s);", (i+1,version_list[i], content_list[i]))
except:
    print("sorry!!!!!!")



conn.commit()
conn.close()
cursor.close()