from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import gspread



app=FastAPI()


### ENDPOINT TO CONFIRM THAT USER EXISTS ####
@app.get("/authentication")
def getusername(username:str,password:str,name:str):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    gc = gspread.service_account('credentials.json')
    spreadsheet=gc.open_by_key(SHEET_ID)
    worksheet=spreadsheet.worksheet(SHEET_NAME)
    rows=worksheet.get_all_records()    
    df=pd.DataFrame(rows)
    cell = worksheet.find(username)
    if username in set(df['Username']) and password in worksheet.cell(cell.row,cell.col +1).value:
        return("User Authentication Successful")
    elif username in set(df['Username']) and password not in worksheet.cell(cell.row,cell.col +1).value:
        raise HTTPException(status_code=401,detail="You Have Entered The Wrong Password")
    else:
        raise HTTPException(status_code=400,detail="Incorrect Credentials were entered")

#### ENDPOINT TO CREATE A USER ####
@app.post("/createuser")
def postusername(username:str,password:str,name:str):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    gc = gspread.service_account('credentials.json')
    spreadsheet=gc.open_by_key(SHEET_ID)
    worksheet=spreadsheet.worksheet(SHEET_NAME)
    rows=worksheet.get_all_records()    
    df=pd.DataFrame(rows)
    if username in set(df['Username']):
        raise HTTPException(status_code=400,detail="YOU ALREADY HAVE A USER CREATED")
    else:
        body= [name,username,password]
        worksheet.append_row(body)
        return("SUCCESSFULLY CREATED USERNAME")
    
### ENDPOINT TO UPDATE USERNAME ###
@app.patch("/updateusername")
def updateusername(currentusername:str,password:str,newusername:str):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    gc = gspread.service_account('credentials.json')
    spreadsheet=gc.open_by_key(SHEET_ID)
    worksheet=spreadsheet.worksheet(SHEET_NAME)
    rows=worksheet.get_all_records()    
    df=pd.DataFrame(rows)
    cell = worksheet.find(currentusername)
    if currentusername in set(df['Username']) and password in worksheet.cell(cell.row,cell.col +1).value:
        cell = worksheet.find(currentusername)
        worksheet.update_cell(cell.row,cell.col,value=newusername)
        return("You Successfully Updated Your Username To: "+newusername)
    elif currentusername in set(df['Username']) and password not in worksheet.cell(cell.row,cell.col +1).value:
        raise HTTPException(status_code=401,detail="You Have Entered The Wrong Password")
    else:
        raise HTTPException(status_code=400,detail="THE USERNAME DOES NOT EXIST")


### ENDPOINT TO UPDATE PASSWORD ####
@app.patch("/updatepassword")
def deleteuser(username:str,password:str,newpassword:str):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    gc = gspread.service_account('credentials.json')
    spreadsheet=gc.open_by_key(SHEET_ID)
    worksheet=spreadsheet.worksheet(SHEET_NAME)
    rows=worksheet.get_all_records()    
    df=pd.DataFrame(rows)
    cell = worksheet.find(username)
    if username in set(df['Username']) and password in worksheet.cell(cell.row,cell.col +1).value:
        cell = worksheet.find(password)
        worksheet.update_cell(cell.row,cell.col,value=newpassword)
        return("You Successfully Updated Your Password")
    elif username in set(df['Username']) and password not in worksheet.cell(cell.row,cell.col +1).value:
        raise HTTPException(status_code=401,detail="You Have Entered The Wrong Password")
    else:
        raise HTTPException(status_code=400,detail="THE USERNAME DOES NOT EXIST")

### ENDPOINT TO DELETE USER ACCOUNT ###
@app.delete("/deleteuser")
def postusername(username:str,password:str):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    gc = gspread.service_account('credentials.json')
    spreadsheet=gc.open_by_key(SHEET_ID)
    worksheet=spreadsheet.worksheet(SHEET_NAME)
    rows=worksheet.get_all_records()    
    df=pd.DataFrame(rows)
    cell = worksheet.find(username)
    if username in set(df['Username']) and password in worksheet.cell(cell.row,cell.col +1).value:
        cell = worksheet.find(username)
        worksheet.delete_row(cell.row)
        return("You Successfully Deleted Your Account")
    elif username in set(df['Username']) and password not in worksheet.cell(cell.row,cell.col +1).value:
        raise HTTPException(status_code=401,detail="You Have Entered The Wrong Password")
    else:
        raise HTTPException(status_code=400,detail="THE USERNAME DOES NOT EXIST")




@app.get("/get-iris")
def get_iris():

    import pandas as pd
    url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    iris = pd.read_csv(url)
    return iris


@app.get("/plot-iris")
def plot_iris():

    import pandas as pd
    import matplotlib.pyplot as plt
    url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    iris = pd.read_csv(url)
    plt.scatter(iris['sepal_length'], iris['sepal_width'])
    plt.savefig('iris.png')
    file = open('iris.png', mode="rb")
    return StreamingResponse(file, media_type="image/png")
