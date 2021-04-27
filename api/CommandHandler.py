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
        self.kata_penting = ["kuis", "ujian", "tucil", "tubes", "praktikum", "deadline"]
        self.typoWord= []
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

    def checkMsgTypo(self):
        reqMsgSplit = self.reqMessage.split()
        typoWord = []
        
        for i in range(0, len(reqMsgSplit)):
            for j in range(0, len(self.kata_penting)):
                kataPenting_len = len(self.kata_penting[j])
                reqMsgSplit_i_len = len(reqMsgSplit[i])

                kemiripan = max(0, 1-levenshteinDistance(reqMsgSplit[i], self.kata_penting[j])/(max(reqMsgSplit_i_len, kataPenting_len)))

                if(kemiripan*100 > 75 and kemiripan != 1):
                    reqMsgSplit[i] = self.kata_penting[j]
                    typoWord.append(self.kata_penting[j])
                    break
        
        self.typoWord = typoWord
        if(len(self.typoWord) != 0): self.resMessage = "Mungkin maksud kamu: " + ' '.join(reqMsgSplit)
        else: self.resMessage = ""
        
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
        kata_kunci1 = [x!="" for x in kata_kunci1]
        with open('database.csv', 'r') as fileDB:
            db_reader = csv.reader(fileDB, delimiter=',')
            retmsg = "[{}]\n".format("Daftar Deadline")
            if(kata_kunci2[0]!=""):
                today = datetime.datetime.now().strftime("%d/%m/%Y")
                for i in db_reader:
                    if(i[1] == today):
                        retmsg += "(ID: {}) {} - {} - {}".format(i[0],i[1],i[2],i[3]) + "\n"               
                return retmsg, True 
            elif(kata_kunci2[1]!=""):
                return retmsg
            elif(kata_kunci2[2]!=""):
                return retmsg
            else:
                return retmsg


def levenshteinDistance(src, dst):
    # Dynamic Programming, Bottom Up
    # d[i][j], adalah jarak levenshtein dengan prefix src ke i dan prefix dst ke j
    n = len(src)
    m = len(dst)
    d = [[0 for j in range(m+1)] for i in range(n+1)]
    
    #Kasus Base
    # kasus ketika src = "", berarti costnya = jumlah insert semua karakter dst ke src
    for j in range(m+1): d[0][j] = j

    #kasus ketika dst = "", berarti costnya = jumlah delete semua karakter src
    for i in range(n+1): d[i][0] = i

    #Kasus Transitional
    for i in range(1, len(src)+1):
        for j in range(1, len(dst)+1):
            if(src[i-1] == dst[j-1]):
                sub_cost = 0
            else:
                sub_cost = 1
            # Insert/delete/substitusi
            d[i][j] = min(d[i][j-1]+1, min(d[i-1][j]+1, d[i-1][j-1]+sub_cost))
    
    return d[n][m]

def handleMessage(message):
    c = CommandHandler(message)
    c.checkMsgTypo()
    c.addTaskCmd()
    c.helpCmd()
    c.getTaskRecorded()

    return c.resMessage, c.typoWord

if __name__ == "__main__":
    # #Untuk testing
    # reqMessage = "Apa yang bisa assistant bisa lakukan"
    # resMessage = handleMessage(reqMessage)
    # if(resMessage):
    #     print(resMessage)
    # else:
    #     print("Maaf, pesan tidak dikenali")

    res, typoWord = handleMessage("Apa saja dedline yang ada sejauh ini?")
    print(res)
    print(typoWord)