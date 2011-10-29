#!/usr/bin/python
#Filename: populate.py

from benjy.models import User, Project
import sqlite3
import re

passwordFile = file('sherlockholmes.txt').read().lower()
words = [word for word in re.split(r'\W+|\d+', passwordFile) if len(word) > 3]
count = 42

def populateUser():
	conn = sqlite3.connect('mail.db')
	cur = conn.cursor()

	cur.execute("select rowid, name, usn, email, project from user")
	students = cur.fetchall()[3:] #empty fields

	for student in students:
		user = User()
		user.name = student[1]
		user.usn = student[2]
		user.email = student[3]
		user.project_id = student[4]
		flag = True
		while flag:
			password = user.password = getPassword()
			try:
				user.save()
				flag = False
			except:	flag = True
		cur.execute("update user set password = ? where rowid = ?", (password, student[0]))# for the mail
	conn.commit()

def getPassword(): 
	global count
	count += 2
	return words[count % len(words)] + ' ' + words[(count+1) % len(words)]
 

def populateProject():
	conn = sqlite3.connect("mail.db")
	cur = conn.cursor()

	cur.execute("select * from projects order by projectId")
	projects = cur.fetchall()

	for project in projects:
		try: user = User.objects.get(name = project[2])
		except: 
			user = User()
			user.name = project[2]
			user.usn = 'T'
			user.isTeacher = True 
			flag = True
			while flag:
				password = user.password = getPassword()
				try: 
					user.save()
					flag = False
				except: 
					flag = True

			cur.execute("insert into user (name, password, usn) values (?, ?, ?)",(user.name, password, user.usn));

		projectObj = Project()
		projectObj.title = project[1]
		projectObj.guide = user
		projectObj.save()
		conn.commit()

