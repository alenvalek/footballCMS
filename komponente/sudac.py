
from tkinter import *
from tkinter import ttk
import mysql.connector

from komponente.sqlConnection import *
from komponente.selekcije import *
from komponente.alertWindows import *


#dohvaca sve sudce i ispisuje ih na zaseban prozor
def pokaziSudce():
    prikaziSudce = Tk()
    prikaziSudce.title("Lista sudaca")
    prikaziSudce.geometry("250x500")

    cursor.execute("SELECT * FROM sudac")
    rezultati = cursor.fetchall()

    for index,rezultat in enumerate(rezultati):

        test_label = Label(prikaziSudce, text=f"{rezultat[0]}. {rezultat[1]} | {rezultat[2]} | {rezultat[3]} | {rezultat[4]} | {rezultat[5]}", bg="white")
        test_label.pack()


# dodaje sudca koji puni korisnik sucelja custom podacima
def dodajSudca():

    def sudacToDb(ime, prezime, datum_rodenja, drzava, grad):
        cursor.execute(f"""INSERT INTO sudac(ime,prezime,datum_rodenja,id_drzava, id_grad) 
                                VALUES("{ime}","{prezime}",str_to_date('{datum_rodenja}','%d/%m/%Y'),{drzava}, {grad})""")
        db.commit()
        clear()

    def clear():
        entry_ime.delete(0, END)
        entry_prezime.delete(0, END)
        entry_dr.delete(0,END)
        lista_gradova.selection_clear(0, END)
        lista_drzava.selection_clear(0, END)

    dodajSudac = Tk()
    dodajSudac.title("Dodaj sudca")
    dodajSudac.geometry("250x500")

    label_ime = Label(dodajSudac, text="Ime")
    label_ime.grid(row=0, column=0)

    label_prezime = Label(dodajSudac, text="Prezime")
    label_prezime.grid(row=1, column=0)

    label_dr = Label(dodajSudac, text="Datum_rodenja\n(dd/mm/yyyy)")
    label_dr.grid(row=2, column=0)

    label_drzava = Label(dodajSudac, text="Drzava")
    label_drzava.grid(row=3, column=0)

    label_grad = Label(dodajSudac, text="Grad")
    label_grad.grid(row=4, column=0)


    entry_ime = Entry(dodajSudac)
    entry_ime.grid(row= 0, column=1)

    entry_prezime = Entry(dodajSudac)
    entry_prezime.grid(row=1, column=1)

    entry_dr = Entry(dodajSudac)
    entry_dr.grid(row=2, column=1)

    lista_drzava = Listbox(dodajSudac, exportselection=0)
    lista_drzava.grid(row=3, column=1)

    lista_gradova = Listbox(dodajSudac, exportselection=0)
    lista_gradova.grid(row=4, column=1)

    popuniDrzaveIzbor(lista_drzava)
    popuniGradIzbor(lista_gradova)

    dodajSudca_gumb = Button(dodajSudac, text="Dodaj", command=lambda:sudacToDb(entry_ime.get(),entry_prezime.get(), entry_dr.get(), lista_drzava.curselection()[0]+1, lista_gradova.curselection()[0]+1))
    dodajSudca_gumb.grid(row=5, column=1, columnspan=2)


# brise sudca iz baze
def deleteSudacEntry():

    def deleteSudac():
        izbor = lista_sudaca.get(lista_sudaca.curselection())
        cursor.execute(f"DELETE FROM sudac WHERE ime = '{izbor}'")
        db.commit()
        alertWindow(f"Sudac {izbor} uspjesno izbrisan!")

    deleteSudacWin = Tk()
    deleteSudacWin.title("Brisanje Sudaca")
    deleteSudacWin.geometry("250x250")

    cursor.execute("SELECT * FROM sudac")
    rezultati = cursor.fetchall()

    # generiranje liste koja cuva podatke o sudcima
    lista_sudaca = Listbox(deleteSudacWin, exportselection=0)
    lista_sudaca.pack()

    # puni se selekcija za brisanje sudaca
    for x in rezultati:
        lista_sudaca.insert(END, f"{x[1]}")

    brisiGumb = Button(deleteSudacWin, text="Izbrisi", pady=5, command=deleteSudac)
    brisiGumb.pack()