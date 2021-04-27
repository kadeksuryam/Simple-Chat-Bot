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

#Method untuk menampilkan deadline (SURYA)

#Method untuk memperbaharui task

#Method untuk menandai suatu task selesai dikerjakan

#Method untuk menampilkan opsi help (SURYA)
def helpCmd():
    # Cari kata kunci "Assistant" dan "bisa"
    k1 = re.search(r"Assistant/i")
    k2 = re.search(r"bisa/i")
    
    if(k1 and k2):
        msg = "[Fitur]\n1. Menambahkan task baru\n2. Melihat daftar task\n3. Menampilkan deadline dari suatu task tertentu\n4. Memperbaharui task tertentu\n5. Menandai suatu task telah selesai dikerjakan\n6. Menampilkan opsi help"
        msg += "\n[Daftar kata penting]\n"
        
        it_kata = 0
        for kata in kata penting:
            it_kata += 1
            msg += str(it_kata) + ". " + kata + '\n'
        
        return msg, True

    if(k1 and k2):
        return "", False

#Method bonus (SURYA)
def checkTypo(message):
    return "", False

def isAddTaskCmd(message):
    deadline = re.findall(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}", message)
    kode_matkul = re.findall(r"[A-Z]{2}[0-9]{4}", message)
    

def checkMessangeType(messange):
    # Cek apakah penambahan task
    


def handleCommand(message):
    date = datetime.datetime.now()
    suggestionMsg, isMsgTypo = checkTypo(message)
    
    if(not(isMsgTypo)):
        msg, isAddTask = addTaskCmd(message) 
        if(isAddTask): return date, msg, []
        
    return date, "Maaf, pesan tidak dikenali", []


if __name__ == "__main__":
    userMsg = "Halo bot, tolong ingetin kalau ada kuis IF3100 Bab 2 sampai 3 pada 22/04/2021"
    msg, status = addTaskCmd(userMsg)
    if(status): print(msg)
    else:
        if