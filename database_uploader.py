
import gspread_dataframe as gd
import gspread as gs
import pandas as pd
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
gc = gs.service_account(filename="Sale Database.json")


messagebox.showinfo(title='Open...', message="Open file to upload")
dfpath = askopenfilename()
try:
    df = pd.read_csv(dfpath)
except:
    df = pd.read_excel(dfpath)
    
def export_to_sheets(worksheet_name,df,mode='r'):
    ws = gc.open("Database").worksheet("Data")
    if(mode=='w'):
        ws.clear()
        gd.set_with_dataframe(worksheet=ws,dataframe=df,include_index=False,include_column_header=True,resize=True)
        return True
    elif(mode=='a'):
        ws.add_rows(df.shape[0])
        gd.set_with_dataframe(worksheet=ws,dataframe=df,include_index=False,include_column_header=False,row=ws.row_count+1,resize=False)
        return True
    else:
        return gd.get_as_dataframe(worksheet=ws)
colsneeded = ['control_number', 'first name', 'last name', 'number', 'grade', 'sport', 'school', 'team', 'parent_first_name', 'parent_last_name', 'parent_phone_number', 'parent_email', 'eight_by_ten', 'team_photo', 'fifty_package', 'banner', 'blanket', 'frame', 'payment_type', 'payment_amount', 'notes', 'date', 'full name', 'resize-first name', 'resize-last name', 'resize-full name', 'rename', 'left_number', 'right_number']
currentcols = list(df)
missingcols =(list(list(set(colsneeded)-set(currentcols)) + list(set(currentcols)-set(colsneeded))))
df=pd.concat([df,pd.DataFrame(columns=missingcols)], sort = True)
df = df[colsneeded]

export_to_sheets("Database",df,'a')
messagebox.showinfo(title='Success!', message="Your file has been uploaded")
