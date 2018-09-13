from CallDetails import callDetails

def ESTtoPST(estTime): 
   pstTime = estTime - 300;
   return pstTime;


callVar4 = "";
callVar6 = "";
callEcc29 = "";
callEcc30 = "";
callEcc31 = "";
logTime = "";
sessionID = "";
intLogTime = 0;
timeDiff = 0;
callDet = callDetails()
callsList = []
firstPrintFlag = 0;
begIndex = 0

print("Enter the timestamp: ")
print()
estTimeIn = int(input());

pstTimeIn = ESTtoPST(estTimeIn);

fh = open('icm_jsp.log')
for line in fh:

   logTime = line[11:16] 
   logTime = logTime.replace(":",""); 
   intLogTime = int(logTime);
   timeDiff = intLogTime - pstTimeIn;

   if(intLogTime > pstTimeIn and timeDiff <= 5 ):
      ########Get Session ID###########
      if(line.find("CED") != -1):
         callDet = callDetails();
         begIndex = line.rfind(" ")
         sessionID = line[begIndex:]
         
         if(sessionID.find("'") == -1):	   
            callDet.sessionID = sessionID.strip();
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
            
for callObj in callsList:
   if(firstPrintFlag == 0):
      print("\n" + str(len(callsList)) + " Result(s) were found :  \n");
      firstPrintFlag = 1;

      
   print("Timestamp :  " + callObj.callTime);
   print("SessionID :  " + callObj.sessionID);
   print("CallVariable4 :  " + callObj.callVar4);
   print("CallVariable6 :  " + callObj.callVar6);
   print("Ecc_29 :  " + callObj.callVarEcc29);	
   print("Ecc_30 :  " + callObj.callVarEcc30);	
   print("Ecc_31 :  " + callObj.callVarEcc31 + "\n");	          

                            
if (len(callsList) > 0):
   print("\nWould you like to print the results to a txt document? Y/N")
   print()
   printFlag = input();
   
   if(printFlag.lower() == "y" ):
      outputFile = open("Output.txt", "w");
      for callObj2 in callsList:
         outputFile.write("Timestamp :  " + callObj2.callTime + "\n");
         outputFile.write("SessionID :  " + callObj2.sessionID + "\n");
         outputFile.write("CallVariable4 :  " + callObj2.callVar4 + "\n");
         outputFile.write("CallVariable6 :  " + callObj2.callVar6 + "\n");
         outputFile.write("Ecc_29 :  " + callObj2.callVarEcc29 + "\n");	
         outputFile.write("Ecc_30 :  " + callObj2.callVarEcc30 + "\n");	
         outputFile.write("Ecc_31 :  " + callObj2.callVarEcc31 + "\n");
         outputFile.write("");

      
      outputFile.close();	
      print("\n" + "Output file has been successfully created.");   

         

                 

