from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import StreamingResponse
import pandas as pd
import gspread
from pydantic import BaseModel




app=FastAPI()


### ENDPOINT TO CONFIRM THAT USER EXISTS ####
@app.post("/authentication")
def getusername(payload: dict = Body(...)):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    username= payload['user']
    password= payload['password']
    gc = gspread.service_account('credentials.json')
    spreadsheet=gc.open_by_key(SHEET_ID)
    worksheet=spreadsheet.worksheet(SHEET_NAME)
    rows=worksheet.get_all_records()    
    df=pd.DataFrame(rows)
    cell = worksheet.find(username)
    try:
        if username in set(df['Username']) and password in worksheet.cell(cell.row,cell.col +1).value:
            raise HTTPException(status_code=200,detail="User Authentication Successful")
        elif username in set(df['Username']) and password not in worksheet.cell(cell.row,cell.col +1).value:
            raise HTTPException(status_code=401,detail="You Have Entered The Wrong Password")
    except:
        raise HTTPException(status_code=400,detail="Incorrect Credentials were entered")
    
@app.head("/authentication")
def getusername():
    raise HTTPException(status_code=403,detail='HEAD IS NOT ALLOWED FOR "authentication" ENDPOINT')
@app.options("/authentication")
def getusername():
    raise HTTPException(status_code=403,detail='OPTIONS IS NOT ALLOWED FOR "authentication" ENDPOINT')
@app.patch("/authentication")
def getusername():
    raise HTTPException(status_code=403,detail='PATCH IS NOT ALLOWED FOR "authentication" ENDPOINT')
@app.put("/authentication")
def getusername():
    raise HTTPException(status_code=403,detail='PUT IS NOT ALLOWED FOR "authentication" ENDPOINT')
@app.delete("/authentication")
def getusername():
    raise HTTPException(status_code=403,detail='DELETE IS NOT ALLOWED FOR "authentication" ENDPOINT')
@app.get("/authentication")
def getusername():
    raise HTTPException(status_code=200,detail='SUCCESS')    


#### ENDPOINT TO CREATE A USER ####
@app.post("/createuser")
def postusername(payload: dict = Body(...)):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    if ('name') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A NAME')
    if ('user') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A USER')
    if ('password') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A PASSWORD')    
    else:
        username= payload['user']
        password= payload['password']   
        name= payload['name']
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
    
@app.head("/createuser")
def updateusername():
    raise HTTPException(status_code=403,detail='HEAD IS NOT ALLOWED FOR "createuser" ENDPOINT')
@app.options("/createuser")
def updateusername():
    raise HTTPException(status_code=403,detail='OPTIONS IS NOT ALLOWED FOR "createuser" ENDPOINT')
@app.patch("/createuser")
def updateusername():
    raise HTTPException(status_code=403,detail='PATCH IS NOT ALLOWED FOR "createuser" ENDPOINT')
@app.put("/createuser")
def updateusername():
    raise HTTPException(status_code=403,detail='PUT IS NOT ALLOWED FOR "createuser" ENDPOINT')
@app.delete("/createuser")
def updateusername():
    raise HTTPException(status_code=403,detail='DELETE IS NOT ALLOWED FOR "createuser" ENDPOINT')
@app.get("/createuser")
def updateusername():
    raise HTTPException(status_code=200,detail='SUCCESS')    

    
### ENDPOINT TO UPDATE USERNAME ###
@app.patch("/updateusername")
def updateusername(payload: dict = Body(...)):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    if ('user') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A USER')
    if ('password') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A PASSWORD') 
    if ('newuser') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A NEW USER')    
    else:
        username= payload['user']
        password= payload['password'] 
        newuser= payload['newuser']    
        gc = gspread.service_account('credentials.json')
        spreadsheet=gc.open_by_key(SHEET_ID)
        worksheet=spreadsheet.worksheet(SHEET_NAME)
        rows=worksheet.get_all_records()    
        df=pd.DataFrame(rows)
        cell = worksheet.find(username)
        if username in set(df['Username']) and password in worksheet.cell(cell.row,cell.col +1).value:
            cell = worksheet.find(username)
            worksheet.update_cell(cell.row,cell.col,value=newuser)
            return("You Successfully Updated Your Username To: "+newuser)
        elif username in set(df['Username']) and password not in worksheet.cell(cell.row,cell.col +1).value:
            raise HTTPException(status_code=401,detail="YOU HAVE ENTERED THE WRONG PASSWORD")
        else:
            raise HTTPException(status_code=400,detail="THE USERNAME DOES NOT EXIST")


@app.head("/updateusername")
def updateusername():
    raise HTTPException(status_code=403,detail='HEAD IS NOT ALLOWED FOR "updateusername" ENDPOINT')
@app.options("/updateusername")
def updateusername():
    raise HTTPException(status_code=403,detail='OPTIONS IS NOT ALLOWED FOR "updateusername" ENDPOINT')
@app.post("/updateusername")
def updateusername():
    raise HTTPException(status_code=403,detail='POST IS NOT ALLOWED FOR "updateusername" ENDPOINT')
@app.put("/updateusername")
def updateusername():
    raise HTTPException(status_code=403,detail='PUT IS NOT ALLOWED FOR "updateusername" ENDPOINT')
@app.delete("/updateusername")
def updateusername():
    raise HTTPException(status_code=403,detail='DELETE IS NOT ALLOWED FOR "updateusername" ENDPOINT')
@app.get("/updateusername")
def updateusername():
    raise HTTPException(status_code=200,detail='SUCCESS')




### ENDPOINT TO UPDATE PASSWORD ####
@app.patch("/updatepassword")
def updatepassword(payload: dict = Body(...)):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    if ('user') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A USER')
    if ('password') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A PASSWORD') 
    if ('newpassword') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A NEW PASSWORD')    
    else:   
        username= payload['user']
        password= payload['password'] 
        newpassword= payload['newpassword'] 
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

@app.head("/updatepassword")
def updatepassword():
    raise HTTPException(status_code=403,detail='HEAD IS NOT ALLOWED FOR "updatepassword" ENDPOINT')
@app.options("/updatepassword")
def updatepassword():
    raise HTTPException(status_code=403,detail='OPTIONS IS NOT ALLOWED FOR "updatepassword" ENDPOINT')
@app.post("/updatepassword")
def updatepassword():
    raise HTTPException(status_code=403,detail='POST IS NOT ALLOWED FOR "updatepassword" ENDPOINT')
@app.put("/updatepassword")
def updatepassword():
    raise HTTPException(status_code=403,detail='PUT IS NOT ALLOWED FOR "updatepassword" ENDPOINT')
@app.delete("/updatepassword")
def updatepassword():
    raise HTTPException(status_code=403,detail='DELETE IS NOT ALLOWED FOR "updatepassword" ENDPOINT')
@app.get("/updatepassword")
def updatepassword():
    raise HTTPException(status_code=200,detail='SUCCESS')






### ENDPOINT TO DELETE USER ACCOUNT ###
@app.delete("/deleteuser")
def deleteuser(payload: dict = Body(...)):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Username'
    if ('user') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A USER')
    if ('password') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A PASSWORD')    
    else:
        username= payload['user']
        password= payload['password']         
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
        
@app.head("/deleteuser")
def deleteuser():
    raise HTTPException(status_code=403,detail='HEAD IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.options("/deleteuser")
def deleteuser():
    raise HTTPException(status_code=403,detail='OPTIONS IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.post("/deleteuser")
def deleteuser():
    raise HTTPException(status_code=403,detail='POST IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.put("/deleteuser")
def deleteuser():
    raise HTTPException(status_code=403,detail='PUT IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.patch("/deleteuser")
def deleteuser():
    raise HTTPException(status_code=403,detail='PATCH IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.get("/deleteuser")
def deleteuser():
    raise HTTPException(status_code=200,detail='SUCCESS')





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
