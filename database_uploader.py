
import gspread_dataframe as gd
import gspread as gs
import pandas as pd
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
gc = gs.service_account(filename="Sale Database.json")


messagebox.showinfo(title='Open...', message="Open the file to upload")
dfpath = askopenfilename()
df = pd.read_csv(dfpath)
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

export_to_sheets("Database",df,'a')
messagebox.showinfo(title='Success!', message="Your file has been uploaded")