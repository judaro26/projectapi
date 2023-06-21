from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import StreamingResponse
import pandas as pd
import gspread
from pydantic import BaseModel




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
        
@app.head("account-management")
def deleteuser():
    raise HTTPException(status_code=403,detail='HEAD IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.options("account-management")
def deleteuser():
    raise HTTPException(status_code=403,detail='OPTIONS IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.post("account-management")
def deleteuser():
    raise HTTPException(status_code=403,detail='POST IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.put("account-management")
def deleteuser():
    raise HTTPException(status_code=403,detail='PUT IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.patch("account-management")
def deleteuser():
    raise HTTPException(status_code=403,detail='PATCH IS NOT ALLOWED FOR "deleteuser" ENDPOINT')
@app.get("account-management")
def deleteuser():
    raise HTTPException(status_code=200,detail='SUCCESS')
