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


def handleMessage(message):
    c = CommandHandler(message)
    c.addTaskCmd()
    c.helpCmd()

    return c.resMessage

if __name__ == "__main__":
    #Untuk testing
    reqMessage = "Apa yang bisa assistant bisa lakukan"
    resMessage = handleMessage(reqMessage)
    if(resMessage):
        print(resMessage)
    else:
        print("Maaf, pesan tidak dikenali")

