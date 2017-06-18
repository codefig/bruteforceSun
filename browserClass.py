from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import * 


import os
import time

class browserClass(QThread):
	def __init__(self):
		QThread.__init__(self)
		self.login_page = "login_page"
		self.login_title = "login_title"
		self.username = ""
		self.password = ""
		self.isLoggedIn = False
		self.isSuntrust = False
		self.resultList = []
		self.chromePath = "config"
		self.browser = webdriver.Chrome(os.path.join(self.chromePath, 'chromedriver.exe'))

	def run(self):
		''' The run method inside the QThread instance '''
		self.result  = self.browse_url()
		self.emit(SIGNAL("DONEWITHMAIL"), self.result[0], self.result[1], self.result[2])

	def set_details(self, username, password):
		''' sets the username and password to use on the url '''
		self.username = username
		self.password = password

	def browse_url(self):
		''' browse the url and find the elements on the page using the 
			self.username and self.password variable '''

		# print("trying the browser class : ")
		# self.resultList.insert(0, self.username)
		# self.resultList.insert(1, self.isLoggedIn)
		# self.resultList.insert(2, self.password)
		try:
			print("trying the browser : ")
			self.browser.implicitly_wait(30)
			self.browser.get(self.login_page)
			self.element = self.browser.find_element_by_id("userId")
			self.element.send_keys(self.username)
			self.element = self.browser.find_element_by_id("password")
			self.element.send_keys(self.password)
			self.element.send_keys(Keys.RETURN)
			#do the watiing process
			self.wait = WebDriverWait(self.browser,10)
			page_loaded = self.wait.until_not(lambda browser: self.browser.current_url == self.login_page)
			ans = str(self.browser.title).lower() == self.login_title.lower()
			if ans:
				self.isLoggedIn = False
			else:
				self.isLoggedIn = True
			self.resultList.insert(0, self.username)
			self.resultList.insert(1, self.isLoggedIn)
			self.resultList.insert(2, " ")
		except Exception as e:
			self.resultList.insert(0, str(e))
			self.resultList.insert(1, str(self.username))
			self.resultList.insert(2, self.isLoggedIn)
		#if there are no errors
		# print("browserClass : " , self.resultList)
		self.browser.close()
		return self.resultList
	def get_details(self):
		''' return the list of results found '''
		return self.resultList

	def close_browser(self):
		''' dummy function to force close the browser '''
		self.browser.close()
