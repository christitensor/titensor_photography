from tkinter import *
import pyqrcode
import os
import pickle
import os.path
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import messagebox
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from tkinter.simpledialog import askstring
import pandas as pd
import sys
import numpy as np

#sets up first main window
window = Tk()
window.title("Titensor Photography Registration")
window.configure(background='yellow')

result = messagebox.askyesno('Resume Session?', 'Would you like to go back to a prior session?')

if result == True:
    messagebox.showinfo(title='Open...', message="Open pickle file you'd like to resume")
    priorsessionpath = askopenfilename()
    name_of_file = askstring('What do you want to title this file?', 'File Name')
    messagebox.showinfo(title='Save...', message="Please navigate to where you want to save today's report")
    save_path = askdirectory()
    #priorsession = pd.read_csv(priorsessionpath)
    with open(priorsessionpath, 'rb') as pkl:
        team = pickle.load(pkl)
    control_number = team['control_number'][-1]
else:
    #Get the file name
    name_of_file = askstring('What do you want to title this file?', 'File Name')
    #create an empty dictionary to later fill out
    team = {'first_name':[], 'last_name':[], 'number':[], 'grade':[], 'sport':[], 'school':[], 'control_number':[] ,
    'team':[], 'parent_first_name':[], 'parent_last_name':[], 'parent_phone_number':[], 'parent_email':[], 'eight_by_ten':[],
    'team_photo':[], 'fifty_package':[], 'banner':[], 'blanket': [], 'frame':[], 'payment_type':[], 'payment_amount':[]}
    #get path to save file to
    messagebox.showinfo(title='Save...', message="Please navigate to where you want to save today's report")
    save_path = askdirectory()
    #choose where to start control number from
    control_number = 0
defaultsales = 0
defaultsalesvar= StringVar(window, value=str(defaultsales))
#get the font path depending on the OS
if sys.platform == 'darwin':
    font_path = '/System/Library/Fonts/Helvetica'
else:
    font_path = '/C:/WINDOWS/FONTS/ARLRDBD'

def generate():
    #function to convert inputs to dictionary and dataframe, also creates QR code and prints out card

    #makes sure first name field is populated before adding to the dataframe
    if len(fname.get()) != 0:
        #password protects submissions
        password = askstring('Thank You!', 'Enter password', show='*')
        #change password below
        if password == 'a':
            global myQr
            global control_number
            #gathers data to create code with
            data=fname.get()+"_"+lname.get()+"_"+grade.get()+"_"+num.get()+"_"+sport.get()+"_"+school.get()
            #creats QR codee
            myQr= pyqrcode.create(data)
            qrImage= myQr.xbm(scale=6)
            global photo
            photo = BitmapImage(data= qrImage)
            myQr.png('qrcode.png')
            control_number += 1
            control_number_text = str(control_number)
            #next part comes from https://stackoverflow.com/questions/43295189/extending-a-image-and-adding-text-on-the-extended-area-using-python-pil
            #create card
            height = 800
            interval = 250
            paperwidth = 2550
            paperheight = 3300
            center = (paperwidth/2)-(paperwidth/6)
            # next part comes from https://stackoverflow.com/questions/43295189/extending-a-image-and-adding-text-on-the-extended-area-using-python-pil
            font = ImageFont.truetype(font=font_path, size=200)
            background = Image.new('RGBA', (paperwidth, paperheight), (255, 255, 255, 255))
            draw = ImageDraw.Draw(background)
            #adds the different text lines to the card
            qr = Image.open('qrcode.png')
            qr = qr.resize((1000, 1000), Image.ANTIALIAS)
            background.paste(qr, ((round(paperwidth / 2)), 20))
            draw.text((center, (height + (interval * 1))), control_number_text, (0, 0, 0), font=ImageFont.truetype(font=font_path, size=300))
            draw.text((center, (height + (interval * 2))), fname.get(), (0, 0, 0), font=font)
            draw.text((center, (height + (interval * 3))), lname.get(), (25, 25, 25), font=font)
            draw.text((center, (height + (interval * 4))), grade.get(), (25, 25, 25), font=font)
            draw.text((center, (height + (interval * 5))), num.get(), (25, 25, 25), font=font)
            draw.text((center, (height + (interval * 6))), sport.get(), (25, 25, 25), font=font)
            draw.text((center, (height + (interval * 7))), school.get(), (25, 25, 25), font=font)
            #save the card as a png
            background.save(save_path+'/'+control_number_text+"_"+fname.get()+"_" +lname.get()+'.png')
            #print the card to default printer
            if sys.platform == 'darwin':
                os.system("lpr "+save_path+'/'+control_number_text+"_"+fname.get()+ '_'+lname.get()+'.png')
            else:
                os.startfile(save_path+'/'+control_number_text+"_"+fname.get()+'_'+ lname.get()+'.png', 'print')
    #add all the inputs to the dictionary
            #team.update( {num.get():{'First Name':fname.get(),'Last Name':lname.get(), 'Number':num.get(), 'Age': age.get(),'Sport': sport.get(), 'School':school.get()}} )
            team['first_name'].append(fname.get())
            team['last_name'].append(lname.get())
            team['number'].append(num.get())
            team['grade'].append(grade.get())
            team['sport'].append(sport.get())
            team['school'].append(school.get())
            team['control_number'].append((control_number))
            team['team'].append(varsity.get())
            team['parent_first_name'].append(parentfname.get())
            team['parent_last_name'].append(parentlname.get())
            team['parent_phone_number'].append((parentnumber.get()))
            team['parent_email'].append(email.get())
            team['eight_by_ten'].append(eightbyten.get())
            team['team_photo'].append(teamphoto.get())
            team['fifty_package'].append(fifty.get())
            team['banner'].append(banner.get())
            team['blanket'].append(blanket.get())
            team['frame'].append(frame.get())
            team['payment_type'].append(payment.get())
            team['payment_amount'].append(paymentamount.get())

            #team = {k: np.nan if not v else v for k, v in team.items()}
            for key, value in team.items():
                if value == '':
                    team[key] = np.nan
            #, 'Last Name': lname.get(), 'Number': num.get(),'Age': age.get(), 'Sport': sport.get(), 'School': school.get()})
            #save to pickle

            completeName = os.path.join(save_path, name_of_file+".pickle")

            file1 = open(completeName, "wb")


            with open(completeName, 'wb') as handle:
                pickle.dump(team, file1)
            file1.close()
            #add to dataframe and save as a csv
            pd.DataFrame(team).to_csv(save_path + '/' + name_of_file + '.csv',index=False)
            #clear out fields
            fields_to_clear = [fnameEntry, lnameEntry, numEntry, parentfnameEntry, parentlnameEntry, parentnumberEntry, emailEntry,
                               eightbytenEntry, teamphotoEntry, fiftyEntry, bannerEntry, blanketEntry, frameEntry]
            for field in fields_to_clear:
                field.delete(0, END)

        else:
            messagebox.showinfo("Incorrect Password", "Please input the correct password")

    else:
        messagebox.showinfo("Error!", "Please Complete the Form")
    try:
        showCode()
    except:
        pass
        

def showCode():
    #function to show the QR code
    global photo
    notificationLabel.config(image= photo)
    #subLabel.config(text= "Showing QR Code for: "+fname.get()+' '+lname.get())

def clear_widget(event):
    # will clear out any entry boxes defined below when the user shifts
    # focus to the widgets defined below
    if eightbytenEntry == window.focus_get():# and username_box.get() == 'Enter Username':
        eightbytenEntry.delete(0, END)
    elif teamphotoEntry == teamphotoEntry.focus_get():# and lnameEntry.get() == '     ':
        teamphotoEntry.delete(0, END)
    elif fiftyEntry == fiftyEntry.focus_get():
        fiftyEntry.delete(0, END)
    elif bannerEntry == bannerEntry.focus_get():
        bannerEntry.delete(0, END)
    elif blanketEntry == blanketEntry.focus_get():
        blanketEntry.delete(0, END)
    elif frameEntry == frameEntry.focus_get():
        frameEntry.delete(0, END)
def repopulate_defaults(event):
    # will repopulate the default text previously inside the entry boxes defined below if
    # the user does not put anything in while focused and changes focus to another widget
    if eightbytenEntry != window.focus_get() and eightbytenEntry.get() == '':
        eightbytenEntry.insert(0, defaultsales)
    elif teamphotoEntry != window.focus_get() and teamphotoEntry.get() == '':
        teamphotoEntry.insert(0, defaultsales)
    elif fiftyEntry != window.focus_get() and fiftyEntry.get() == '':
        fiftyEntry.insert(0, defaultsales)
    elif bannerEntry != window.focus_get() and bannerEntry.get() == '':
        bannerEntry.insert(0, defaultsales)
    elif blanketEntry != window.focus_get() and blanketEntry.get() == '':
        blanketEntry.insert(0, defaultsales)
    elif frameEntry != window.focus_get() and frameEntry.get() == '':
        frameEntry.insert(0, defaultsales)

#set up placement for each line
fnamerow = 0
lnamerow = 1 + fnamerow
numrow = 1 + lnamerow
graderow = 1 + numrow
schoolrow = 1 + graderow
sportrow = 1 + schoolrow
varsityrow = 1 + sportrow
parentfnamerow = 1 + varsityrow
parentlnamerow = 1 + parentfnamerow
parentnumberrow = 1 + parentlnamerow
emailrow = 1 + parentnumberrow

spacerow = 1 + emailrow
eightbytenrow = 1+ spacerow
teamphotorow = 1 + eightbytenrow
fiftyrow = 1 + teamphotorow
bannerrow = 1 + fiftyrow
blanketrow = 1 + bannerrow
framerow = 1 + blanketrow
paymentrow = 1 + framerow
paymentamountrow = 1 + paymentrow
submitrow = 2 + paymentamountrow


#setting up the window some more
#this adds all of the labels on the left side
fnamelab = Label(window, text="First Name",  font=("Helvetica", 12))
fnamelab.grid(row=fnamerow, column= 0, sticky= N+S+E+W)

lnamelab = Label(window, text="Last Name",  font=("Helvetica", 12))
lnamelab.grid(row=lnamerow, column= 0, sticky= N+S+E+W)

numlab = Label(window, text="Jersey Number",  font=("Helvetica", 12))
numlab.grid(row=numrow, column= 0, sticky= N+S+E+W)

gradelab = Label(window, text="Grade",  font=("Helvetica", 12))
gradelab.grid(row=graderow, column= 0, sticky= N+S+E+W)

schoollab = Label(window, text="School",  font=("Helvetica", 12))
schoollab.grid(row=schoolrow, column= 0, sticky= N+S+E+W)

sportlab = Label(window, text="Sport",  font=("Helvetica", 12))
sportlab.grid(row=sportrow, column= 0, sticky= N+S+E+W)

varsitylab = Label(window, text="Team",  font=("Helvetica", 12))
varsitylab.grid(row=varsityrow, column= 0, sticky= N+S+E+W)

parentfnamelab = Label(window, text="Parent First Name",  font=("Helvetica", 12))
parentfnamelab.grid(row=parentfnamerow, column= 0, sticky= N+S+E+W)

parentlnamelab = Label(window, text="Parent Last Name",  font=("Helvetica", 12))
parentlnamelab.grid(row=parentlnamerow, column= 0, sticky= N+S+E+W)

parentnumberlab = Label(window, text="Parent Phone Number",  font=("Helvetica", 12))
parentnumberlab.grid(row=parentnumberrow, column= 0, sticky= N+S+E+W)

emaillab = Label(window, text="Parent Email",  font=("Helvetica", 12))
emaillab.grid(row=emailrow, column= 0, sticky= N+S+E+W)

spacelab = Label(window, text="*PROCEED TO THIS POINT",  font=("Helvetica", 20))
spacelab.grid(row=spacerow, column= 0, sticky= N+S+E+W)

eightbytenlab = Label(window, text="8x10",  font=("Helvetica", 12))
eightbytenlab.grid(row=eightbytenrow, column= 0, sticky= N+S+E+W)

teamphotolab = Label(window, text = 'Team Photo', font = ('Helvitica', 12))
teamphotolab.grid(row=teamphotorow, column= 0, sticky= N+S+E+W)

fiftylab = Label(window, text = '$50 Package', font = ('Helvitica', 12))
fiftylab.grid(row=fiftyrow, column= 0, sticky= N+S+E+W)

bannerlab = Label(window, text = 'Banner $40', font = ('Helvitica', 12))
bannerlab.grid(row=bannerrow, column= 0, sticky= N+S+E+W)

blanketlab = Label(window, text = 'Blanket $70', font = ('Helvitica', 12))
blanketlab.grid(row=blanketrow, column= 0, sticky= N+S+E+W)

framelab = Label(window, text = 'Frame $20', font = ('Helvitica', 12))
framelab.grid(row=framerow, column= 0, sticky= N+S+E+W)

paymentlab = Label(window, text="Payment Type",  font=("Helvetica", 12))
paymentlab.grid(row=paymentrow, column= 0, sticky= N+S+E+W)

paymentamountlab = Label(window, text="Payment Amount",  font=("Helvetica", 12))
paymentamountlab.grid(row=paymentamountrow, column= 0, sticky= N+S+E+W)

##############################################################################

#this adds the entry fields
fname= StringVar()
fnameEntry = Entry(window, textvariable = fname,font=("Helvetica", 12))
fnameEntry.grid(row=fnamerow, column=1, sticky= N+S+E+W)
fnameEntry.bind("<FocusIn>", clear_widget)

lname= StringVar()
lnameEntry = Entry(window, textvariable = lname, font=("Helvetica", 12))
lnameEntry.grid(row=lnamerow, column=1, sticky= N+S+E+W)
lnameEntry.bind("<FocusIn>", clear_widget)

num= StringVar()
numEntry = Entry(window, textvariable = num, font=("Helvetica", 12))
numEntry.grid(row=numrow, column=1, sticky= N+S+E+W)

grade= StringVar()
gradechoices = {9, 10, 11,12, 'Coach'}
grade.set(9) # set the default option
gradedropdown = OptionMenu(window, grade, *gradechoices)
gradedropdown.grid(row=graderow, column=1, sticky= N+S+E+W)

school = StringVar()
schoolchoices = { 'Preston', 'Green Canyon', 'Ridgeline', 'Skyview', 'Logan'}
school.set('Preston') # set the default option
schooldropdown = OptionMenu(window, school, *schoolchoices)
schooldropdown.grid(row = schoolrow, column =1, sticky= N+S+E+W)

sport = StringVar()
sportchoices = { 'Football','Tennis', 'Soccer', 'Volleyball', 'Cross Country','Golf', 'Cheer'}
sport.set('Football') # set the default option
sportdropdown = OptionMenu(window, sport, *sportchoices)
sportdropdown.grid(row = sportrow, column =1, sticky= N+S+E+W)

varsity = StringVar()
varsitychoices = { 'Varsity', 'JV', 'Freshman','N/A'}
varsity.set('N/A') # set the default option
varsitydropdown = OptionMenu(window, varsity, *varsitychoices)
varsitydropdown.grid(row = varsityrow, column =1, sticky= N+S+E+W)

parentfname = StringVar()
parentfnameEntry = Entry(window, textvariable = parentfname, font=("Helvetica", 12))
parentfnameEntry.grid(row=parentfnamerow, column=1, sticky= N+S+E+W)

parentlname = StringVar()
parentlnameEntry = Entry(window, textvariable = parentlname, font=("Helvetica", 12))
parentlnameEntry.grid(row=parentlnamerow, column=1, sticky= N+S+E+W)

parentnumber = StringVar()
parentnumberEntry = Entry(window, textvariable = parentnumber, font=("Helvetica", 12))
parentnumberEntry.grid(row=parentnumberrow, column=1, sticky= N+S+E+W)

email = StringVar()
emailEntry = Entry(window, textvariable = email, font=("Helvetica", 12))
emailEntry.grid(row=emailrow, column=1, sticky= N+S+E+W)

spacelab = Label(window, text="The pretty lady will help you from here",  font=("Helvetica", 20))
spacelab.grid(row=spacerow, column= 1, sticky= N+S+E+W)

eightbyten = StringVar()
eightbytenEntry = Entry(window, textvariable = eightbyten, font=("Helvetica", 12))
eightbytenEntry.insert(END, 0)
eightbytenEntry.grid(row=eightbytenrow, column=1, sticky= N+S+E+W)
eightbytenEntry.bind("<FocusIn>", clear_widget)
eightbytenEntry.bind('<FocusOut>', repopulate_defaults)

teamphoto = StringVar()
teamphotoEntry = Entry(window, textvariable = teamphoto, font=("Helvetica", 12))
teamphotoEntry.insert(END, 0)
teamphotoEntry.grid(row=teamphotorow, column=1, sticky= N+S+E+W)
teamphotoEntry.bind("<FocusIn>", clear_widget)
teamphotoEntry.bind('<FocusOut>', repopulate_defaults)

fifty = StringVar()
fiftyEntry = Entry(window, textvariable = fifty, font=("Helvetica", 12))
fiftyEntry.insert(END, 0)
fiftyEntry.grid(row=fiftyrow, column=1, sticky= N+S+E+W)
fiftyEntry.bind("<FocusIn>", clear_widget)
fiftyEntry.bind('<FocusOut>', repopulate_defaults)

banner = StringVar()
bannerEntry = Entry(window, textvariable = banner, font=("Helvetica", 12))
bannerEntry.insert(END, 0)
bannerEntry.grid(row=bannerrow, column=1, sticky= N+S+E+W)
bannerEntry.bind("<FocusIn>", clear_widget)
bannerEntry.bind('<FocusOut>', repopulate_defaults)

blanket = StringVar()
blanketEntry = Entry(window, textvariable = blanket, font=("Helvetica", 12))
blanketEntry.insert(END, 0)
blanketEntry.grid(row=blanketrow, column=1, sticky= N+S+E+W)
blanketEntry.bind("<FocusIn>", clear_widget)
blanketEntry.bind('<FocusOut>', repopulate_defaults)

frame = StringVar()
frameEntry = Entry(window, textvariable = frame, font=("Helvetica", 12))
frameEntry.insert(END, 0)
frameEntry.grid(row=framerow, column=1, sticky= N+S+E+W)
frameEntry.bind("<FocusIn>", clear_widget)
frameEntry.bind('<FocusOut>', repopulate_defaults)

payment = StringVar()
#here are choices for the field
paymentchoices = { 'Cash', 'Card', 'Check','Did not pay'}
payment.set('Did not pay') # set the default option
paymentdropdown = OptionMenu(window, payment, *paymentchoices)
paymentdropdown.grid(row = paymentrow, column =1, sticky= N+S+E+W)

paymentamount = StringVar()
paymentamountEntry = Entry(window, textvariable = paymentamount, font=("Helvetica", 12))
paymentamountEntry.insert(END, 0)
paymentamountEntry.grid(row=paymentamountrow, column=1, sticky= N+S+E+W)
paymentamountEntry.bind("<FocusIn>", clear_widget)
paymentamountEntry.bind('<FocusOut>', repopulate_defaults)

createButton = Button(window, text= "Submit", font=("Helvetica", 12), width= 15,command= generate)
createButton.grid(row=submitrow, column=0, sticky= N+S+E+W)

#notificationLabel= Label(window)
#notificationLabel.grid(row= submitrow, column=1, sticky= N+S+E+W)

#subLabel= Label(window, text="")
#subLabel.grid(row= 7, column=1, sticky= N+S+E+W)

#Making responsive layout:
totalRows= 3
totalCols = 3

for row in range(totalRows+1):
    window.grid_rowconfigure(row, weight=1)

for col in range(totalCols+1):
    window.grid_columnconfigure(col, weight=1)

#looping the GUI
window.mainloop()
