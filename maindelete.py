from fastapi import FastAPI, HTTPException, Body,Request
from fastapi.responses import StreamingResponse
import pandas as pd
import gspread




app=FastAPI()


### FUNCTION TO ALLOW USERS TO LOGINTO ADMIN ###
@app.post("/access")
def postaccess(payload:dict=Body(...)):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    SHEET_NAME='Management User DB'
    if ('user') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED AN ADMIN USER')
    if ('password') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED AN ADMIN PASSWORD') 
    gc = gspread.service_account('credentials.json')
    spreadsheet=gc.open_by_key(SHEET_ID)
    worksheet=spreadsheet.worksheet(SHEET_NAME)
    ### CREATING VARIABLES FOR TARGET USER VALUES FOUND IN THE SPREADSHEETS ###   
    username= payload['user']  
    password=payload['password']                   
    usercell=worksheet.find(username)
    try:
        if len(worksheet.cell(usercell.row,usercell.col).value)==None:
            raise (HTTPException(status_code=401,detail="THERE IS AN ISSUE WITH THE USERNAME"))
        if payload['user'] in worksheet.cell(usercell.row,usercell.col).value and password in worksheet.cell(usercell.row,usercell.col+1).value:
            raise HTTPException(status_code=200,detail='SUCCESSFUL ENTRY')
        else:
            raise HTTPException(status_code=401,detail='YOURE CREDENTIALS ARE INCORRECT')
    except:
        pass
@app.head("/access")
def deleteuser():
    raise HTTPException(status_code=403,detail='HEAD IS NOT ALLOWED FOR "access" ENDPOINT')
@app.options("/access")
def deleteuser():
    raise HTTPException(status_code=403,detail='OPTIONS IS NOT ALLOWED FOR "access" ENDPOINT')
@app.put("/access")
def deleteuser():
    raise HTTPException(status_code=403,detail='PUT IS NOT ALLOWED FOR "access" ENDPOINT')
@app.get("/access")
def deleteuser():
    raise HTTPException(status_code=200,detail='SUCCESS')


### ENDPOINT TO DELETE USER ACCOUNTs ###
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
        if username in usernamevalue:
            try:
                if len(payload['targetUser'])>0:
                    try:
                        if username in usernamevalue and password in passwordvalue:
                            todeleteworksheet.delete_row(todeleteworksheet.find(payload['targetUser']).row)
                            return("YOU DELETED " + payload['targetUser'])
                        elif username in usernamevalue and password in passwordvalue and todeleteworksheet.find(payload['targetUser'])==None:
                            return("THE USER REQUESTED CAN'T BE FOUND")
                    except:
                        return("THE USER REQUESTED CAN'T BE FOUND")
            except:
                pass
            try:
                if ('targetUser') not in payload and username in usernamevalue and password in passwordvalue and delete in yesvalue:
                    todeleteworksheet.batch_clear(["A2:D1000"])
                    return("YOU CLEARED THE FIRST 1000 USERS FROM THE DB")
                elif username in usernamevalue and password not in passwordvalue:
                        return("YOU HAVE ENTERED THE WRONG PASSWORD")
            except:
                print('line 59' + str(len(payload['targetUser'])))
                pass
        else: 
            raise HTTPException(status_code=401,detail="THE ADMIN USERNAME DOES NOT EXIST")
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


### FUNCTION TO UPDATE USER ACCOUNTS ###       
@app.patch("/accountmanagement")
def patchuser(targetpassword:str,targetName:str, newUser:str, payload: dict = Body(...)):
    SHEET_ID='1XyE3KPBlM4AIqFHEUYkmyLxKvun6RnUFg92BeQMz4M0'
    TOUPDATESHEET_NAME="Username"
    SHEET_NAME='Management User DB'
    ### CREATE PARAM INDEX ####
    targetdata=[targetpassword,targetName,newUser]
    ### CREATE CONDITIONS FOR ADMIN USER VALIDATION ###
    if ('user') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED AN ADMIN USER')
    if ('password') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED AN ADMIN PASSWORD') 
    if ('targetUser') not in payload:
        raise HTTPException(status_code=400,detail='YOU HAVE NOT ENTERED A TARGET USER')  
    if ('canupdate') not in payload:
        raise HTTPException(status_code=400,detail="YOU HAVE NOT ENTERED A 'canupdate' OBJECT IN YOUR PAYLOAD")  
    ### CREATE CONDITIONS FOR ADMIN TO CONFIRM IF PAYLOAD CONTAINS THE SPECIFIC VALUES IN THE PAYLOAD AND PARAMS ###
    try:
        if len(targetdata[1])>0 and payload['targetUser']!=None and payload['targetName']!=None:
                if payload['targetName']==None and targetdata[1]!=None:
                    return("YOU ARE MISSING THE 'targetName' BODY OBJECT")
                elif payload['targetName']!=None and targetdata[1]!=None:
                    bodyName=payload['targetName']
    except:
        print('line 170')
        pass
    try:     
        if len(targetdata[0])>0 and payload['targetUser']!=None and payload['targetPassword']!=None:
                    if payload['targetPassword']==None and targetdata[0]!=None:
                        return("YOU ARE MISSING THE 'targetPassword' BODY OBJECT")
                    elif payload['targetPassword']!=None and targetdata[0]!=None:
                        passwordBody=payload['targetPassword']
    except:
        print('line 178')
        pass 
    try:    
        if len(targetdata[2])>0 and payload['targetUser']!=None:
                if bodyUser==payload['newUser']:
                    if bodyUser==None and targetdata[2]!=None:
                        return("YOU ARE MISSING THE 'newUser' BODY OBJECT")
                    elif bodyUser!=None and targetdata[2]!=None:
                        bodyUser=payload['newUser']
    except:
            print('line 189')
            pass
    ### CREATING ADMIN AND TARGET USER VARIABLES ####
    username= payload['user']
    password= payload['password'] 
    canupdate= payload['canupdate'] 
    gc = gspread.service_account('credentials.json')
    spreadsheet=gc.open_by_key(SHEET_ID)
    worksheet=spreadsheet.worksheet(SHEET_NAME)
    tobeupdated=spreadsheet.worksheet(TOUPDATESHEET_NAME)
    targetusercell=tobeupdated.find(payload['targetUser'])   
    ### CREATE CONDITIONS TO CONFIRM IF TARGET USER EXISTS AND IF THERE ARE CERTAIN THINGS TO BE PATCHED IN THE PAYLOAD ###
    try:
        ### CHECK IF TARGET USER EXISTS ###
        if len(payload['targetUser'])==0 and targetusercell==None:
            raise (HTTPException(status_code=400,detail="YOU ARE NOT INCLUDING A 'targetUser' IN YOUR PAYLOAD"))
    except:
        print('206')
        raise (HTTPException(status_code=404,detail="THE USER '"+payload['targetUser']+"' DOES NOT EXIST")) 
    try: 
        ### RUN VALIDATION TO MAKE UPDATES TO THE PASSWORD ###
        if len(payload['targetUser'])==0 and targetusercell==None and len(payload['targetPassword'])==0:
            raise (HTTPException(status_code=400,detail="YOU ARE NOT INCLUDING A 'targetUser' IN YOUR PAYLOAD"))      
        elif len(payload['targetUser'])!=0 and targetusercell==None and len(payload['targetPassword'])!=0:
            raise (HTTPException(status_code=404,detail="THE USER '"+payload['targetUser']+"' DOES NOT EXIST"))
    except: 
        print('line 214')
        pass
    try:
        ### RUN VALIDATION TO MAKE UPDATES TO THE TARGET USER'S NAME ###
        if len(payload['targetUser'])==0 and targetusercell==None and len(payload['targetName'])==0:   
            raise (HTTPException(status_code=404,detail="THE USER '"+payload['targetUser']+"' DOES NOT EXIST")) 
        elif len(payload['targetUser'])!=0 and targetusercell==None and len(payload['targetName'])!=0:   
            raise (HTTPException(status_code=404,detail="THE USER '"+payload['targetUser']+"' DOES NOT EXIST"))                                                 
    except: 
        print('line 225') 
        pass      
    ### CREATING VARIABLES FOR TARGET USER VALUES FOUND IN THE SPREADSHEETS ###                        
    usercell=worksheet.find(username)
    usernamevalue= worksheet.cell(usercell.row,usercell.col).value
    passwordvalue=worksheet.cell(usercell.row,usercell.col+1).value
    updatevalue=worksheet.cell(usercell.row,usercell.col+3).value
    #### CREATE 2ND VALIDATION CONDITIONS FOR ADMIN USERS ###
    if usernamevalue==None:
        raise HTTPException(status_code=401,detail="USER '"+username+ "' DOES NOT HAVE PERMISSIONS OR DOESN'T EXIST") 
    if canupdate!=updatevalue:
        raise HTTPException(status_code=401,detail="USER '"+username+ "' DOES NOT HAVE PERMISSIONS OR DOESN'T EXIST") 
    if password!=passwordvalue:
        raise HTTPException(status_code=401,detail="THE PASSWORD FOR '"+username+ "' IS NOT CORRECT") 
    elif passwordvalue==None:
        raise HTTPException(status_code=401,detail="THE PASSWORD FOR '"+username+ "' IS NOT CORRECT")
    ### CONFIRM ADMIN USERNAME ###      
    if username in usernamevalue and password in passwordvalue and updatevalue==canupdate:
        try:
            ### CONFIRM THAT THE TARGET USERNAME EXISTS ###
            if tobeupdated.cell(targetusercell.row,targetusercell.col).value==payload['targetUser']:
            ### MAKE CALL TO UPDATE THE PASSWORD FOR THE TARGET-USER ###
                try:
                    if ('targetPassword') in payload:              
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col+1,value=payload['targetPassword'])
                        return("SUCCESSFULLY UPDATED THE PASSWORD FOR "+payload['targetUser']+" IN THE DATABASE")
                    elif payload['targetPassword']==None:
                        print ('line 249')
                        pass
                except:
                    print('252')
                    pass
                try:
                ### MAKE CALL TO UPDATE THE FIRST NAME FOR THE TARGET-USER ###
                    if payload['targetName']!=None:
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col-2,value=payload['targetName'])
                        return("SUCCESSFULLY UPDATED THE FIRST NAME FOR "+payload['targetUser']+" IN THE DATABASE")
                    elif payload['targetName']==None: 
                        print('line 257')   
                        pass
                except:
                    print('line 259')
                    pass
                try:
                ### MAKE CALL TO UPDATE THE LAST NAME FOR THE TARGET-USER ###
                    if payload['targetLastname']!=None:
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col-1,value=payload['targetLastname'])
                        return("SUCCESSFULLY UPDATED THE LAST NAME FOR "+payload['targetUser']+" IN THE DATABASE")
                    elif payload['targetLastname']==None: 
                        print('line 205')   
                        pass
                except:
                    print('line 208')
                    pass
                try:
                ### MAKE CALL TO UPDATE THE NAME FOR THE TARGET-USER ###
                    if payload['targetAddress']!=None:
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col+2,value=payload['targetAddress'])
                        return("SUCCESSFULLY UPDATED THE ADDRESS FOR "+payload['targetUser']+" IN THE DATABASE")
                    elif payload['targetAddress']==None: 
                        print('line 216')   
                        pass
                except:
                    print('line 219')
                    pass
                try:
                ### MAKE CALL TO UPDATE THE CITY FOR THE TARGET-USER ###
                    if payload['targetCity']!=None:
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col+3,value=payload['targetCity'])
                        return("SUCCESSFULLY UPDATED THE CITY FOR "+payload['targetUser']+" IN THE DATABASE")
                    elif payload['targetCity']==None: 
                        print('line 227')   
                        pass
                except:
                    print('line 230')
                    pass
                try:
                ### MAKE CALL TO UPDATE THE COUNTRY FOR THE TARGET-USER ###
                    if payload['targetCountry']!=None:
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col+4,value=payload['targetCountry'])
                        return("SUCCESSFULLY UPDATED THE COUNTRY FOR "+payload['targetUser']+" IN THE DATABASE")
                    elif payload['targetCountry']==None: 
                        print('line 238')   
                        pass
                except:
                    print('line 241')
                    pass        
                try:
                ### MAKE CALL TO UPDATE THE TELEPHONE FOR THE TARGET-USER ###
                    if payload['targetPhone']!=None:
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col+5,value=payload['targetPhone'])
                        return("SUCCESSFULLY UPDATED THE TELEPHONE FOR "+payload['targetUser']+" IN THE DATABASE")
                    elif payload['targetPhone']==None: 
                        print('line 249')   
                        pass
                except:
                    print('line 252')
                    pass   
                try:
                ### MAKE CALL TO UPDATE THE ID NUMBER FOR THE TARGET-USER ###
                    if payload['targetId']!=None:
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col+6,value=payload['targetId'])
                        return("SUCCESSFULLY UPDATED THE ID NUMBER FOR "+payload['targetUser']+" IN THE DATABASE")
                    elif payload['targetId']==None: 
                        print('line 260')   
                        pass
                except:
                    print('line 263')
                    pass      
                try:
                ### MAKE CALL TO UPDATE THE ID TYPE FOR THE TARGET-USER ###
                    if payload['targetIdType']!=None:
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col+7,value=payload['targetIdType'])
                        return("SUCCESSFULLY UPDATED THE COUNTRY FOR "+payload['targetUser']+" IN THE DATABASE")
                    elif payload['targetIdType']==None: 
                        print('line 260')   
                        pass
                except:
                    print('line 263')
                    pass            
                try:
                ### MAKE CALL TO UPDATE THE NAME FOR THE TARGET-USER ###
                    if payload['newUser']!=None and tobeupdated.find(payload['newUser'])==None:
                        tobeupdated.update_cell(targetusercell.row,targetusercell.col,value=payload['newUser'])
                        return("SUCCESSFULLY UPDATED THE USERNAME FOR "+payload['targetUser']+ " TO "+payload['newUser']+ " IN THE DATABASE")
                    elif payload['newUser']==None: 
                        print('line 257')   
                        pass
                except:
                    print('line 275')
                    yield("CONFIRM THAT THE TARGET NEWUSERNAME DOES NOT ALREADY EXIST")
        except:  
            raise HTTPException(status_code=404,detail="USER " +payload['targetUser'] +" DOESN'T EXIST")              
    else:
        raise HTTPException(status_code=404,detail="USER DOES NOT HAVE PERMISSIONS OR DOESN'T EXIST")
        #if ('targetUser') in payload:

        
        
