#!/usr/bin/python

OID = '.1.3.6.1.4.1.25359.1'
BASE_OID = OID + '.2.1'
INDEX_OID = OID + '.1'

import sys, commands, re, snmpresponse, math, calendar, time, csv, os

def updatePoolPerf(poolName, poolIndex, allocatedNumber):

    perfFile = "/usr/local/snmp/zpoolUsage.csv"
    if os.path.isfile(perfFile):
      with open(perfFile) as csvfile:
        reader = csv.DictReader(csvfile)
        rownum = 0
        zpoolUsage = []
        for row in reader:
                #print(row['poolname'], row['poolindex'], row['minutes'], row['epoch'], row['lastused'], row['currentused'], row['difference'])
                zpoolUsage.append (row)
                rownum += 1

        epochTime = calendar.timegm(time.gmtime())

        newLine = True

        with open(perfFile, 'w') as csvfile:
                fieldnames = ['poolname', 'poolindex', 'minutes', 'epoch', 'lastused', 'currentused', 'difference']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for i in range(rownum) :
                  if zpoolUsage[i]['poolname'] == poolName :
                    newLine = False
                    if long(epochTime) > long(zpoolUsage[i]['epoch']) + 60 :
                        zpoolUsage[i]['lastused'] = zpoolUsage[i]['currentused']
                        zpoolUsage[i]['currentused'] = allocatedNumber
                        zpoolUsage[i]['epoch'] = epochTime
                        zpoolUsage[i]['difference'] = long(allocatedNumber) - long(zpoolUsage[i]['lastused'])
                        writer.writerow(zpoolUsage[i])
                        newLine = False
                    else :
                        writer.writerow(zpoolUsage[i])
                  else :
                      writer.writerow(zpoolUsage[i])

                if newLine == True :
                        writer.writerow({'poolname':  poolName , 'poolindex': str(poolIndex) , 'currentused': str(allocatedNumber) , 'lastused': str(allocatedNumber) , 'epoch': epochTime, 'difference': '0', 'minutes': '1'})


        csvfile.close()


def readPoolPerf(poolName):

    perfFile = "/usr/local/snmp/zpoolUsage.csv"
    if os.path.isfile(perfFile):
      with open(perfFile) as csvfile:
        reader = csv.DictReader(csvfile)
        zpoolUsage = []
        for row in reader:
                if row['poolname'] == poolName:
                        return row['difference']

      csvfile.close()

updatePoolPerf("tpool",4,35)

poolPerf=readPoolPerf("tpool")

print(poolPerf)
