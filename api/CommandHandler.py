import datetime, re, csv, shutil
from tempfile import NamedTemporaryFile
import sys, os.path
dir_cmd = (os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
sys.path.append(dir_cmd)

class CommandHandler:
    def __init__(self, message):
        self.reqMessage = message
        self.resMessage = ""
        self.kata_penting = [
        "kuis", "ujian", "tucil", "tubes", "praktikum",
         "uts", "uas", "pr", "tugas", "milestone"
        ]
        self.kata_tugas = [
            "tucil", "tubes", "tugas", "pr", "milestone"
        ]
        self.kata_petunjuk_waktu = [
            "pada", "buat", "pas", "tanggal", "dikumpul", "deadline"
        ]
        self.kata_bulan = {
        "januari" : 1, "februari" : 2, "maret" : 3, "april" : 4, "mei" : 5, 
        "juni" : 6, "juli" : 7, "agustus" : 8, "september" : 9, 
        "oktober" : 10, "november" : 11, "desember" : 12
        }
        self.kata_perbarui = [
            "ganti", "ubah", "diundur", "diganti", "diubah", "jadi" 
        ]
        self.fieldnames = ["id", "tgl_dibuat", "deadline", "jenis_task","kode_matkul", "topik", "is_finished"]

        
    def addTaskCmd(self):
        # Cari jenis task
        jenis_task = re.findall(r"(?<!\w)("+'|'.join(self.kata_penting)+r")(?!\w)", self.reqMessage, re.IGNORECASE)
        if(len(jenis_task) > 0):
            # Cari deadline
            deadline = []
            # Kalau bentuk tanggalnya seperti "12 April" atau "3 Oktober"
            tanggal = re.findall(r"([1-9][0-9]?)\s("+'|'.join(list(self.kata_bulan))+r")", self.reqMessage, re.IGNORECASE)
            if(len(tanggal) != 0): 
                deadline.append(datetime.datetime(datetime.date.today().year, self.kata_bulan[tanggal[0][1].lower()], int(tanggal[0][0])))
            else: 
                # Kalau bentuknya DD/MM/YYYY
                tanggal = re.findall(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}", self.reqMessage)
                if(len(tanggal) > 0):
                    tanggal = tanggal[0].split('/')
                    tanggal.reverse()
                    yr, mo, day =  [int(x) for x in tanggal]
                    deadline.append(datetime.datetime(yr, mo, day))

            # Cari kode matkul    
            kode_matkul = re.findall(r"[A-Z]{2}[0-9]{4}", self.reqMessage)
            
            # Cari topik
            topik = re.findall(r"(?<=\s[A-Z]{2}[0-9]{4}\s).*(?=\s.*[0-9]{2}\/[0-9]{2}\/[0-9]{4})", self.reqMessage)
            if(len(topik) == 0): topik = re.findall(r"(?<=\s[A-Z]{2}[0-9]{4}\s).*$", self.reqMessage)

            # Parsing kata petunjuk waktu dari topik
            if(len(tanggal) > 0):
                katatopik = topik[0]
                for katawaktu in (self.kata_petunjuk_waktu + list(tanggal[0])):
                    matchIndex = boyerMooreMatch(katatopik, katawaktu)
                    if(matchIndex > -1):
                        katatopik = katatopik[0:matchIndex] + katatopik[matchIndex + len(katawaktu) + 1:] 
                topik[0] = katatopik
            
            if(deadline and kode_matkul and jenis_task and topik):
                #tambahkan task ke database
                with open('database.csv', 'r', newline='') as fileDB:
                    db_reader = csv.reader(fileDB, delimiter=',')
                    nRows = sum(1 for row in db_reader)

                with open('database.csv', 'a', newline='') as fileDB:
                    db_writer = csv.writer(fileDB, delimiter=',')
                    db_writer.writerow([nRows, datetime.datetime.now().strftime("%d/%m/%Y"), deadline[0].strftime("%d/%m/%Y"), jenis_task[0], kode_matkul[0], topik[0], 0])
                self.resMessage = f"[TASK BERHASIL DICATAT]\n(ID: {nRows}) - " + deadline[0].strftime("%d/%m/%Y") + f"- {jenis_task[0]} - {kode_matkul[0]} - {topik[0]}"
                return True
            else:
                return False
    
    def renewTask(self):
        # Pengecekan apakah kalimat menunjukkan tanda-tanda pembaruan task
        ganti_task = re.findall(r"(?<!\w)("+'|'.join(self.kata_perbarui)+r")(?!\w)", self.reqMessage, re.IGNORECASE)
        if(len(ganti_task) > 0):
            # Cari tanggal yang baru
            deadline = []
            # Kalau bentuk tanggalnya seperti "12 April" atau "3 Oktober"
            tanggal = re.findall(r"([1-9][0-9]?)\s("+'|'.join(list(self.kata_bulan))+r")", self.reqMessage, re.IGNORECASE)
            if(len(tanggal) != 0): 
                deadline.append(datetime.datetime(datetime.date.today().year, self.kata_bulan[tanggal[0][1].lower()], int(tanggal[0][0])))
            else: 
                # Kalau bentuknya DD/MM/YYYY
                tanggal = re.findall(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}", self.reqMessage)
                if(len(tanggal) > 0):
                    tanggal = tanggal[0].split('/')
                    tanggal.reverse()
                    yr, mo, day =  [int(x) for x in tanggal]
                    deadline.append(datetime.datetime(yr, mo, day))
            
            # Cari nomor task
            noTask = re.findall(r"task\s[1-9][0-9]*", self.reqMessage, re.IGNORECASE)
            if(len(noTask) > 0):
                noTask[0] = noTask[0][5:]
                
            # Update ke database
            
            if(noTask and deadline):
                topik = 0
                jenis_task = 0
                found = False
                tempfile = NamedTemporaryFile(mode="w", delete=False, newline="")
                with open('database.csv', 'r', newline='') as csvfile, tempfile:
                    reader = csv.DictReader(csvfile, fieldnames = self.fieldnames)
                    writer = csv.DictWriter(tempfile, fieldnames = self.fieldnames)
                    for row in reader:
                        if noTask[0] == row["id"]:
                            row["deadline"] = deadline[0].strftime("%d/%m/%Y")
                            found = True
                            topik = row["topik"]
                            jenis_task = row["jenis_task"]
                        writer.writerow({"id": row["id"], "tgl_dibuat": row["tgl_dibuat"],"deadline": row["deadline"],
                        "jenis_task": row["jenis_task"],"topik": row["topik"],"kode_matkul" : row["kode_matkul"], "is_finished": row["is_finished"]})
                shutil.move(tempfile.name, "database.csv")
                if(found):
                    self.resMessage = f"[TASK BERHASIL DIUBAH]\n(ID: {noTask[0]}) - " + deadline[0].strftime("%d/%m/%Y") + f"- {jenis_task} - {topik}"
                else: self.resMessage = "Maaf, task yang kamu cari tidak ada"
                return found     


    def helpCmd(self):
        # Cari kata kunci "Assistant" dan "bisa"
        k1 = re.search(r"Assistant", self.reqMessage, flags=re.IGNORECASE)
        k2 = re.search(r"bisa", self.reqMessage, flags=re.IGNORECASE)
        
        if(k1 and k2):
            resMsg = "\n[Fitur]\n1. Menambahkan task baru\n2. Melihat daftar task\n3. Menampilkan deadline dari suatu task tertentu\n4. Memperbaharui task tertentu\n5. Menandai suatu task telah selesai dikerjakan\n6. Menampilkan opsi help\n"
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
            for listOfKeyword in self.kata_penting, self.kata_perbarui, self.kata_petunjuk_waktu:
                for keyword in listOfKeyword:
                    kataPenting_len = len(keyword)
                    reqMsgSplit_i_len = len(reqMsgSplit[i])

                    kemiripan = max(0, 1-levenshteinDistance(reqMsgSplit[i], keyword)/(max(reqMsgSplit_i_len, kataPenting_len)))
                    if(kemiripan*100 > 75 and kemiripan != 1):
                        reqMsgSplit[i] = keyword
                        typoWord.append(keyword)
                        break

        self.typoWord = typoWord
        if(len(self.typoWord) != 0): self.resMessage = "Mungkin maksud kamu: \n" + ' '.join(reqMsgSplit)
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
        kata_kunci1 = [x for x in kata_kunci1[0] if x!=""]
        if (len(kata_kunci1)==0): return "",False
        key2 = r"\b(hari ini)\b|\b(sejauh ini)\b|(\d{2}\/\d{2}\/\d{4})\b \w+ (\d{2}\/\d{2}\/\d{4}\b)|\b(\d+)\b \b(\w+)\b ke depan"
        kata_kunci2 = re.findall(key2,msg)
        msgformat = "(ID: {}) {} - {} - {} - {}"
        retmsg = "[{}]".format("Daftar Deadline")
        if (len(kata_kunci2)==0): 
            if(kata_kunci1[0]=="deadline"):
                with open('database.csv', 'r') as fileDB:
                    db_reader = csv.reader(fileDB, delimiter=',')
                    next(db_reader, None)
                    for i in db_reader:
                        if(i[6]=="0"):
                            retmsg += "\n"
                            retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                if(retmsg == "Daftar Deadline"):return False
                self.resMessage = retmsg
                return True
            else:   return "",False
        kata_kunci2 = kata_kunci2[0]
        with open('database.csv', 'r') as fileDB:
            db_reader = csv.reader(fileDB, delimiter=',')
            next(db_reader, None)
            today = datetime.datetime.now().strftime("%d/%m/%Y")
            if(kata_kunci2[0]!=""):
                for i in db_reader:
                    if(i[2] == today and kata_kunci1[0] == "deadline" and i[6]=="0"):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    elif(i[2] == today and kata_kunci1[0] == i[3] and i[6]=="0"):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    else:
                        continue
            elif(kata_kunci2[1]!=""):
                for i in db_reader:
                    if(kata_kunci1[0] == "deadline" and i[6]=="0"):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    elif(kata_kunci1[0] == i[3] and i[6]=="0"):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    else:
                        continue
            elif(kata_kunci2[2]!="" and kata_kunci2[3]!=""):
                dateawal = datetime.datetime.strptime(kata_kunci2[2], '%d/%m/%Y')
                dateakhir = datetime.datetime.strptime(kata_kunci2[3], '%d/%m/%Y')
                for i in db_reader:
                    datedb = datetime.datetime.strptime(i[2], '%d/%m/%Y')
                    if(kata_kunci1[0] == "deadline" and i[6]=="0" and dateawal <= datedb and dateakhir>= datedb):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    elif(kata_kunci1[0] == i[3] and i[6]=="0" and dateawal <= datedb and dateakhir>= datedb):
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
                    if(kata_kunci1[0] == "deadline" and i[6]=="0" and todaydate <= datedb and movedate>= datedb):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3], i[4])
                    elif(kata_kunci1[0] == i[3] and i[6]=="0" and todaydate <= datedb and movedate>= datedb):
                        retmsg += "\n"
                        retmsg += msgformat.format(i[0],i[1],i[2],i[3],i[4])
                    else:
                        continue
                    
            if(retmsg == "Daftar Deadline"):return False
            self.resMessage = retmsg
            return True
    
    def getOneTaskDeadline(self):
        #cari kata deadline
        kw1 = re.findall(r"deadline", self.reqMessage, re.IGNORECASE)
        #cari kemunculan kata tugas
        kw2 = re.findall(r"|".join(self.kata_tugas), self.reqMessage, re.IGNORECASE)
        #cari kode matakuliah
        kw3 = re.findall(r"[A-Z]{2}[0-9]{4}", self.reqMessage, re.IGNORECASE)

        if(kw1 and kw2 and kw3):
            #cari di database
            deadline = ""
            with open('database.csv', 'r', newline='') as fileDB:
                db_reader = csv.DictReader(fileDB, fieldnames = self.fieldnames)
                for row in db_reader:
                    if(row["jenis_task"].lower() == kw2[0] and row["kode_matkul"] == kw3[0]):
                        deadline = row["deadline"]

            if(deadline == ""): 
                self.resMessage = "Deadline task terkait tidak ditemukan"
            else:
                self.resMessage = deadline

def taksIscompleted(message):
    pass

def lastOccurence(string):
    loc = [-1 for i in range(128)]
    for i in range(len(string)):
        loc[ord(string[i])] = i
    return loc

def boyerMooreMatch(text, pattern):
    loc = lastOccurence(pattern)
    n = len(text)
    m = len(pattern)
    i = m - 1
    if(i > n - 1): return -1
    else:
        j = m - 1
        while(i <= n - 1): 
            if(pattern[j] == text[i]):
                if(j == 0): return i
                else: i, j = i - 1, j - 1
            else: 
                i += m - min(j, 1 + loc[ord(text[i])])
                j = m - 1
        return -1


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
    c.renewTask()
    c.getTaskRecorded()
    c.getOneTaskDeadline()
    return datetime.datetime.now(), c.resMessage, c.typoWord

if __name__ == "__main__":
    #Untuk testing
    #reqMessage = "Apa yang bisa assistant bisa lakukan"
    #reqMessage = input()
    resMessage = handleMessage("apa saja deadline")
    if(resMessage):
        print(resMessage)
    else:
        print("Maaf, pesan tidak dikenali")
