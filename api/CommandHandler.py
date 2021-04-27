import datetime, re, csv

class CommandHandler:
    def initRegexKataPenting(self):
        self.regex_kata_penting = r""
        for i in range(0, len(self.kata_penting)): 
            if(i < len(self.kata_penting)-1): self.regex_kata_penting += self.kata_penting[i] + "|"
            else: self.regex_kata_penting += self.kata_penting[i]

    def __init__(self, message):
        self.reqMessage = message
        self.resMessage = ""
        self.kata_penting = ["kuis", "ujian", "tucil", "tubes", "praktikum"]
        self.initRegexKataPenting()
        
    def addTaskCmd(self):
        deadline = re.findall(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}", self.reqMessage)
        kode_matkul = re.findall(r"[A-Z]{2}[0-9]{4}", self.reqMessage)
        jenis_task = re.findall(self.regex_kata_penting, self.reqMessage)
        topik = re.findall(r"(?<=\s[A-Z]{2}[0-9]{4}\s).*(?=\s.*[0-9]{2}\/[0-9]{2}\/[0-9]{4})", self.reqMessage)
        if(len(topik) == 0): topik = re.findall(r"(?<=\s[A-Z]{2}[0-9]{4}\s).*$", self.reqMessage)

        if(deadline and kode_matkul and jenis_task and topik):
            #tambahkan task ke database
            with open('database.csv', 'r') as fileDB:
                db_reader = csv.reader(fileDB, delimiter=',')
                nRows = sum(1 for row in db_reader)

            with open('database.csv', 'a') as fileDB:
                db_writer = csv.writer(fileDB, delimiter=',')
                db_writer.writerow([nRows, datetime.datetime.now().strftime("%d/%m/%Y"), deadline[0], jenis_task[0], topik[0], 0])
            self.resMessage = f"[TASK BERHASIL DICATAT]\n(ID: {nRows}) - {deadline[0]} - {jenis_task[0]} - {topik[0]}"
            return True
        else:
            return False
    
    def helpCmd(self):
        # Cari kata kunci "Assistant" dan "bisa"
        k1 = re.search(r"Assistant", self.reqMessage, flags=re.IGNORECASE)
        k2 = re.search(r"bisa", self.reqMessage, flags=re.IGNORECASE)
        
        if(k1 and k2):
            resMsg = "[Fitur]\n1. Menambahkan task baru\n2. Melihat daftar task\n3. Menampilkan deadline dari suatu task tertentu\n4. Memperbaharui task tertentu\n5. Menandai suatu task telah selesai dikerjakan\n6. Menampilkan opsi help\n"
            resMsg += "\n[Daftar kata penting]\n"
            
            it_kata = 0
            for kata in self.kata_penting:
                it_kata += 1
                resMsg += str(it_kata) + ". " + kata + '\n'
            
            self.resMessage = resMsg
            return True
        else:
            return False

    def getTaskRecorded(self):
        msg = self.reqMessage.lower()
        rkey = r"^(?=.*\bapa\b)"
        key1 = ""
        key1 += rkey +r"(?=.*\b({})\b).*".format("deadline") 
        for i in self.kata_penting:
            key1 += r"|"+ rkey + r"(?=.*\b({})\b).*".format(i)
        key1 +=r"$"
        kata_kunci1 = re.findall(key1,msg)
        if (len(kata_kunci1)==0): return "",False
        key2 = r"\b(hari ini)\b|\b(sejauh ini)\b|(\d{2}\/\d{2}\/\d{4})\b \w+ (\d{2}\/\d{2}\/\d{4}\b)|\b(\d+)\b \b(\w+)\b ke depan"
        kata_kunci2 = re.findall(key2,msg)
        if (len(kata_kunci2)==0): return "",False
        kata_kunci1 = [x for x in kata_kunci1[0] if x!=""]
        kata_kunci2 = kata_kunci2[0]
        with open('database.csv', 'r') as fileDB:
            db_reader = csv.reader(fileDB, delimiter=',')
            next(db_reader, None)
            msgformat = "(ID: {}) {} - {} - {} - {}"
            retmsg = "[{}]".format("Daftar Deadline")
            today = datetime.datetime.now().strftime("%d/%m/%Y")
            if(kata_kunci2[0]!=""):
                for i in db_reader:
                    if(i[2] == today and kata_kunci1[0] == "deadline" and i[5]=="0"):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    elif(i[2] == today and kata_kunci1[0] == i[3] and i[5]=="0"):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    else:
                        continue
            elif(kata_kunci2[1]!=""):
                for i in db_reader:
                    if(kata_kunci1[0] == "deadline" and i[5]=="0"):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    elif(kata_kunci1[0] == i[3] and i[5]=="0"):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    else:
                        continue
            elif(kata_kunci2[2]!="" and kata_kunci2[3]!=""):
                dateawal = datetime.datetime.strptime(kata_kunci2[2], '%d/%m/%Y')
                dateakhir = datetime.datetime.strptime(kata_kunci2[3], '%d/%m/%Y')
                for i in db_reader:
                    datedb = datetime.datetime.strptime(i[2], '%d/%m/%Y')
                    if(kata_kunci1[0] == "deadline" and i[5]=="0" and dateawal <= datedb and dateakhir>= datedb):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    elif(kata_kunci1[0] == i[3] and i[5]=="0" and dateawal <= datedb and dateakhir>= datedb):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3],i[4])
                    else:
                        continue
            elif(kata_kunci2[4]!="" and kata_kunci2[5]!=""):
                todaydate = datetime.datetime.strptime(today, '%d/%m/%Y')
                movedate = todaydate
                if(kata_kunci2[5] == "hari"):
                    movedate = movedate + datetime.timedelta(days=int(kata_kunci2[4]))
                else: # elif (kata_kunci1[5] == minggu)
                    movedate = movedate + datetime.timedelta(weeks=int(kata_kunci2[4]))
                for i in db_reader:
                    datedb = datetime.datetime.strptime(i[2], '%d/%m/%Y')
                    if(kata_kunci1[0] == "deadline" and i[5]=="0" and todaydate <= datedb and movedate>= datedb):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    elif(kata_kunci1[0] == i[3] and i[5]=="0" and todaydate <= datedb and movedate>= datedb):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3],i[4])
                    else:
                        continue
            else:
                pass
            if (retmsg == "[Daftar Deadline]"): retmsg = "Tidak ditemukan task"
            self.resMessage = retmsg
            return True

def handleMessage(message):
    c = CommandHandler(message)
    c.addTaskCmd()
    c.helpCmd()
    c.getTaskRecorded()

    return c.resMessage

if __name__ == "__main__":
    #Untuk testing
    reqMessage = "apa saja deadline 3 hari ke depan?"
    resMessage = handleMessage(reqMessage)
    if(resMessage):
        print(resMessage)
    else:
        print("Maaf, pesan tidak dikenali")

