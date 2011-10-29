#!/usr/bin/env python
import xlrd
from benji.models import *
def scrapeUserData():
	xlbook = xlrd.open_workbook('/home/sunfinity/Downloads/finalProjectList.xls', 'rw')
	xlsheet = xlbook.sheet_by_name('CSE')
	for i in range(1, xlsheet.nrows):
		user = User(usn = xlsheet.cell_value(i, 1), name = xlsheet.cell_value(i, 2), email = xlsheet.cell_value(i, 21))
		user.save()

