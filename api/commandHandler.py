import datetime
import csv

kata_penting = ["kuis", "ujian", "tucil", "tubes", "praktikum"]

#Method untuk menambahkan task baru
#gunakan regex
import re
def addTaskCmd(message):
    #Cari tanggal, trival ? maybe
    deadline = re.findall(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}", message)
    if(len(deadline) == 0): return "", False

    #Cari kode matakuliah
    kode_matkul = re.findall(r"[A-Z]{2}[0-9]{4}", message)
    if(len(kode_matkul) == 0): return "", False

    #Cari jenis tugas
    regex_kata_penting = r""
    for i in range(0, len(kata_penting)): 
        if(i < len(kata_penting)-1): regex_kata_penting += kata_penting[i] + "|"
        else: regex_kata_penting += kata_penting[i]

    jenis_task = re.findall(regex_kata_penting, message)

    #Cari topik tugas (asumsi: mungkin kosong)
    # kasus 1 : Halo bot, tolong ingetin kalau ada kuis IF3100 Bab 2 sampai 3 pada 22/04/2021
    topik = re.findall(r"(?<=\s[A-Z]{2}[0-9]{4}\s).*(?=\s.*[0-9]{2}\/[0-9]{2}\/[0-9]{4})", message)
    # kasus 2 : Halo bot, tolong ingetin kalau pada 22/04/2021 ada kuis IF3100 Bab 2 sampai 3
    if(len(topik) == 0): topik = re.findall(r"(?<=\s[A-Z]{2}[0-9]{4}\s).*$", message)
    
    #tambahkan task ke database
    with open('database.csv', 'r') as fileDB:
        db_reader = csv.reader(fileDB, delimiter=',')
        nRows = sum(1 for row in db_reader)

    with open('database.csv', 'a') as fileDB:
        db_writer = csv.writer(fileDB, delimiter=',')
        db_writer.writerow([nRows, datetime.datetime.now().strftime("%d/%m/%Y"), deadline[0], jenis_task[0], topik[0], 0])

    return f"[TASK BERHASIL DICATAT]\n(ID: {nRows}) - {deadline[0]} - {jenis_task[0]} - {topik[0]}", True


#Method untuk menampilkan daftar task
def getTaskRecorded(message,date):
    msg = message.lower()
    rkey = r"^(?=.*\bapa\b)"
    key1 = ""
    key1 += rkey +r"(?=.*\b({})\b).*".format("deadline") 
    for i in kata_penting:
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
            today = date.strftime("%d/%m/%Y")
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
    # querykey =  
#Method untuk menampilkan deadline (SURYA)

#Method untuk memperbaharui task

#Method untuk menandai suatu task selesai dikerjakan

#Method untuk menampilkan opsi help (SURYA)

#Method bonus (SURYA)
def checkTypo(message):
    return "", True



def handleCommand(message):
    date = datetime.datetime.now()
    suggestionMsg, statusTypo = checkTypo(message)
    
    if(statusTypo):
        msg, isAddTask = addTaskCmd(message) 
        if(isAddTask): return date, msg, []
        msg, isGetTask = getTaskRecorded(message,date)
        if(isGetTask): return date, msg, []
        print(msg)
    return date, "Maaf, pesan tidak dikenali", []



if __name__ == "__main__":
    msg, status = addTaskCmd("Halo bot, tolong ingetin kalau ada kuis IF3100 Bab 2 sampai 3 pada 22/04/2021")
    if(status):
        print(msg)