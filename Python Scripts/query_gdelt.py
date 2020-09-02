"""
Created on Mon Nov 27 12:22:41 2017

The original code is obtained from 
https://q-a-assistant.com/computer-internet-technology/178212_postgresql-query-taking-too-long-via-python.html
on 11/27/2017.

The file connects to PostgresSQL for GDELT data, query records and save text of
each queried record to text files.

The file supports PostgresSQL for GDELT data, and there are some assumptions
being made here:
    1. the url for each row of record is expected to be at 60 that is 
    hard-coded in code below
    2. the SQL statements are somewhat hard-coded in the code below
    3. there is at least one column in the SQL table where cameo code reside
    
When using sql_query or sql_query3:    
    Note that number of text documents extracted and saved may be less than the 
    number of queries asked for, this is due to some unsuccessful downloads of 
    the text documents from url. Consider running sql_query2, where all records 
    are queried so enough records are ensured (but this approach may be 
    time-consuming).

"""

#!/usr/bin/env python
import os
import sys
import psycopg2
import scrape # a python files
from psycopg2 import sql
#from bs4 import BeautifulSoup

def sql_query(conn, numQueries):
    # here we query based on number of queries needed, independent of cameo code
        
    cur = conn.cursor()
    cur.execute('select * from public.export', (numQueries,))
    
    print('Query done, proceed next')


    return cur.fetchall()


def sql_query2(conn, cameoCode, cameoCodeColName):
    # here we query based on selection of cameo code
        
    cur = conn.cursor()
    cur.execute(sql.SQL("SELECT * FROM public.export WHERE {} = %s").format(sql.Identifier(cameoCodeColName)), 
                (cameoCode,))
    
    print('Query done, proceed next')

    return cur.fetchall()

def sql_query3(conn, numQueries, cameoCode, cameoCodeColName):
    # here we query based on selection of cameo code with numQueries specified
        
    cur = conn.cursor()
    cur.execute(sql.SQL("SELECT * FROM public.export WHERE {} = %s limit %s").format(sql.Identifier(cameoCodeColName)), 
                (cameoCode, numQueries))
    
    print('Query done, proceed next')

    return cur.fetchall()


def main(connectServer, sqlQuery, outPath):
    
    # connect to the server containing GDELT data
    myConnection = psycopg2.connect(host=connectServer['host'], user=connectServer['user'], 
                                    password=connectServer['password'], dbname=connectServer['dbname'], 
                                    port=connectServer['port'])
    
    # call sql_query, sql_query2 or sql_query3
    query = sqlQuery['query']
    if query == 1:
        results = sql_query(myConnection, sqlQuery['numQueries'])
    
    elif query == 2:
        results = sql_query2(myConnection, sqlQuery['cameoCode'],
                             sqlQuery['cameoCodeColName'])
    elif query == 3:
        results = sql_query3(myConnection, sqlQuery['numQueries'], sqlQuery['cameoCode'],
                             sqlQuery['cameoCodeColName'])
    else:
        sys.exit("Error: Specify either 1, 2 or 3 for the query")
    
    totalQueries = len(results)
    numQueries = sqlQuery['numQueries']
    numDigits = len(str(numQueries))
    formatDigits = '0' + str(numDigits) + 'd'
    
    if not os.path.exists(outPath):
        os.makedirs(outPath)  
    
    # obtain text for each query and save the text
    print('Start saving the text ...')
    
    saveURL = []
    cameoCodeColIndex = sqlQuery['cameoCodeColIndex']
    
    if outPath[-1] != os.sep:
        # add a file separator here
        outPath = outPath + os.sep
            
    f1 = open(outPath+'cameo.txt', 'wb')
 
    # start the query loop till all the there are successful numQueries text
    # documents
    cameoCode = sqlQuery['cameoCode']
    count = 1
    queryNumber = -1
    
    while count <= numQueries and queryNumber < totalQueries:
        
        # go through the records
        queryNumber += 1
        
        try:
            # the 60th position contains the url for GDELT data
            url = results[queryNumber][60]
            cameo = results[queryNumber][cameoCodeColIndex]
            
            # proceed to extract the text if the url is new only
            if url not in saveURL:
                # this is a new url, so proceed
                
                # save the url to ensure there is no duplicate
                saveURL.append(url)
                
                # extrac the text
                article = scrape.GdeltArticle(url)
                #article.print_results()
                text = article.results['text']
                
                # save the text and cameo code
                if text != '':
                    # save the text
                    savePath = outPath + 'cameo' + cameoCode + '_document' + format(count, formatDigits) + '.txt'
                    f2 = open(savePath, 'wb')
                    f2.write(text.encode('utf-8'))
                    f2.close()
                    
                    # save the caemo code
                    saveCameo = cameo + '\n'
                    f1.write(saveCameo.encode('utf-8'))
                    
                    print(count)
                    count += 1
        except:
            continue
        
    f1.close()
    
    print('Queries done!')
    
    return


if __name__ == "__main__":
    
    connectServer = {}
    
    # specify input parameter for connecting to Trevor's PostgresSQL server
    connectServer['host'] = '10.51.4.174'
    connectServer['user'] = 'admin'
    connectServer['password'] = 'password'
    connectServer['dbname'] = 'gdelt'
    connectServer['port'] = 23518
    
    # specify additional parameters for the query
    sqlQuery = {}
    sqlQuery['query'] = 2 # 1 for running sql_query, 2 for sql_query2, 3 for sql_query3
    sqlQuery['numQueries'] = 5000
    sqlQuery['cameoCode'] = '09' # the 2 or 3-digit cameo code that is needed, for sql_query2 and sql_query3
    sqlQuery['cameoCodeColName'] = 'EventRootCode' # column name of the cameo code to extract, for sql_query2 and sql_query3
    sqlQuery['cameoCodeColIndex'] = 28 # column index of the cameo code to extract, for sql_query2 and sql_query3
    
    # specify additional parameters for saving the documents
    # outPath will be created if does not exist
    #outPath = '/Users/thuang38/Documents/work/auto_ontology/test'
    outPath = '/Volumes/Projects/xdata/data/gdelt/cameo_09_n_15000_v2'
    
    # call the main function
    main(connectServer, sqlQuery, outPath)
      