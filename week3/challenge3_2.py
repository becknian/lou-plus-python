from openpyxl import load_workbook
from openpyxl import load_workbook
import datetime

def combine():
	courses = load_workbook('courses.xlsx')
	students = courses.get_sheet_by_name('students')
	time = courses.get_sheet_by_name('time')
	courses.create_sheet('combine')
	combine = courses.get_sheet_by_name('combine')
	students.auto_filter.ref = 'A2:C485'
	students.auto_filter.add_sort_condition('A2:A485')
	for row in students.iter_rows():
		combine.append(row)
	courses.save('test.xlsx')

	#print(list(students.iter_rows()))


#def split():


if __name__ == '__main__':
	combine()
	#split()