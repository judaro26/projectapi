from fastapi import FastAPI, HTTPException, Body,Request
from fastapi.responses import StreamingResponse
import pandas as pd
import gspread
from pydantic import BaseModel
import re




app=FastAPI()


### ENDPOINT TO DELETE USER ACCOUNT ###
@app.delete("/accountmanagement")
def deleteuser(payload: dict = Body(...)):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    TODELETESHEET_NAME="Username"
    SHEET_NAME='Management User DB'
    if ('user') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A USER')
    if ('password') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A PASSWORD')    
    if ('delete') not in payload:
        raise HTTPException(status_code=400,detail="YOU ARE MISSING THE DELETE OBJECT")
    else:
        username= payload['user']
        password= payload['password'] 
        delete= payload['delete']        
        gc = gspread.service_account('credentials.json')
        spreadsheet=gc.open_by_key(SHEET_ID)
        worksheet=spreadsheet.worksheet(SHEET_NAME)
        todeleteworksheet=spreadsheet.worksheet(TODELETESHEET_NAME)
        usercell=worksheet.find(username)
        usernamevalue= worksheet.cell(usercell.row,usercell.col).value
        passwordvalue=worksheet.cell(usercell.row,usercell.col+1).value
        yesvalue=worksheet.cell(usercell.row,usercell.col+2).value
        if username in usernamevalue and password in passwordvalue and delete in yesvalue:
            todeleteworksheet.batch_clear(["A1:D1000"])
            return("YOU CLEARED THE FIRST 1000 USERS FROM THE DB")
        elif username in usernamevalue and password not in passwordvalue:
            raise HTTPException(status_code=401,detail="YOU HAVE ENTERED THE WRONG PASSWORD")
        else:
            raise HTTPException(status_code=400,detail="THE USERNAME DOES NOT EXIST")
        
@app.head("/accountmanagement")
def deleteuser():
    raise HTTPException(status_code=403,detail='HEAD IS NOT ALLOWED FOR "accountmanagement" ENDPOINT')
@app.options("/accountmanagement")
def deleteuser():
    raise HTTPException(status_code=403,detail='OPTIONS IS NOT ALLOWED FOR "accountmanagement" ENDPOINT')
@app.post("/accountmanagement")
def deleteuser():
    raise HTTPException(status_code=403,detail='POST IS NOT ALLOWED FOR "accountmanagement" ENDPOINT')
@app.put("/accountmanagement")
def deleteuser():
    raise HTTPException(status_code=403,detail='PUT IS NOT ALLOWED FOR "accountmanagement" ENDPOINT')
@app.get("/accountmanagement")
def deleteuser():
    raise HTTPException(status_code=200,detail='SUCCESS')




### ENDPOINT TO DELETE USER ACCOUNT ###
@app.patch("/accountmanagement")
def patchuser(targerUsername:str| None=None,targetpassword:str| None = None,targetname:str| None = None,payload: dict = Body(...)):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    TODELETESHEET_NAME="Username"
    SHEET_NAME='Management User DB'
    if ('user') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A USER')
    if ('password') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A PASSWORD')    
    if ('delete') not in payload:
        raise HTTPException(status_code=400,detail="YOU ARE MISSING THE DELETE OBJECT")
    else:
        username= payload['user']
        password= payload['password'] 
        delete= payload['delete'] 
        gc = gspread.service_account('credentials.json')
        spreadsheet=gc.open_by_key(SHEET_ID)
        worksheet=spreadsheet.worksheet(SHEET_NAME)
        tobeupdated=spreadsheet.worksheet(TODELETESHEET_NAME)
        usercell=worksheet.find(username)
        usernamevalue= worksheet.cell(usercell.row,usercell.col).value
        passwordvalue=worksheet.cell(usercell.row,usercell.col+1).value
        yesvalue=worksheet.cell(usercell.row,usercell.col+2).value
        if username in usernamevalue and password in passwordvalue and delete in yesvalue:
                newuserlist=[targerUsername,targetpassword,targetname]
                if newuserlist[0]!=None:
                    currentuser=str(newuserlist[0])
                    criteria_re = re.compile(currentuser)
                    coordinates = tobeupdated.find(criteria_re)
                    if 'newusername' in payload:
                        tobeupdated.update_cell(coordinates.row,coordinates.col,value=payload['newuser'])
                        raise HTTPException(status_code=200,detail="USER UPDATED TO "+ payload['newuser'])
                    else:
                        raise HTTPException(status_code=207,detail="YOU FORGOT TO INCLUDE A NEW USER IN THE BODY OF YOUR CALL")
                elif newuserlist[0]==None:
                    raise HTTPException(status_code=207,detail="YOU DIDN'T ENTER A VALID 'targetUsername:True' PARAMETER")
                if newuserlist[1]!=None:
                    currentuser=str(newuserlist[0])
                    criteria_re = re.compile(currentuser)
                    coordinates = tobeupdated.find(criteria_re)
                    if 'newpassword' in payload:
                        tobeupdated.update_cell(coordinates.row,coordinates.col,value=payload['newuser'])
                        raise HTTPException(status_code=200,detail="USER UPDATED TO "+ payload['newuser'])
                    else:
                        raise HTTPException(status_code=207,detail="YOU FORGOT TO INCLUDE A NEW PASSWORD IN THE BODY OF YOUR CALL")
                else:
                    raise HTTPException(status_code=207,detail="YOU DIDN'T ENTER A VALID 'targetpassword:True' PARAMETER")               
                
                
        elif username in usernamevalue and password not in passwordvalue:
            raise HTTPException(status_code=401,detail="YOU HAVE ENTERED THE WRONG PASSWORD")
        else:
            raise HTTPException(status_code=400,detail="THE USERNAME DOES NOT EXIST")
        
