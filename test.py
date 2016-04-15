# http://usingpython.com/guis-and-functions/
import tkinter
window = tkinter.Tk()
window.title('PhoneBook')
lbl = tkinter.Label(window, text = 'Click a contact to display details')
information = {
		'Marvin': ['6502857174', 'bdeng2@stanford.edu'],
		'Yanyang': ['6502857358', 'yanyangk@stanford.edu'],
		'Oliver': ['0773299509', 'thed00d@aol.com']
		}
lbl.pack()
name = ''
phone = ''
email = ''
def changeInformation(key):
	def rtn():
		lbl0.configure(text = 'Details for ' + key)
		lbl1.configure(text = information[key][0])
		lbl2.configure(text = information[key][1])
	return rtn
for key in information:
	btn = tkinter.Button(text = key, command = changeInformation(key))
	btn.pack()
lbl0 = tkinter.Label(window, text = 'Details for ' + key)
lbl0.pack()
tkinter.Label(window, text = 'Mobile:').pack()
lbl1 = tkinter.Label(window, text = phone)
lbl1.pack()
tkinter.Label(window, text = 'Email:').pack()
lbl2 = tkinter.Label(window, text = email)
lbl2.pack()
window.mainloop()
