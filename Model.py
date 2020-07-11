from requests import get
from bs4 import BeautifulSoup
from requests import post
import smtplib
import sqlite3
from sqlite3 import Error

import hashlib
import email.message

import pickle

def FetchData(): #scrape data and store in db
    
    try:
        url = 'https://www.worldometers.info/coronavirus/'
        response = get(url)
        
        if response.ok:       
            html_soup = BeautifulSoup(response.text, 'html.parser')

            lastchecked=html_soup.find(id='page-top').findNext('div').text
            
            table=html_soup.find(id='main_table_countries_today')
            rows = table.find('tbody').find_all('tr')

            conn = create_connection()

            with conn:
                
                for tr in rows:
                    col=tr.find_all('td')
                    countryname=col[1].text
                    if '\n' not in countryname:
                        deaths=col[4].text.replace(',','').strip()
                        confirmed=col[2].text.replace(',','').strip()
                        recovered=col[6].text.replace(',','').strip()

                        if deaths.isnumeric()==False:
                            deaths=None
                        if confirmed.isnumeric()==False:
                            confirmed=None
                        if recovered.isnumeric()==False:
                            recovered=None
                        
                        #create_db(conn, (countryname,deaths,confirmed,recovered,lastchecked))
                        update_db(conn, (deaths, confirmed, recovered, lastchecked,countryname))
                
            
            return(True)
            
        else:
            return False
        
    except Exception as e:
        return False


def create_connection():
    db_file="pythonsqlite.db"

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_db(conn, project): #append data to db

    sql = ''' INSERT INTO project(countryName,deaths,confirmed,recovered,lastchecked)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)


        
def initdb(): #create table in db

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS project (
                                        id integer PRIMARY KEY,
                                        countryName text NOT NULL,
                                        deaths int,
                                        confirmed int,
                                        recovered int,
                                        lastchecked text
                                        
                                    ); """

    # create a database connection
    conn = create_connection()

    # create table
    if conn is not None:
        # create table
        try:
            c = conn.cursor()
            c.execute(sql_create_projects_table)
        except Error as e:
            print(e)

    else:
        print("Error! cannot create the database connection.")


def update_db(conn, task): #update data in db

    sql = ''' UPDATE project
              SET deaths = ? ,
                  confirmed = ? ,
                  recovered = ? ,
                  lastchecked = ?
              WHERE countryName = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def select_by_country(conn,order):
    cur = conn.cursor()
    cur.execute("SELECT * FROM project ORDER BY countryName {0}".format(order))
    rows = cur.fetchall()

    return rows

        
def select_by_deaths(conn,order):
    cur = conn.cursor()
    cur.execute("SELECT * FROM project ORDER BY deaths {0}".format(order))
    rows = cur.fetchall()
    
    return rows

def select_by_confirmed(conn,order):
    cur = conn.cursor()
    cur.execute("SELECT * FROM project ORDER BY confirmed {0}".format(order))
    rows = cur.fetchall()

    return rows

def select_by_recovered(conn,order):
    cur = conn.cursor()
    cur.execute("SELECT * FROM project ORDER BY recovered {0}".format(order))
    rows = cur.fetchall()

    return rows

def select_top5_deaths(conn):
    cur = conn.cursor()
    cur.execute("SELECT countryName,deaths FROM project ORDER BY deaths DESC LIMIT 5 OFFSET 1")
    rows = cur.fetchall()

    return rows

def select_top5_recovered(conn):
    cur = conn.cursor()
    cur.execute("SELECT countryName,recovered FROM project ORDER BY recovered DESC LIMIT 5 OFFSET 1")
    rows = cur.fetchall()

    return rows

def select_top5_confirmed(conn):
    cur = conn.cursor()
    cur.execute("SELECT countryName,confirmed FROM project ORDER BY confirmed DESC LIMIT 5 OFFSET 1")
    rows = cur.fetchall()

    return rows


#DESC ASC

################################################################################################
def posttoserver(name,email,msg,stars):
    try:  
        url='https://gfarah.000webhostapp.com/esibpythonapp/script.php'
        myobj = {'name':name,'emailaddress': email,'message':msg,'stars':stars}
        x = post(url, data = myobj)

        return x.text
    except Exception as e:
        return False


def getfromserver(username,password):
    try:  
        url='https://gfarah.000webhostapp.com/esibpythonapp/script2.php'
        myobj = {'username':username,'password': password}
        x = post(url, data = myobj)
        
        response=x.json()
        return response
        
    except Exception as e:
        return False



def sendmail(receiver,sender,password):

    body = """\

    Hello,
    Thank you for your message. We appreciate you sharing your thoughts.
    This is an automated message sent from Python."""

    msg = email.message.Message()
    msg['Subject'] = 'ESIB 19/20 TP'    
    msg['From'] = sender
    msg['To'] = receiver
    msg.add_header('Content-Type', 'text/plain')
    msg.set_payload(body)

    smtpserver = smtplib.SMTP('smtp.gmail.com',587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(sender,password)

    smtpserver.sendmail(sender,receiver,msg.as_string())
    print('sent')
    smtpserver.close()


################################################################################################
class Location:
    country='Lebanon'
    def __init__(self):
        self.getLocation()
    @classmethod
    def getLocation(cls):
        try:
            url = 'https://whatismycountry.com/'
            response = get(url)
                    
            if response.ok:       
                html_soup = BeautifulSoup(response.text, 'html.parser')
                
                allH4=html_soup.find_all('h4')
                #country=allH4[1].text
                Location.country=allH4[1].text

                if Location.country=='United States':
                    Location.country='United States of America'
                    
                return True
            
            else:
                return False
            
        except Exception as e:
            return False
        


################################################################################################



def FetchNumbers():
    
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_emergency_telephone_numbers'
        response = get(url)
        
        if response.ok:
            data={}
            html_soup = BeautifulSoup(response.text, 'html.parser')
            
            tables=html_soup.find_all('table')

            
            for table in tables:
                rows = table.find('tbody').find_all('tr')
                for row in rows:
                    
                    tds=row.find_all('td')
                    if len(tds)==5:
                        countryname=tds[0].text.strip().split('[')[0]
                        police=tds[1].text.strip().split('[')[0]
                        ambulance=tds[2].text.strip().split('[')[0]
                        fire=tds[3].text.strip().split('[')[0]
                        
                        data[countryname]={'police':police,'ambulance':ambulance,'fire':fire}
                    
                    if len(tds)==3:
                        countryname=tds[0].text.strip().split('[')[0]
                        police=tds[1].text.strip().split('[')[0]
                        ambulance=tds[1].text.strip().split('[')[0]
                        fire=tds[1].text.strip().split('[')[0]
                        
                        data[countryname]={'police':police,'ambulance':ambulance,'fire':fire} 
                    if len(tds)==4:
                        if tds[1].has_attr('colspan'):
                            countryname=tds[0].text.strip().split('[')[0]
                            police=tds[1].text.strip().split('[')[0]
                            ambulance=tds[1].text.strip().split('[')[0]
                            fire=tds[2].text.strip().split('[')[0]
                            
                            data[countryname]={'police':police,'ambulance':ambulance,'fire':fire}
                        
                        elif tds[2].has_attr('colspan'):
                            countryname=tds[0].text.strip().split('[')[0]
                            police=tds[1].text.strip().split('[')[0]
                            ambulance=tds[2].text.strip().split('[')[0]
                            fire=tds[2].text.strip().split('[')[0]
                            
                            
                            data[countryname]={'police':police,'ambulance':ambulance,'fire':fire}
                        else:#lithunia malaysia the bahamas
                            countryname=tds[0].text.strip().split('[')[0]
                            police=tds[1].text.strip().split('[')[0]
                            ambulance=tds[1].text.strip().split('[')[0]
                            fire=tds[1].text.strip().split('[')[0]
                            data[countryname]={'police':police,'ambulance':ambulance,'fire':fire}

            open('phoneNumbers.txt', 'w').close()
            with open('phoneNumbers.txt', 'wb') as f:
                pickle.dump(data, f)
            
            
    except Exception as e:
        print(str(e))



def getPhoneNumbers():
    with open('phoneNumbers.txt','rb') as f:
        return pickle.load(f)

###################################################################################
def hashpasswordInit(password):  
    salt=b'Rz9\xbd\xda.\x99y\xf0\xb1E\x13\x15\x18Vf\xa5\xbf\xc4\xb0\x98!\x05B\x92"?{?\xbc\xa9\xa8'

    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000 
    )
    return {'salt':str(salt),'key':str(key)}

###################################################################################

def FetchLatLong(): #scrape data and store in db
    
    try:
        url = 'http://www.csgnetwork.com/llinfotable.html'
        response = get(url)
        
        if response.ok:       
            html_soup = BeautifulSoup(response.text, 'html.parser')

            
            table=html_soup.find_all('table')[5]
            
            rows = table.find_all('tr')

            countries={}
            for tr in rows:
                tds=tr.find_all('td')
                countryname=tds[0].text
                capital=tds[1].text
                lat=tds[2].text
                long=tds[3].text
                
                if countryname!='Country':
                    if countryname=='United States\r\n  of America':
                        countryname='USA'
                    if countryname=='United Kingdom of Great Britain and Northern Ireland':
                        countryname='UK'
                    if countryname=='Russian Federation':
                        countryname='Russia'

                    
                    if lat[-1]=='S':
                        a=lat.split("'")[0].replace('°','.')
                        lat=-float(a)
                    else:
                        a=lat.split("'")[0].replace('°','.')
                        lat=float(a)                    
                        
                    if long[-1]=='W':
                        a=long.split("'")[0].replace('°','.')
                        long=-float(a)
                    else:
                        a=long.split("'")[0].replace('°','.')
                        long=float(a)
                    
                    countries[countryname]=[capital,lat,long]

            open('CountriesCoords.txt','w').close()
            f=open('CountriesCoords.txt','wb')
            pickle.dump(countries,f)
            f.close()
        
            
        else:
            return False
        
    except Exception as e:
        return str(e)

def getLatLong():
    with open('CountriesCoords.txt','rb') as f:
        return pickle.load(f)
