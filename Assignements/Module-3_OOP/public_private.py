# class studeninfo():

#     stid = 12
#     stnm = "kaushal"

#     def getdata(self):
#         print("This is getdata!")
#         print("ID:",self.stid)
#         print("Name:",self.stnm)


# st = studeninfo()
# print("ID:",st.stid)
# print("Name:",st.stnm)
# st.getdata()        


class studeninfo():

    __stid = 12
    __stnm = "kaushal"

    def __getdata(self):
        print("This is getdata!")
        print("ID:",self.__stid)
        print("Name:",self.__stnm)

    def printdata(self):
        print("This is printdata!")
        print("ID:",self.__stid)
        print("Name:",self.__stnm)

st = studeninfo()
# print("ID:",st.stid)
# print("Name:",st.stnm)
# st.getdata()        
st.printdata()
