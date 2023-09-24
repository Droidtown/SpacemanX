#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# FileName: spaceman.py
# Developer: Peter. w (peterwolf.wang@gmail.com)
# File establishment date: 2012.04.12
# Last modification date: 2023.09.24
# Version 0.99

import platform
import unicodedata
import sys
import os

def makeroom(inputSTR="", inputFile=None, mode="modest"):
    if inputSTR == "" and inputFile != None:
        fileInfo = {"fileName": ".".join(inputFile.replace("../../../", "").split(".")[:-1]), "fileType": inputFile.split(".")[-1]}

        if os.path.exists(inputFile):
            if fileInfo["fileType"] == "txt":
                pass
            else:
                print("\n Error! The file specified may not be a text file.")
                return None
        else:
            print("\n Error! File not found! Please check the file name specified.")
            return None

        inputLIST = []
        f = open(inputFile, "r")
        for i in f.readlines():
            inputLIST.append(i.decode("utf-8"))
    elif inputSTR != "" and inputFile == None:
        inputLIST = inputSTR.split("\n")

    fullWidthPunctuation = (u"，", u"。", u"、", u"．", u"‧", u"／", u"＼", u"：", u"；", u"！", u"？", u"「", u"」", u"｢", u"｣", u"《", u"》")
    toBeUnifiedTokenTuple = ( ## Unifying the style of the paragraphes input.
                            (u"  ", u" "),
                            (u"	", u" "),
                            (u"“", u"\""),
                            (u"‘", u"'"),
                            (u"”", u"\""),
                             #Replace binary brackets with unitary brackets.
                            (u"（", u"("),
                            (u"）", u")"),
                            (u"﹝", u"("),
                            (u"﹞", u")"),
                            (u"〈", u"("),
                            (u"〉", u")"),
                            (u"％", u"%"),
                             #Remove redundant space.
                            (u"( ", u"("),
                            (u" )", u")"),
                            (u" (", u"("),
                            (u") ", u")"),
                            (u"[ ", u"["),
                            (u" ]", u"]"),
                            (u" [", u"["),
                            (u"] ", u"]"),
                            (u"{ ", u"{"),
                            (u" }", u"}"),
                            (u" {", u"{"),
                            (u"} ", u"}"),
                            (u"\" ", u"\""),
                            (u" \"", u"\""),
                            )
    outputList = []
    quotationCounter = 0

    for i in inputLIST:

        # Preserving the character at the very end of the last paragraph for it will not be processed later.
        tail = ""
        if inputLIST.index(i) == len(inputLIST) - 1:
            tail = i[-1]

        for token in toBeUnifiedTokenTuple:
            i = i.replace(token[0], token[1])

        tmpString = ""
        for j in range(0, len(i)-1):

            if i[j] == u"(" and j > 0:
                if mode == "strong":
                    tmpString = tmpString + u" " + i[j] + u" "
                elif mode == "modest":
                    tmpString = tmpString + u" " + i[j]
                else: #mode == "weak"
                    tmpString = tmpString + i[j]
            elif i[j] == u")" and j > 0:
                if mode == "strong":
                    tmpString = tmpString + u" " + i[j] + u" "
                elif mode == "modest":
                    tmpString = tmpString + i[j] + u" "
                else: #mode == "weak"
                    tmpString = tmpString + i[j]
            elif i[j] == u"[" and j > 0:
                if mode == "strong":
                    tmpString = tmpString + u" " + i[j] + u" "
                elif mode == "modest":
                    tmpString = tmpString + u" " + i[j]
                else: #mode == "weak"
                    tmpString = tmpString + i[j]
            elif i[j] == u"]" and j > 0:
                if mode == "strong":
                    tmpString = tmpString + u" " + i[j] + u" "
                elif mode == "modest":
                    tmpString = tmpString + i[j] + u" "
                else: #mode == "weak"
                    tmpString = tmpString + i[j]
            elif i[j] == u"{" and j > 0:
                if mode == "strong":
                    tmpString = tmpString + u" " + i[j] + u" "
                elif mode == "modest":
                    tmpString = tmpString + u" " + i[j]
                else: #mode == "weak"
                    tmpString = tmpString + i[j]
            elif i[j] == u"}" and j > 0:
                if mode == "strong":
                    tmpString = tmpString + u" " + i[j] + u" "
                elif mode == "modest":
                    tmpString = tmpString + i[j] + u" "
                else: #mode == "weak"
                    tmpString = tmpString + i[j]
            elif i[j] == u"\"" and j > 0:
                if mode == "strong":
                    tmpString = tmpString + u" " + i[j] + u" "
                elif mode == "modest":
                    if quotationCounter == 0:
                        tmpString = tmpString + u" " + i[j]
                        quotationCounter = quotationCounter + 1
                    else:
                        tmpString = tmpString + i[j] + u" "
                        quotationCounter = quotationCounter - 1
                else: #mode == "weak"
                    tmpString = tmpString + i[j]

            elif unicodedata.east_asian_width(i[j]) in ("N", "A", "Na"): # Dealing with some letters in some European languages.
                if unicodedata.east_asian_width(i[j+1]) not in ("N", "A", "Na", " "):
                    tmpString = tmpString + i[j] + u" "
                else:
                    tmpString = tmpString + i[j]

            elif unicodedata.east_asian_width(i[j]) == unicodedata.east_asian_width(i[j+1]):
                tmpString = tmpString + i[j]

            else:
                if i[j+1] not in (u"(", u")", u"[", u"]", u"{", u"}", u"\""):
                    tmpString = tmpString + i[j] + u" "
                else:
                    tmpString = tmpString + i[j]

            while u"  " in tmpString:
                tmpString = tmpString.replace(u"  ", u" ")

            if mode == "strong":
                pass
            else: #mode == "modest" or mode == "weak"
                for k in fullWidthPunctuation:
                    tmpString = tmpString.replace(u" %s" % k, k)
                    tmpString = tmpString.replace(u"%s " % k, k)
                tmpString = tmpString.replace(u" ’ ", u"’")
                tmpString = tmpString.replace(u" : ", u": ")
                tmpString = tmpString.replace(u" / ", u"/")

            # Dealing with the situations when brackets or quotation marker appears at the very beginning of a line.
            if tmpString[0] in (u"(", u"[", u"{", u"\"") and tmpString[1:2] == u" ":
                if mode == "strong":
                    pass
                else: #mode == "modest" or mode == "weak":
                    for m in (u"(", u"[", u"{", u"\""):
                        if tmpString[0:2] == u"%s " % m:
                            tmpString = tmpString[0:2].replace(u"%s " % m, u"%s" % m)
            # Remove the space at the very beginning of a line.
            if tmpString[0] == " ":
                tmpString = tmpString[1:]
            else:
                pass
        outputList.append(tmpString)

    # Recovering the character appears at the very end of the last paragraph in the text file input.
    outputList[-1] = outputList[-1] + tail

    if inputSTR == "" and inputFile != None:
        # Setting directory prefix.
        if platform.system() == "Darwin":
            outputDir = "../../../Spaceman_Output/"
        else:
            outputDir = "./Spaceman_Output/"

        # Checking if the directory exists already.
        if os.path.exists(outputDir):
            pass
        else:
            os.mkdir(outputDir)

        # Saving the file into Spaceman_Output directory.
        outputFile = open(outputDir+fileInfo["fileName"]+"_output.txt", "w")
        for i in outputList:
            outputFile.write(i.encode("utf-8")+"\n")

        outputFile.close()
    elif inputSTR != "" and inputFile == None:
        return "\n".join(outputList)

if __name__ == "__main__":
    if platform.system() == "Linux":
        try:
            fileName = sys.argv[1]
        except IndexError:
            fileName = ""
        try:
            mode = sys.argv[2][2:]
        except IndexError:
            mode = ""
        if fileName == "":
            print("Please specify a text file for process.")
        else:
            if mode == "" or mode not in ("strong", "modest", "weak"):
                print("\nPlease specify mode. \n(spaceman.py supoort '--strong', '--modest' and '--weak' modes.) \nUsage: $ python spaceman.py [text File] [mode]")
            else:
                makeroom(fileName, mode)

    elif platform.system() == "Windows":
        fileNameList = []
        for i in os.listdir("./"):
            if i.split(".")[-1] == "txt":
                fileNameList.append("./"+i)
        for i in fileNameList:
            makeroom(i, mode="modest")

    elif platform.system() == "Darwin":
        print(os.getcwd())
        fileNameList = []
        for i in os.listdir("../../../"):
            if i.split(".")[-1] == "txt":
                fileNameList.append("../../../"+i)

        for i in fileNameList:
            makeroom(i, mode="modest")
