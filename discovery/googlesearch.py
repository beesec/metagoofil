import string
import httplib, sys
import myparser
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class search_google:
	def __init__(self,word,limit,start,filetype):
                self.driver = webdriver.Firefox()
		self.word=word
		self.results=""
		self.totalresults=""
		self.filetype=filetype.replace(",", " OR filetype:")
		print self.filetype
		self.server="www.google.com"
		self.hostname="www.google.com"
		self.userAgent="(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
		self.quantity="100"
		self.limit=limit
		self.counter=start
		
	def do_search_files(self):
		self.driver.get("http://"+self.server+"/search?num="+self.quantity+"&start=" + str(self.counter) + "&hl=en&meta=&filter=0&q=filetype:"+self.filetype+"%20inurl:" + self.word)
                try:
                        captcha = self.driver.find_element_by_name("captcha")
                        answer = raw_input("Please enter captcha: ")
                        captcha.clear()
                        captcha.send_keys(answer)
                        captcha.send_keys(Keys.RETURN)
                except:
                        print "No Captcha"
                try:                        
                        self.driver.find_element_by_xpath("//p[@id = 'ofr']/i/a").click()
                except:
                        print "No Link to click for more results"
                try:        
                        elems = self.driver.find_elements_by_xpath("//div[@class = 'g']/div/h3/a")
                        links = [i.get_attribute('href') for i in elems]
                except:
                        print "No Results"
                        pass
                print "control"        
		#self.results = links
                self.results = self.driver.page_source
		self.totalresults+= self.results

	def get_emails(self):
		rawres=myparser.parser(self.totalresults,self.word)
		return rawres.emails()
	
	def get_hostnames(self):
		rawres=myparser.parser(self.totalresults,self.word)
		return rawres.hostnames()
	
	def get_files(self):
		rawres=myparser.parser(self.totalresults,self.word)
		print rawres.fileurls()
		return rawres.fileurls()
	
	def process_files(self):
		#while self.counter < self.limit:
		self.do_search_files()
		print "Done searching"
		#	time.sleep(1)
		#	self.counter+=100
		#	print "\tSearching "+ str(self.counter) + " results..."

