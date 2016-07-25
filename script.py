import urllib
import urllib2
import lxml.html
import json
import httplib2
import re
from lxml.etree import tostring
from urlparse import urljoin
from  more_itertools import unique_everseen
from BeautifulSoup import BeautifulSoup, SoupStrainer
import os
import webbrowser

states_name  = {"albany":"Albany","albuquerque":"Albuquerque","atlanta":"Atlanta","austin":"Austin","baltimore":"Baltimore","birmingham":"Birmingham","boston":"Boston","buffalo":"Buffalo","charlotte":"Charlotte","chicago": "Chicago","cincinnati":"Cincinnati","columbus":"Columbus","dallas":"Dallas","dayton":"Dayton","denver":"Denver","triad":"Greensboro","houston":"Houston","jacksonville":"Jacksonville","kansascity":"Kansas City","losangeles": "Los Angeles","louisville":"Louisville","memphis":"Memphis","milwaukee":"Milwaukee","twincities":"Mpls./St. Paul","nashville":"Nashville","newyork":"New York","orlando":"Orlando","pacific":"Pacific","philadelphia":"Philadelphia","phoenix":"Phoenix","pittsburgh":"Pittsburgh","portland":"Portland","triangle":"Raleigh/Durham","sacramento":"Sacramento","sanantonio":"San Antonio","sanfrancisco":"San Francisco","sanjose":"San Jose","seattle":"Seattle","southflorida":"South Florida","stlouis":"St. Louis","tampabay":"Tampa Bay","washington":"Washington, D.C.","wichita":"Wichita"}

states_count = {"albany":12,"albuquerque":12,"atlanta":75,"austin":33,"baltimore":37,"birmingham":10,"boston":111,"buffalo":12,"charlotte":23,"chicago":3,"cincinnati":20,"columbus":22,"dallas":63,"dayton":9,"denver":44,"triad":12,"houston":57,"jacksonville":15,"kansascity":22,"losangeles":4,"louisville":12,"memphis":9,"milwaukee":11,"twincities":50,"nashville":14,"newyork":6,"orlando":28,"pacific":11,"philadelphia":61,"phoenix":46,"pittsburgh":25,"portland":32,"triangle":29,"sacramento":19,"sanantonio":17,"sanfrancisco":54,"sanjose":79,"seattle":55,"southflorida":51,"stlouis":28,"tampabay":42,"washington":107,"wichita":5}

for z in states_count:
    done = 0
    print z,states_count[z]
    try:
        #---------------------------------------------------------------
        def func1():
            jsonfile = open('relative_url_allcompany_inbusinessdirectory.json', 'w')
            jsonfile1 = open('address_allcompanies.json', 'w')
            jsonfile2 = open('name_allcompanies.json', 'w')

            print "starting"
            ul = 'http://businessdirectory.bizjournals.com/'+z+'/information_technology/page/'
            jsonfile.write('[')
            jsonfile1.write('[')
            jsonfile2.write('[')
            for i in range(1,states_count[z]):
                print str(i)+'/'+str(states_count[z])+' - 1/7'
                connection = urllib.urlopen(ul+str(i))
                dom=lxml.html.fromstring(connection.read())
                for link in dom.xpath('//a/@href'):
                    lnk = link
                    link = link.split("/") 
                    if(3 < len(link)):
                        if(link[3].isdigit()):
                            if(int(link[3]) > 0):
                                json.dump(lnk, jsonfile)
                                jsonfile.write(',')
                for link in dom.xpath("//td[@class='results_td_address']/ul/li/p"):
                    link = link.text.strip()
                    json.dump(' '.join(link.split()), jsonfile1)
                    jsonfile1.write(',')
                for link in dom.xpath("//td[@class='results_td_address']/ul/li/a/span"):
                    link = link.text.strip()
                    json.dump(' '.join(link.split()), jsonfile2)
                    jsonfile2.write(',')
            jsonfile.seek(-1, os.SEEK_END)
            jsonfile1.seek(-1, os.SEEK_END)
            jsonfile2.seek(-1, os.SEEK_END)
            jsonfile2.write(']')
            jsonfile1.write(']')
            jsonfile.write(']')
            jsonfile.truncate()
            jsonfile1.truncate()
            jsonfile2.truncate()
            done = 1
            jsonfile2.close()
            jsonfile1.close()
            jsonfile.close()
            func2()
        #-----------------------------------------

        def func2():
            jsonfile = open('allcompany_url.json', 'w')
            jsonfile1 = open('allcompany_url_name.json', 'w')
            ul = 'http://businessdirectory.bizjournals.com'
            jsonfile.write('[')
            jsonfile1.write('[')
            with open('name_allcompanies.json') as data_file1:
                data1 = json.load(data_file1)
                with open('relative_url_allcompany_inbusinessdirectory.json') as data_file:    
                    data = json.load(data_file)
                    for x in range(len(data)):
                        print str(x)+'/'+str(len(data))+'- 2/7'
                        jsonfile1.write('[')
                        connection = urllib.urlopen(ul+data[x])
                        dom=lxml.html.fromstring(connection.read())
                        for link in dom.xpath("//div[@class='b2secDetails-URL']/ul/li/a/@href"):
                            json.dump(link, jsonfile)
                            jsonfile.write(',')
                            json.dump(link, jsonfile1)
                            jsonfile1.write(',')
                            json.dump(data1[x], jsonfile1)
                        jsonfile1.write(']')
                        jsonfile1.write(',')
            jsonfile.seek(-1, os.SEEK_END)
            jsonfile.truncate()
            jsonfile1.seek(-1, os.SEEK_END)
            jsonfile1.truncate()
            jsonfile.write(']')
            jsonfile1.write(']')
            done = 2
            jsonfile1.close()
            jsonfile.close()
            func3()
        #------------------------------------------------
        def func3():
            http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
            word =  ['Candidates','careers','career','job','listing','join','venture','employment']
            word1 = ['reach','contact']

            jsonfile = open('url_available_career_job.json', 'w')
            jsonfile.write('[')

            with open('allcompany_url.json') as data_file:    
                data =  json.load(data_file)
                for x in range(len(data)):
                    print str(x)+'/'+str(len(data))+'- 3/7'
                    try:    
                        status, response = http.request(data[x])
                        if status.status==200:
                            jsonfile.write('[[')
                            json.dump(data[x], jsonfile)
                            for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
                                if link.has_key('href'):
                                    for j in range(len(word)):
                                        if word[j].lower() in link['href'].lower() or word[j].lower() in link.text.lower():
                                            jsonfile.write(',')
                                            json.dump(urljoin(data[x],link['href']), jsonfile)
                            jsonfile.write('],[')
                            json.dump(data[x], jsonfile)
                            for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
                                if link.has_key('href'):
                                    for j in range(len(word1)):
                                        if word1[j].lower() in link['href'].lower() or word1[j].lower() in link.text.lower():
                                            jsonfile.write(',')
                                            json.dump(urljoin(data[x],link['href']), jsonfile)
                            jsonfile.write(']],')
                    except Exception, e:
                        print "Site is Down -> "+ data[x]+" ("+str(e)+")"
            jsonfile.seek(-1, os.SEEK_END)
            jsonfile.truncate()
            jsonfile.write(']')
            done = 3
            jsonfile.close()
            func4()
        #-----------------------------------------------
        def func4():
            jsonfile = open('url_available_career_job_unique.json', 'w')
            jsonfile.write('[')

            with open('url_available_career_job.json') as data_file:    
                data = json.load(data_file)
                for x in range(len(data)):
                    print str(x)+'/'+str(len(data))+'- 4/7'
                    if(1 < len(data[x][0]) or 1 < len(data[x][1])):
                        data[x][0] = list(unique_everseen(data[x][0]))
                        data[x][1] = list(unique_everseen(data[x][1]))
                        json.dump(data[x], jsonfile)
                        jsonfile.write(',')
            jsonfile.seek(-1, os.SEEK_END)
            jsonfile.truncate()
            jsonfile.write(']')
            done = 4
            jsonfile.close()
            func5()
        #------------------------------------------------
        def func5():
            http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

            ed = []

            edpath = r"seg_words.txt"
            words = open(edpath).read().split()
            for  word in words:
                   ed.append(word)

            td = []
            with open('seg_techwords.json') as data_file:    
                data = json.load(data_file)
                for x in data:
                    td.append(x)

            misl_words = []
            jsonfile = open('company_url_techword.json', 'w')
            jsonfile.write('[')

            with open('url_available_career_job_unique.json') as data_file:    
                data = json.load(data_file)
                for i in range(len(data)):
                    print str(i)+'/'+str(len(data))+'- 5/7'
                    if len(data[i][0]) > 1:
                        for j in data[i][0]:
                            try:
                                status, response = http.request(j)
                                if status.status==200:
                                        site = BeautifulSoup (response.decode('utf-8', 'ignore'))
                                        [s.extract() for s in site(['style', 'script', '[document]', 'head', 'title'])]
                                        visible_text = site.getText()
                                        found = visible_text.encode('ascii','ignore').split()
                                        fnd_list = []
                                        tch_list = []
                                        tch_list.append(data[i][0][0])
                                        for wd in found:
                                            wd = ''.join(e for e in wd if e.isalpha())
                                            if wd.lower() not in ed and wd.lower() not in fnd_list:
                                                if wd.lower() in td:
                                                    if wd.lower() not in tch_list:
                                                        tch_list.append(wd.lower())
                                                else:
                                                    if wd.lower() not in misl_words:
                                                        misl_words.append(wd.lower())
                                        json.dump(tch_list, jsonfile)
                                        jsonfile.write(',')
                            except Exception, e:
                                print "Site is Down -> "+ j+" ("+str(e)+")"
            jsonfile.seek(-1, os.SEEK_END)
            jsonfile.truncate()
            jsonfile.write(']')
            jsonfile1 = open('misl_words.json', 'w')
            json.dump(misl_words, jsonfile1)
            done = 5
            jsonfile1.close()
            jsonfile.close()
            func6()
        #---------------------------------------------
        def func6():
            jsonfile = open('company_latlng.json', 'w')
            jsonfile.write('[')
            ul = 'http://businessdirectory.bizjournals.com'
            with open('relative_url_allcompany_inbusinessdirectory.json') as data_file:    
                data = json.load(data_file)
                for x in range(len(data)):
                    print str(x)+'/'+str(len(data))+'- 6/7'
                    jsonfile.write('[')
                    web = urllib2.urlopen(ul+data[x])
                    dom=lxml.html.fromstring(web.read())
                    flg = False
                    for link in dom.xpath("//div[@class='b2secDetails-URL']/ul/li/a/@href"):
                        if len(link) > 1:
                            flg = True
                            json.dump(link, jsonfile)

                    if flg:
                        rg = re.compile('((?:[a-z][a-z]+))(\\s+)(google\\.maps\\.LatLng)(\\()(\\s+)([+-]?\\d*\\.\\d+)(?![-+0-9\\.])(,)(\\s+)([+-]?\\d*\\.\\d+)(?![-+0-9\\.])(\\))(;)',re.IGNORECASE|re.DOTALL)
                        js_text = re.findall(rg, dom.xpath("//script")[14].text)
                        for i in js_text:
                            for j in range(len(i)):
                                if j == 5 or j == 8:
                                    jsonfile.write(',')
                                    json.dump(i[j], jsonfile)
                        jsonfile.write(']')
                        jsonfile.write(',')
                    else:
                        jsonfile.seek(-1, os.SEEK_END)
                        jsonfile.truncate()

            jsonfile.seek(-1, os.SEEK_END)
            jsonfile.write(']')
            jsonfile.truncate()
            done = 6
            jsonfile.close()
            func7()
        #----------------------------------------------
        def func7():
            dic={}

            print '7/7'
            with open('company_url_techword.json') as data_file:    
                data = json.load(data_file)
                for x in data:
                    if len(x) > 1:
                        if x[0] not in dic:
                            temp = x[0]
                            x = x[1:]
                            dic[temp] = x
                        else:
                            temp = x[0]
                            x = x[1:]
                            tmp = dic[temp]
                            for i in x:
                                if i not in tmp:
                                    tmp.append(i)
                            dic[temp] = tmp

            with open('company_latlng.json') as data_file:    
                data = json.load(data_file)
                for y in range(len(data)):
                    x = data[y]
                    if x[0] in dic:
                        temp = dic[x[0]]
                        x1 = x[1:]
                        temp = x1 + temp
                        dic[x[0]] = temp

            with open('allcompany_url_name.json') as data_file1:    
                data = json.load(data_file1)
                for y in range(len(data)-1):
                    x = data[y]
                    if len(x) > 1:
                        if x[0] in dic:
                            temp = dic[x[0]]
                            x1 = x[1:]
                            temp = x1 + temp
                            dic[x[0]] = temp


            jsonfile = open('final_output_'+z+'.json', 'w')
            jsonfile.write('[')

            for i in dic:
                jsonfile.write('[')
                json.dump(i, jsonfile)
                for j in dic[i]:
                    jsonfile.write(',')
                    json.dump(j, jsonfile)
                jsonfile.write(']')
                jsonfile.write(',')
            jsonfile.seek(-1, os.SEEK_END)
            jsonfile.truncate()
            jsonfile.write(']')
            jsonfile.close()

            print "Scraping completed ! "
            done = 7
        #-----------------------------------------------------------------

    except Exception, e:
        print "Restart -> ("+str(e)+") at process "+str(done+1)
        eval("func"+str(done+1)+"()")

    func1()