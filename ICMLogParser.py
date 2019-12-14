from CallDetails import callDetails

########Functions Start###########

def ESTtoPST(estTime): 
   pstTime = estTime - 300;
   return pstTime;
   
def findVars(pstTimeIn, passedInSessID, passedMode):
    callsList = [];
    callVar4 = "";
    callVar6 = "";
    callEcc29 = "";
    callEcc30 = "";
    callEcc31 = "";
    sessionID = "";
    intLogTime = 0;
    timeDiff = 0;
    callDet = callDetails();
    begIndex = 0;
    sessIDCount = 0;
        
    fh = open('icm_jsp.log')
    for line in fh:

       logTime = line[11:16] 
       logTime = logTime.replace(":",""); 
       intLogTime = int(logTime);
       timeDiff = intLogTime - pstTimeIn;
       
       
       ########Get Session ID for ID Search###########
       if(line.find("CED") != -1):
         begIndex = line.rfind(" ")
         sessionID = line[begIndex:]
         
         if(sessionID.find("'") == -1):	   
            sessionID = sessionID.strip();
            sessionID = sessionID[1:-1];

       if( (passedMode == "time" and intLogTime > pstTimeIn and timeDiff <= 5) or (sessionID == passedInSessID and sessIDCount <= 25) ):
          ########Get Session ID###########
          sessIDCount += 1;
          if(line.find("CED") != -1):
             callDet = callDetails();
             begIndex = line.rfind(" ")
             sessIDTemp = line[begIndex:];
             
             if(sessIDTemp.find("'") == -1):	   
                callDet.sessionID = sessIDTemp.strip();
                callDet.callTime = logTime.strip();

          #//////////Get Variable 4///////////////
          elif (line.find("CallVariable4") != -1):
             begIndex = line.rfind(" ")
             callVar4 = line[begIndex:];
             if(callVar4.find("'")  == -1):
                callDet.callVar4 = callVar4.strip();
                
          #//////////Get Variable 6///////////////
          elif (line.find("CallVariable6") != -1):
             begIndex = line.rfind("[")
             callVar6 = line[begIndex:];
             if(callVar6.find("'")  == -1):
                callDet.callVar6 = callVar6.strip();
          
          # //////////Get Variable ECC_29///////////////      
          elif (line.find("user_ECC_29") != -1):
             begIndex = line.rfind("[")
             callEcc29 = line[begIndex:];
             if(callEcc29.find("'")  == -1 and callEcc29.find("ced") == -1):
                callDet.callVarEcc29 = callEcc29.strip();
          
          # //////////Get Variable ECC_30///////////////     
          elif (line.find("user_ECC_30") != -1):
             begIndex = line.rfind("[")
             callEcc30 = line[begIndex:];
             if(callEcc30.find("'")  == -1 and callEcc30.find("ced") == -1):
                callDet.callVarEcc30 = callEcc30.strip();
                
           # //////////Get Variable ECC_31///////////////     
          elif (line.find("user_ECC_31") != -1):
             begIndex = line.rfind("[")
             callEcc31 = line[begIndex:];
             if(callEcc31.find("'")  == -1 and callEcc31.find("ced") == -1):
                callDet.callVarEcc31 = callEcc31.strip();
                callsList.append(callDet)
    
    return callsList;
    
def printResults(multiMap, userInputCallsList):
    for x in userInputCallsList:
        callsList = multiCallMap[x];
        firstPrintFlag = 0;
        
        if(len(callsList) > 0):
        
            for callObj in callsList:
               if(firstPrintFlag == 0):
                  print("\n" + str(len(callsList)) + " Result(s) were found for: "+ str(x) + "\n");
                  firstPrintFlag = 1;

                  
               print("Timestamp :  " + callObj.callTime);
               print("SessionID :  " + callObj.sessionID);
               print("CallVariable4 :  " + callObj.callVar4);
               print("CallVariable6 :  " + callObj.callVar6);
               print("Ecc_29 :  " + callObj.callVarEcc29);	
               print("Ecc_30 :  " + callObj.callVarEcc30);	
               print("Ecc_31 :  " + callObj.callVarEcc31 + "\n");
        else:
            print("\nNo resuts found for: " + str(x));
        

def outputResults(multiMap, userInputCallsList):
    printFlag = "n";
    firstPrintFlag = 0;	
    outputFile = open("Output.txt", "w");
    for x in userInputCallsList:
       callsList = multiCallMap[x];   
       
       if (len(callsList) > 0):
           print("\nWould you like to print the results to a txt document? Y/N")
           print()
           printFlag = input();
           if(printFlag.lower() == "y" ):
              for callObj2 in callsList:
                 if(firstPrintFlag == 0):			  
                   outputFile.write(str(len(callsList)) + " Result(s) were found for: "+ str(x) + "\n");
                   firstPrintFlag = 1			   
                 outputFile.write("Timestamp :  " + callObj2.callTime + "\n");
                 outputFile.write("SessionID :  " + callObj2.sessionID + "\n");
                 outputFile.write("CallVariable4 :  " + callObj2.callVar4 + "\n");
                 outputFile.write("CallVariable6 :  " + callObj2.callVar6 + "\n");
                 outputFile.write("Ecc_29 :  " + callObj2.callVarEcc29 + "\n");	
                 outputFile.write("Ecc_30 :  " + callObj2.callVarEcc30 + "\n");	
                 outputFile.write("Ecc_31 :  " + callObj2.callVarEcc31 + "\n");
                 outputFile.write("\n");

       else:
           outputFile.write("No resuts found for: " + str(x));
       
    outputFile.close();
    if(printFlag.lower() == "y" ):
        print("\n" + "Output file has been successfully created.");


########Functions End###########



##################
#   Main Start   #
##################

modeFlag = "";
pstTimeIn = 0;
sessID = "";
callArray = [];
multiCallMap = {};

print("Enter the timestamp or the session ID: ")
print()

userInput = input();

if(userInput.find(",") != -1):
    modeFlag = "time";
    callArray = userInput.split(",");
    
elif(len(userInput) > 4):
    modeFlag = "id";
    sessID = userInput.strip();
    callArray.append(sessID);
else:
    modeFlag = "time";
    estTimeIn = int(userInput);
    callArray.append(estTimeIn);

for callTimeORSessID in callArray:
    if(modeFlag == "time"):
        foundCallsList = findVars(ESTtoPST(int(callTimeORSessID)), "dummy", modeFlag);
    else:
        foundCallsList = findVars(0, callTimeORSessID, modeFlag);
    
    multiCallMap[callTimeORSessID] = foundCallsList;
            
printResults(multiCallMap, callArray);

outputResults(multiCallMap, callArray);
                            
   

         

                 

