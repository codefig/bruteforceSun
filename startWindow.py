from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtWebKit import *


import sys
import os
import browserClass
import time 

class startWindow(QMainWindow):
	def __init__(self):
		super(startWindow, self).__init__()
		self.setWindowTitle("Applicationn Name")
		self.setStyleSheet("background-color:#2c3e50")
		self.setGeometry(50,50, 500, 400)
		self.iconBase = "icons"
		self.configBase = "config"
		self.setWindowIcon(QIcon(os.path.join(self.iconBase, "logo.png")))
		self.toolBar = QToolBar("First bar")
		self.toolBar.setStyleSheet("background-color:#95a5a6")
		self.addToolBar(self.toolBar)
		self.emailList = []
		self.passList = []
		self.mailCount = 0
		self.passCount = 0
		self.continueBrute = True 
		


		#create the toolbar actions 
		self.loadEmails = QAction(QIcon(os.path.join(self.iconBase, "at-sign.png")), "Load Emails", self)
		self.loadPasswords = QAction(QIcon(os.path.join(self.iconBase, "application-plus-red.png")),"Load Password", self)
		self.startBrute = QAction(QIcon(os.path.join(self.iconBase, "arrow.png")),"Start", self)
		self.clearEmails = QAction("Clear Email", self)
		self.clearPasswords = QAction("Clear Passwords", self)
		# self.clearStatus = QAction(QIcon(os.path.join(self.iconBase, "terminal.png")),"Clear Results", self)
		self.clearStatus = QAction("Clear Results", self)
		self.stopBrute = QAction(QIcon(os.path.join(self.iconBase, "cross.png")),"stop Application", self)
		self.aboutApplication = QAction(QIcon(os.path.join(self.iconBase, "eye.png")),"Public Disclaimer", self)
		self.addChromePath = QAction(QIcon(os.path.join(self.iconBase, "switch-small.png")),"Configure Chrome Folder", self)
		self.toolBar.addAction(self.loadEmails)
		self.toolBar.addAction(self.loadPasswords)
		self.toolBar.addAction(self.clearStatus)
		self.toolBar.addAction(self.clearEmails)
		self.toolBar.addAction(self.clearPasswords)
		self.toolBar.addAction(self.startBrute)
		self.toolBar.addAction(self.stopBrute)


		#create the status bar 
		self.statusBar = QStatusBar(self)
		self.statusBar.setStyleSheet("background-color:#95a5a6")
		self.setStatusBar(self.statusBar)
		self.statusBar.showMessage("Ready")
		# self.statusBar.setText("that is toog")
		
		#create the menubar 
		self.menuBar = QMenuBar()
		self.firstMenu = self.menuBar.addMenu('&Settings')
		self.configMenu = self.menuBar.addMenu("&Configuration")
		self.helpMenu = self.menuBar.addMenu("&About")
		self.firstMenu.addAction(self.loadEmails)
		self.firstMenu.addAction(self.loadPasswords)
		self.firstMenu.addAction(self.clearStatus)
		self.firstMenu.addSeparator()
		self.firstMenu.addAction(self.clearEmails)
		self.firstMenu.addAction(self.clearPasswords)

		self.configMenu.addAction(self.addChromePath)

		self.helpMenu.addAction(self.aboutApplication)
		self.setMenuBar(self.menuBar)

		#create the central widget
		self.centralWidget = QWidget()


		self.layout = QHBoxLayout()

		self.mailWidget = QTextEdit()
		self.passwordWidget = QTextEdit()
		self.resultsWidget = QTextEdit()
		self.mailWidget.setStyleSheet("color:white;border:1px solid #1abc9c; border-radius:10px 5px 10px 5px")
		self.passwordWidget.setStyleSheet("color:yellow;border:1px solid #1abc9c; border-radius:10px 5px 10px 5px")
		self.resultsWidget.setStyleSheet("color:yellow;border:1px solid #1abc9c; border-radius:10px 5px 10px 5px")

		self.mailWidget.setReadOnly(True)
		self.passwordWidget.setReadOnly(True)
		self.resultsWidget.setReadOnly(True)


		self.layout.addWidget(self.mailWidget)
		self.layout.addWidget(self.passwordWidget)
		self.layout.addWidget(self.resultsWidget)
		
		self.setCentralWidget(self.centralWidget)
		self.centralWidget.setLayout(self.layout)


		#connect the actions to methods
		self.loadEmails.triggered.connect(self.load_email_file)
		self.loadPasswords.triggered.connect(self.load_password_file)
		self.clearStatus.triggered.connect(self.clearStatusField)
		self.clearEmails.triggered.connect(self.clearEmailField)
		self.clearPasswords.triggered.connect(self.clearPasswordField)
		self.startBrute.triggered.connect(self.start_application)
		self.stopBrute.triggered.connect(self.stop_application)

		#connect the configure chrome action 
		self.addChromePath.triggered.connect(self.add_chrome_path)

		#connect the disclaimer action 
		self.aboutApplication.triggered.connect(self.show_disclaimer)

		#connect the stopBruteforcing application and event
		self.connect(self, SIGNAL("STOPBRUTE"), self.stop_email_loop)


	def load_email_file(self):
		filename = QFileDialog.getOpenFileName(self.centralWidget, 'Open File', 'C:\\')
		try:
			self.emailList += open(filename, 'r').readlines()
			# print(self.emailList)
			self.mailCount = len(self.emailList)
			self.statusBar.showMessage("Email: " + str(self.mailCount) + " Password : " + str(self.passCount))
			# self.mailWidget.setText(self.emailList)
			for lines in open(filename, 'r').xreadlines():
				self.mailWidget.append(lines)
		except Exception as e:
			self.alertBox = QMessageBox(self)
			self.alertBox.setIcon(QMessageBox.Warning)
			self.alertBox.setWindowTitle("Invalid Email File selected")
			# self.alertBox.setText("File Error: " + str(e))
			self.alertBox.setText("File Error: A valid email file must be selected ")
			self.alertBox.show()

	def load_password_file(self):
		password_file = QFileDialog.getOpenFileName(self.centralWidget, 'Open File', 'C:\\')
		try:
			self.passList += open(password_file, 'r').readlines()
			self.passCount = len(self.passList)
			self.statusBar.showMessage("Email: " + str(self.mailCount) + " Password : " + str(self.passCount))
			for lines in open(password_file, 'r').xreadlines():
				self.passwordWidget.append(lines)
		except Exception as e:
			self.alertBox = QMessageBox(self)
			self.alertBox.setIcon(QMessageBox.Warning)
			self.alertBox.setWindowTitle("Invalid Password File selected")
			# self.alertBox.setText("File Error !" + str(e))
			self.alertBox.setText("File Error: A valid email file must be selected ")
			self.alertBox.show()

	def clear_output_status(self):
		self.resultWidget.setText('')

	def clearEmailField(self):
		self.mailWidget.setText('')
		self.mailCount = 0
		self.emailList = []
		self.statusBar.showMessage("Email: " + str(self.mailCount) + " Password : " + str(self.passCount))

	def clearPasswordField(self):
		self.passwordWidget.setText('')
		self.passCount = 0
		self.passList = []
		self.statusBar.showMessage("Email: " + str(self.mailCount) + " Password : " + str(self.passCount))

	def clearStatusField(self):
		self.resultsWidget.setText('')

	def show_disclaimer(self):
		self.alertbox = QMessageBox.about(self,"About Application", 
			"This Application has been developed for Educational use only "
			"You are free to use at your own risk, The developer will NOT in any way "
			"be responsible for the way you use the application as an end user"
			"You can contact the developer at <a href='mailto:johndoeh4ck[at]gmail.com'>johndoeh4ck[at]gmail.com</a> "
			"This application is licenced under the GNU/GPL License.")

	def add_chrome_path(self):
		# print('adding the chrome path')
		self.chromepath = "path_to_chrome"

	def stop_email_loop(self):
		''' changes the value of the continueBrute variable 
			so as to stop the bruteforcing loop 
			sends a stop signal and tries to break out of the loop '''
		self.continueBrute = False

	def stop_application(self):
		''' Happens when the stopBrute button is clicked on the main window
		  @usedby => Stop Bruteforcing button 
		  @target => stop_email_loop
		  @essence => Stops the bruteforcing operation '''

		self.continueBrute = False
		if self.startBrute.isEnabled() == False:
			self.stopBrute.setEnabled(False)
			self.startBrute.setEnabled(True)
			self.clearStatus.setEnabled(True)
			self.clearEmails.setEnabled(True)
			self.clearPasswords.setEnabled(True)
			#do some shittty operation here
			self.emit(SIGNAL("STOPBRUTE"))
			QMessageBox.information(self, "Alert", "You just stopped the bruteforcing operation")
		else:
			# print("No action to perform")
			QMessageBox.information(self, "Invalid Operation", "Please you have to start the bruteforce first!")
		
	def update_statusBar(self, error, username, login_status):
		print("Update: " + str(username) + ": "+str(error) + ">>" + str(login_status))
		
	def start_application(self):
		print("starting the application ")
		if len(self.emailList) != 0 and len(self.passList) != 0:
			self.startBrute.setEnabled(False)
			self.clearStatus.setEnabled(False)
			self.clearEmails.setEnabled(False)
			self.clearPasswords.setEnabled(False)
			self.stopBrute.setEnabled(True)
			#then do the looping construct
			for email in self.emailList:
				for password in self.passList:
				# set the email and current password in the statusbar 
					email = email.strip()
					password = password.strip()
					self.statusBar.showMessage("Trying: "+ email + " : "+ password)
					#use the browserthreaad class here 
					self.browserThread = browserClass.browserClass()
					self.browserThread.set_details(email, password)
					time.sleep(10)
					self.connect(self.browserThread, SIGNAL("DONEWITHMAIL"),  self.browser_done)
					# self.connect(self.browserThread, SIGNAL("finished()"), self.browser_done)
					self.browserThread.start() #start the  browser in a thread
			#finished performing the operation
			self.stopBrute.setEnabled(False)
			self.startBrute.setEnabled(True)
			self.clearStatus.setEnabled(True)
			self.clearEmails.setEnabled(True)
			self.clearPasswords.setEnabled(True)
			QMessageBox.information(self, "Done", "Operation has finished Successfully, wait for the results to be updated !")

		else:
			QMessageBox.information(self, "Error !", "Sorry Email and Passwords must be loaded")
	def browser_done(self,error, username, login_status):
		''' Updates the status pane when all request have been fetched and puts 
			status on the status pane '''
		print("done browserr", error, username, login_status)
		if 'element' in error:
			output = "Website is down: Email :" + str(username) + " Status: " + str(login_status)
		else:
			output = str(username) + " Status: " + str(login_status)
		self.resultsWidget.append(output)
				





app   = QApplication(sys.argv)
window = startWindow()
window.show()
app.exec_()