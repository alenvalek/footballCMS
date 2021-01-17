
from tkinter import *
from tkinter import ttk
import mysql.connector

from komponente.sqlConnection import *
from komponente.selekcije import *
from komponente.alertWindows import *



def dodajGolove(sesija_id):
    dodaj_gol = Tk()
    dodaj_gol.title("Dodaj gol sesiji")
    dodaj_gol.geometry("500x250")


    if not sesija_id or sesija_id == '':
        test_label3 = Label(dodaj_gol, text='Niste upisali sesiju!', bg="white")
        test_label3.grid(row=1, column=1)
        return

    cursor.execute(f"SELECT * FROM sesija WHERE id = {sesija_id}")
    rezultati = cursor.fetchone()

    label_id = Label(dodaj_gol, text=f"Dodaj golove za sesiju:  [ID:{sesija_id}]")
    label_id.grid(row=0, column=0)

    if not rezultati:
        print('TRUE')
        test_label2 = Label(dodaj_gol, text='Nema podataka za ovu sesiju!', bg="white")
        label_id.grid(row=1, column=0)
        return


    def golToDb(id_sesije, id_tim, id_igrac, vrijeme):
        cursor.execute(f"""INSERT INTO gol(id_sesija, id_tim, id_igrac, vrijeme) 
                                VALUES({id_sesije},{id_tim},{id_igrac}, STR_TO_DATE('{vrijeme}','%d/%m/%Y %H:%i'))""")
        db.commit()
        alertWindow(f"Gol uspjesno dodan u bazu podataka!")


    def getTimIDFromIgracID(id_igrac):
        cursor.execute(f'SELECT id_tim FROM igrac WHERE id = {id_igrac}')
        rezultat = cursor.fetchone()
        return rezultat[0]

    def getIDnumFromString(string):
        num = int(''.join(filter(str.isdigit, f'{string}')))
        return num

    label_igraci = Label(dodaj_gol, text="Igraci: ")
    label_igraci.grid(row=2, column=0)

    lista_igraca = Listbox(dodaj_gol, exportselection=0, width=50 )
    lista_igraca.grid(row=2, column=1)

    label_vrijeme = Label(dodaj_gol, text="Vrijeme gola(dd/mm/yyyy hh:mi):")
    label_vrijeme.grid(row=3, column=0)

    entry_vrijeme = Entry(dodaj_gol)
    entry_vrijeme.grid(row=3, column=1)


    popuniIgraceIzbor(lista_igraca, sesija_id)

    dodajGol_gumb = Button(dodaj_gol, text="Dodaj gol", command=lambda: golToDb(sesija_id, getTimIDFromIgracID(getIDnumFromString(lista_igraca.get(lista_igraca.curselection()))), getIDnumFromString(lista_igraca.get(lista_igraca.curselection())),entry_vrijeme.get()))
    dodajGol_gumb.grid(row=4, column=1, columnspan=2)

def prikaziSveGolovePoSesiji(sesija_id):

    prikaziGol = Tk()
    prikaziGol.title("Lista golova")
    prikaziGol.geometry("350x500")

    cursor.execute(f""" 

    SELECT i.id,t.ime ime_tima,CONCAT(i.ime,' ', i.prezime) as 'Igrac', g.vrijeme FROM sesija s
		JOIN tim t ON t.id = s.id_tim1
		JOIN igrac i ON i.id_tim = t.id
        JOIN gol g ON i.id = g.id_igrac
		WHERE s.id = {sesija_id}
	UNION
	SELECT i.id,t.ime ime_tima,CONCAT(i.ime,' ', i.prezime) as 'Igrac', g.vrijeme FROM sesija s
		JOIN tim t ON t.id = s.id_tim2
		JOIN igrac i ON i.id_tim = t.id
        JOIN gol g ON i.id = g.id_igrac
		WHERE s.id = {sesija_id};

""")
    rezultati = cursor.fetchall()

    for index, rezultat in enumerate(rezultati):
        test_label = Label(prikaziGol, text=f"{rezultat[1]} | {rezultat[2]} -> {rezultat[3]}", bg="white")
        test_label.pack()



def deleteGolEntry(sesija_id):

    def deleteGol():
        izbor = lista_golova.get(lista_golova.curselection())
        cursor.execute(f"DELETE FROM gol WHERE vrijeme = '{izbor}'")
        db.commit()
        alertWindow(f"Gol [TIMESTAMP:{izbor}] uspjesno izbrisan!")

    deleteGoalWin = Tk()
    deleteGoalWin.title("Brisanje golova")
    deleteGoalWin.geometry("250x250")

    cursor.execute(f"SELECT * FROM gol WHERE id_sesija = {sesija_id}")
    rezultati = cursor.fetchall()

    # generiranje liste koja cuva podatke o timovima
    lista_golova = Listbox(deleteGoalWin, exportselection=0)
    lista_golova.pack()

    # puni se selekcija za brisanje timova
    for x in rezultati:
        lista_golova.insert(END, f"{x[3]}")

    brisiGumb = Button(deleteGoalWin, text="Izbrisi gol", pady=5, command=deleteGol)
    brisiGumb.pack()