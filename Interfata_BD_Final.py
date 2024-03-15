from tkinter import *
import pyodbc
from datetime import datetime
import pandas as pd


server = 'DESKTOP-AJD5D57\SQLEXPRESS'
database = 'DealerAuto_StoianMihai331AB'
port = '12.0.2269'
try:
    conexiune = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    print("Conectat cu succes la baza de date")
except pyodbc.Error as e:
    print("Eroare la conectare:", e)

def format_output(rezultat,cursor):
    def format_element(element):
                if isinstance(element, datetime):
                     return element.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    return str(element)
                
    # + intre atribute | intre entitati
    string_rezultat_raw = ['+'.join(format_element(element) for element in row) for row in rezultat]
    string_rezultat = '|'.join(string_rezultat_raw)

    rows = string_rezultat.strip().split('|')
    matrix = [row.split('+') for row in rows]
    df = pd.DataFrame(matrix)
        
    # obtinem header-urile
    column_headers = [column[0] for column in cursor.description]
    return df,column_headers

# Top 3 salarii din departamentul ...
def task_1():
    def task_1_interogare():
        conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
        cursor = conn.cursor()
        
        departament = insert_task_1_depart.get()
        sql_query = """
        SELECT TOP 3 Angajati.Nume, Angajati.Prenume,Angajati.Salariu 
        FROM Angajati
        JOIN Departamente ON Angajati.Departament_ID = Departamente.Departament_ID
        WHERE Departamente.Denumire_departament = ?
        ORDER BY Angajati.Salariu DESC;
        """
        cursor.execute(sql_query,departament)

        rezultat = cursor.fetchall()
    
        [df,column_headers] = format_output(rezultat,cursor)
    
        # retinem data si ora curenta
        current_datetime = datetime.now()
        
        # formatam data cum dorim
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        # concatenam data si ora la numele taskului indeplinit
        file_name = "task_1_{}.xlsx".format(formatted_datetime)

        # salvam dataframeul in documentul excel cu numele corespunzator
        df.to_excel(file_name, index=False, header=column_headers)
    
        # afisam un mesaj care sa ne indice ca a fost realizat task-ul
        print("Task_1 executat cu succes !")

    interface_t1=Tk()
    interface_t1.title('Task_1')
    interface_t1.geometry('375x100')

    insert_task_1_depart= Entry(interface_t1,width=30)
    insert_task_1_depart.grid(row=0,column=1,padx=20)

    insert_task_1_dept_label = Label(interface_t1, text="Departament")
    insert_task_1_dept_label.grid(row=0,column=0)

    run_task_1_bt = Button(interface_t1, text = "Run Task 1", command=task_1_interogare)
    run_task_1_bt.grid(row=1,column=1,columnspan=1)

# numele, prenumele, salariu si procentul salariului fata de managerul departamentului, pt toti angajatii
def task_2():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()
    
    sql_query = """
    SELECT Angajati.Nume, Angajati.Prenume, Angajati.Salariu,(Angajati.Salariu / Manageri.Salariu) * 100 AS Procent_Salariu,Departamente.Denumire_Departament
    FROM Angajati
    JOIN Departamente ON Angajati.Departament_ID = Departamente.Departament_ID
    LEFT JOIN Angajati AS Manageri ON Departamente.Manager_ID = Manageri.Angajat_ID
    """

    cursor.execute(sql_query)

    rezultat = cursor.fetchall()
   
    [df,column_headers] = format_output(rezultat,cursor)

    current_datetime = datetime.now()

    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    file_name = "task_2_{}.xlsx".format(formatted_datetime)

    df.to_excel(file_name, index=False, header=column_headers)
   
    print("Task_2 executat cu succes !")

# departamentele si nr de ang din fiecare departament
def task_3():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()

    sql_query = """
    SELECT Departamente.Denumire_departament AS Departament, COUNT(Angajati.Angajat_ID) AS Numar_Angajati
    FROM Departamente
    LEFT JOIN Angajati ON Departamente.Departament_ID = Angajati.Departament_ID
    GROUP BY Departamente.Denumire_departament;
    """

    cursor.execute(sql_query)

    rezultat = cursor.fetchall()
   
    [df,column_headers] = format_output(rezultat,cursor)

    current_datetime = datetime.now()

    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    file_name = "task_3_{}.xlsx".format(formatted_datetime)

    df.to_excel(file_name, index=False, header=column_headers)
   
    print("Task_3 executat cu succes !")

# detalii despre toți clienții și tranzactiile pe care le au efectuat(model+stare masina, suma+tip tranzactie)
def task_4():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()

    sql_query = """
    SELECT C.Nume, C.Prenume,M.Marca, M.Stare,T.Data_tranzactie, T.Suma_platita, T.Metoda_Plata
    FROM Clienti C
    JOIN Tranzactii T ON C.Customer_ID = T.Customer_ID
    JOIN Masina M ON T.Masina_ID = M.Masina_ID;
    """
    
    cursor.execute(sql_query)

   
    rezultat = cursor.fetchall()
   
    [df,column_headers] = format_output(rezultat,cursor)
   
    current_datetime = datetime.now()

    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    file_name = "task_4_{}.xlsx".format(formatted_datetime)

    df.to_excel(file_name, index=False, header=column_headers)
   
    print("Task_4 executat cu succes !")

# totalul tranzactiilor realizate de fiecare angajat
def task_5():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()

    sql_query = """
    SELECT A.Nume, A.Prenume, SUM(T.Suma_platita) AS Total_vanzari
    FROM Angajati A
    JOIN Tranzactii T ON A.Angajat_ID = T.Angajat_ID
    GROUP BY A.Nume, A.Prenume;
    """
    # Execute the query
    cursor.execute(sql_query)

    # Fetch the results
    rezultat = cursor.fetchall()
   
    [df,column_headers] = format_output(rezultat,cursor)
    # exportam datele in excell
     # Get current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Concatenate the formatted date and time to the file name
    file_name = "task_5_{}.xlsx".format(formatted_datetime)

    # Save DataFrame to Excel with the concatenated file name
    df.to_excel(file_name, index=False, header=column_headers)
   
    print("Task_5 executat cu succes !")

# angajatii care au realizat tranzactii pe masini neavariate + detalii despre masina si tranzactie
def task_6():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()

    sql_query = """
    SELECT T.Tip_tranzactie, M.Marca, M.An_fabricatie, A.Nume, A.Prenume
    FROM Masina M
    JOIN Tranzactii T ON M.Masina_ID = T.Masina_ID
    JOIN Angajati A ON T.Angajat_ID = A.Angajat_ID
    WHERE M.Stare = 'Neavariata';
    """
    # Execute the query
    cursor.execute(sql_query)

    # Fetch the results
    rezultat = cursor.fetchall()
   
    [df,column_headers] = format_output(rezultat,cursor)
    # exportam datele in excell
     # Get current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Concatenate the formatted date and time to the file name
    file_name = "task_6_{}.xlsx".format(formatted_datetime)

    # Save DataFrame to Excel with the concatenated file name
    df.to_excel(file_name, index=False, header=column_headers)
   
    print("Task_6 executat cu succes !")
     
# numele si prenumele angajatilor de la dept vanzari, care nu au procesat nicio tranzactie
def task_7():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()

    sql_query = """
    SELECT A.Nume, A.Prenume
    FROM Angajati A
    WHERE A.Angajat_ID NOT IN (
    SELECT DISTINCT Angajat_ID
    FROM Tranzactii
    )
    AND A.Departament_ID = (
    SELECT Departament_ID
    FROM Departamente
    WHERE Denumire_departament = 'Vanzari'
    );
    """
    # Execute the query
    cursor.execute(sql_query)

    # Fetch the results
    rezultat = cursor.fetchall()
   
    [df,column_headers] = format_output(rezultat,cursor)
    # Get current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Concatenate the formatted date and time to the file name
    file_name = "task_1_{}.xlsx".format(formatted_datetime)

    # Save DataFrame to Excel with the concatenated file name
    df.to_excel(file_name, index=False, header=column_headers)
   
    print("Task_7 executat cu succes !")

# clienti care au facut rezervari supra mai multor masini 
def task_8():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()

    sql_query = """
    SELECT CONCAT(C.Nume,' ',C.Prenume) AS Nume_client
    FROM Clienti C
    WHERE C.Customer_ID IN (
    SELECT Customer_ID
    FROM Tranzactii
    WHERE Tip_tranzactie = 'Rezervare'
    GROUP BY Customer_ID
    HAVING COUNT(DISTINCT Masina_ID) > 1
);
    """
    # Execute the query
    cursor.execute(sql_query)

    # Fetch the results
    rezultat = cursor.fetchall()
   
    [df,column_headers] = format_output(rezultat,cursor)
    # exportam datele in excell
     # Get current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Concatenate the formatted date and time to the file name
    file_name = "task_8_{}.xlsx".format(formatted_datetime)

    # Save DataFrame to Excel with the concatenated file name
    df.to_excel(file_name, index=False, header=column_headers)
   
    print("Task_8 executat cu succes !")

# ultima tranzactie de tip ... realizata de fiecare client
def task_9():
        def task_9_interogare():
            conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
            cursor = conn.cursor()
            tip_tranz = insert_task_9_tip_vanz.get()
            sql_query = """
            SELECT C.Nume, C.Prenume, M.Marca, M.An_fabricatie, T.Data_tranzactie AS Data_vanzare
            FROM
                Clienti C
                JOIN Tranzactii T ON C.Customer_ID = T.Customer_ID
                JOIN Masina M ON T.Masina_ID = M.Masina_ID
            WHERE
                T.Tip_tranzactie = ?
                AND T.Data_tranzactie = (
                    SELECT MAX(Data_tranzactie)
                    FROM Tranzactii
                    WHERE Customer_ID = C.Customer_ID AND Tip_tranzactie = 'Vanzare'
                );
            """
            # Execute the query
            cursor.execute(sql_query,tip_tranz)

            # Fetch the results
            rezultat = cursor.fetchall()
        
            [df,column_headers] = format_output(rezultat,cursor)
            # exportam datele in excell
            # Get current date and time
            current_datetime = datetime.now()

            # Format the date and time as a string
            formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

            # Concatenate the formatted date and time to the file name
            file_name = "task_9_{}.xlsx".format(formatted_datetime)

            # Save DataFrame to Excel with the concatenated file name
            df.to_excel(file_name, index=False, header=column_headers)
        
            print("Task_9 executat cu succes !")
        interface_t9=Tk()
        interface_t9.title('Task_9')
        interface_t9.geometry('375x100')

        insert_task_9_tip_vanz= Entry(interface_t9,width=30)
        insert_task_9_tip_vanz.grid(row=0,column=1,padx=20)

        insert_task_9_tip_vanz_l = Label(interface_t9, text="Tip tranzactie:")
        insert_task_9_tip_vanz_l.grid(row=0,column=0)

        run_task_9_bt = Button(interface_t9, text = "Run Task 9", command=task_9_interogare)
        run_task_9_bt.grid(row=1,column=1,columnspan=1)
# dealer-urile de masini care au numarul maxim de dacii dupa anul 2005
def task_10():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()

    sql_query = """
    SELECT Dealer_ID, Nume_Dealer
    FROM Dealer
    WHERE Dealer_ID IN (
        SELECT Dealer_ID
        FROM Masina
        WHERE An_Fabricatie > 2005 AND Marca = 'Dacia'
        GROUP BY Dealer_ID
        HAVING COUNT(*) = (
            SELECT TOP 1 COUNT(*)
            FROM Masina
            WHERE An_Fabricatie > 2005 AND Marca = 'Dacia'
            GROUP BY Dealer_ID
            ORDER BY COUNT(*) DESC
        )
    );
    """

    cursor.execute(sql_query)

    rezultat = cursor.fetchall()
   
    [df,column_headers] = format_output(rezultat,cursor)

    current_datetime = datetime.now()

    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    file_name = "task_10_{}.xlsx".format(formatted_datetime)

    df.to_excel(file_name, index=False, header=column_headers)
   
    print("Task_10 executat cu succes !")

def quit_application():
    interface.destroy()
    instructiuni.destroy()
    
####### insert/update/delete ##########
def insert_masini():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()
    
    
    cursor.execute("INSERT INTO Masina(Masina_ID,Dealer_ID,Marca,An_fabricatie,Pret,Kilometraj, Combustibil, Transmisie, Culoare, Stare, Descriere_Service) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                   (
                       insert_id_masina.get(),
                       insert_id_dealer.get(),
                       insert_model.get(),
                       insert_an_fab.get(),
                       insert_pret.get(),
                       insert_kilometraj.get(),
                       insert_combustibil.get(),
                       insert_transmisie.get(),
                       insert_culoare.get(),
                       insert_stare.get(),
                       insert_descriere_service.get(),


                   )
                  )
    conn.commit()
    conn.close()
    

    insert_id_masina.delete(0, END)
    insert_id_dealer.delete(0, END)
    insert_model.delete(0, END)
    insert_an_fab.delete(0, END)
    insert_pret.delete(0, END)
    insert_kilometraj.delete(0, END)
    insert_combustibil.delete(0, END)
    insert_transmisie.delete(0, END)
    insert_culoare.delete(0, END)
    insert_stare.delete(0, END)
    insert_descriere_service.delete(0, END)

def update_masini():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Masina SET Dealer_ID=?,Marca=?, An_fabricatie=?, Pret=?, Kilometraj=?, Combustibil=?, Transmisie=?, Culoare=?, Stare=?, Descriere_Service=? WHERE Masina_ID=?",
                   (
                       update_id_dealer.get(),
                       update_model.get(),
                       update_an_fab.get(),
                       update_pret.get(),
                       update_kilometraj.get(),
                       update_combustibil.get(),
                       update_transmisie.get(),
                       update_culoare.get(),
                       update_stare.get(),
                       update_descriere_service.get(),
                       update_id_masina.get(),
                   )
                  )
    conn.commit()
    conn.close()

    update_id_masina.delete(0, END)
    update_id_dealer.delete(0, END)
    update_model.delete(0, END)
    update_an_fab.delete(0, END)
    update_pret.delete(0, END)
    update_kilometraj.delete(0, END)
    update_combustibil.delete(0, END)
    update_transmisie.delete(0, END)
    update_culoare.delete(0, END)
    update_stare.delete(0, END)
    update_descriere_service.delete(0, END)

def delete_masina():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Masina WHERE Masina_ID=?",
                   (
                       delete_id_masina.get()
                   )
                  )
    conn.commit()
    conn.close()

    delete_id_masina.delete(0, END)

def insert_angajati():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Angajati(Angajat_ID,Dealer_ID,Departament_ID,Nume,Prenume,Adresa,Numar_telefon,Pozitie, Salariu, Data_Angajarii) VALUES (?,?,?,?,?,?,?,?,?,?)",
                   (
                       insert_id_angajat_ang.get(),
                       insert_id_dealer_ang.get(),
                       insert_id_depart_ang.get(),
                       insert_nume_ang.get(),
                       insert_prenume_ang.get(),
                       insert_adresa_ang.get(),
                       insert_numar_ang.get(),
                       insert_poz_ang.get(),
                       insert_salariu_ang.get(),
                       insert_data_ang_ang.get(),
                   )
                  )
    conn.commit()
    conn.close()
    
    insert_id_angajat_ang.delete(0, END)
    insert_id_dealer_ang.delete(0, END)
    insert_id_depart_ang.delete(0, END)
    insert_nume_ang.delete(0, END)
    insert_prenume_ang.delete(0, END)
    insert_adresa_ang.delete(0, END)
    insert_numar_ang.delete(0, END)
    insert_poz_ang.delete(0, END)
    insert_salariu_ang.delete(0, END)
    insert_data_ang_ang.delete(0, END)

def update_angajati():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()

    cursor.execute("UPDATE Angajati SET Dealer_ID=?, Departament_ID=?, Nume=?, Prenume=?, Adresa=?, Numar_telefon=?, Pozitie=?, Salariu=?, Data_angajarii=CONVERT(datetime, ?, 120) WHERE Angajat_ID=?",
                   (
                       update_id_dealer_ang.get(),
                       update_id_depart_ang.get(),
                       update_nume_ang.get(),
                       update_prenume_ang.get(),
                       update_adresa_ang.get(),
                       update_numar_ang.get(),
                       update_poz_ang.get(),
                       update_salariu_ang.get(),
                       update_data_ang_ang.get(),
                       update_id_angajat_ang.get(),
                   )
                  )
    
   
    conn.commit()
    conn.close()
    
    update_id_angajat_ang.delete(0, END)
    update_id_dealer_ang.delete(0, END)
    update_id_depart_ang.delete(0, END)
    update_nume_ang.delete(0, END)
    update_prenume_ang.delete(0, END)
    update_adresa_ang.delete(0, END)
    update_numar_ang.delete(0, END)
    update_poz_ang.delete(0, END)
    update_salariu_ang.delete(0, END)
    update_data_ang_ang.delete(0, END)

def delete_angajati():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port}')
    cursor = conn.cursor()
    
    # Comanda SQL, ? este valoarea pe care o ia din widgetul de entry din delete_id_angajat.
    cursor.execute("DELETE FROM Angajati WHERE Angajat_ID=?",
                   (
                       delete_id_angajat.get()
                   )
                  )
    conn.commit()
    conn.close()

    # Ștergerea datelor din widget-urile Entry după ștergerea în baza de date
    delete_id_angajat.delete(0, END)

interface=Tk()
interface.title('Interfata Manipulare Baza de date')
interface.geometry('1500x1200')

instructiuni=Tk()
instructiuni.title("Instructiuni Task-uri")
instructiuni.geometry('950x700')

########## MASINA ##########
#region insert
insert_id_masina= Entry(interface,width=30)
insert_id_masina.grid(row=2,column=1,padx=20)
insert_id_dealer = Entry(interface,width=30)
insert_id_dealer.grid(row=3,column = 1,padx=20)
insert_model = Entry(interface,width=30)
insert_model.grid(row=4,column=1,padx=20)
insert_an_fab = Entry(interface,width=30)
insert_an_fab.grid(row=5,column=1,padx=20)
insert_pret = Entry(interface,width=30)
insert_pret.grid(row=6,column=1,padx=20)
insert_kilometraj = Entry(interface,width=30)
insert_kilometraj.grid(row=7,column=1,padx=20)
insert_combustibil = Entry(interface,width=30)
insert_combustibil.grid(row=8,column=1,padx=20)
insert_transmisie = Entry(interface,width=30)
insert_transmisie.grid(row=9,column=1,padx=20)
insert_culoare = Entry(interface,width=30)
insert_culoare.grid(row=10,column=1,padx=20)
insert_stare = Entry(interface,width=30)
insert_stare.grid(row=11,column=1,padx=20)
insert_descriere_service = Entry(interface,width=30)
insert_descriere_service.grid(row=12,column=1,padx=20)

insert_masina_m_id_lab = Label(interface, text="ID Masina")
insert_masina_m_id_lab.grid(row=2,column=0)
insert_masina_d_id_lab = Label(interface, text="ID Dealer")
insert_masina_d_id_lab.grid(row=3,column=0)
insert_masina_model_lab = Label(interface, text="Marca")
insert_masina_model_lab.grid(row=4,column=0)
insert_masina_an_fab_lab = Label(interface, text="An fabricatie")
insert_masina_an_fab_lab.grid(row=5,column=0)
insert_masina_pret_lab = Label(interface, text="Pret")
insert_masina_pret_lab.grid(row=6,column=0)
insert_masina_kilom_lab = Label(interface, text="Kilometraj")
insert_masina_kilom_lab.grid(row=7,column=0)
insert_masina_comb_lab = Label(interface, text="Combustibil")
insert_masina_comb_lab.grid(row=8,column=0)
insert_masina_transmisie_lab = Label(interface, text="Transmisie")
insert_masina_transmisie_lab.grid(row=9,column=0)
insert_masina_culoare_lab = Label(interface, text="Culoare")
insert_masina_culoare_lab.grid(row=10,column=0)
insert_masina_stare_lab = Label(interface, text="Stare")
insert_masina_stare_lab.grid(row=11,column=0)
insert_masina_descriere_lab = Label(interface, text="Descriere Service")
insert_masina_descriere_lab.grid(row=12,column=0)

submit_insert_car = Button(interface, text = "Introduceti masina", command=insert_masini)
submit_insert_car.grid(row=13,column=0,columnspan=2,pady=10,padx=10,ipadx=100)
#endregion

#region update
update_id_masina = Entry(interface, width=30)
update_id_masina.grid(row=2, column=11, padx=20)
update_id_dealer = Entry(interface, width=30)
update_id_dealer.grid(row=3, column=11, padx=20)
update_model = Entry(interface, width=30)
update_model.grid(row=4, column=11, padx=20)
update_an_fab = Entry(interface, width=30)
update_an_fab.grid(row=5, column=11, padx=20)
update_pret = Entry(interface, width=30)
update_pret.grid(row=6, column=11, padx=20)
update_kilometraj = Entry(interface, width=30)
update_kilometraj.grid(row=7, column=11, padx=20)
update_combustibil = Entry(interface, width=30)
update_combustibil.grid(row=8, column=11, padx=20)
update_transmisie = Entry(interface, width=30)
update_transmisie.grid(row=9, column=11, padx=20)
update_culoare = Entry(interface, width=30)
update_culoare.grid(row=10, column=11, padx=20)
update_stare = Entry(interface, width=30)
update_stare.grid(row=11, column=11, padx=20)
update_descriere_service = Entry(interface, width=30)
update_descriere_service.grid(row=12, column=11, padx=20)

update_id_masina_lab = Label(interface, text="ID Masina")
update_id_masina_lab.grid(row=2, column=10)
update_id_dealer_lab = Label(interface, text="ID Dealer")
update_id_dealer_lab.grid(row=3, column=10)
update_model_lab = Label(interface, text="Marca")
update_model_lab.grid(row=4, column=10)
update_an_fab_lab = Label(interface, text="An fabricatie")
update_an_fab_lab.grid(row=5, column=10)
update_pret_lab = Label(interface, text="Pret")
update_pret_lab.grid(row=6, column=10)
update_kilometraj_lab = Label(interface, text="Kilometraj")
update_kilometraj_lab.grid(row=7, column=10)
update_combustibil_lab = Label(interface, text="Combustibil")
update_combustibil_lab.grid(row=8, column=10)
update_transmisie_lab = Label(interface, text="Transmisie")
update_transmisie_lab.grid(row=9, column=10)
update_culoare_lab = Label(interface, text="Culoare")
update_culoare_lab.grid(row=10, column=10)
update_stare_lab = Label(interface, text="Stare")
update_stare_lab.grid(row=11, column=10)
update_descriere_service_lab = Label(interface, text="Descriere Service")
update_descriere_service_lab.grid(row=12, column=10)

submit_update_car = Button(interface, text="Update masina", command=update_masini)
submit_update_car.grid(row=13, column=10, columnspan=2, pady=10, padx=10, ipadx=100)
#endregion

#region delete
delete_id_masina_lab = Label(interface, text="ID Masina")
delete_id_masina_lab.grid(row=9, column=17)

delete_id_masina = Entry(interface, width=30)
delete_id_masina.grid(row=9, column=18, padx=20)

submit_delete_car = Button(interface, text="Stergeti masina", command=delete_masina)
submit_delete_car.grid(row=13, column=18, columnspan=1, pady=10, padx=10, ipadx=100)
#endregion
########## STOP MASINA ##########

label = Label(interface)
label.grid(row=15,column=1,columnspan=30,pady = 50)


########## START ANGAJATI ##########
#region insert
insert_id_angajat_ang= Entry(interface,width=30)
insert_id_angajat_ang.grid(row=16,column=1,padx=20)
insert_id_dealer_ang = Entry(interface,width=30)
insert_id_dealer_ang.grid(row=17,column = 1,padx=20)
insert_id_depart_ang = Entry(interface,width=30)
insert_id_depart_ang.grid(row=18,column=1,padx=20)
insert_nume_ang = Entry(interface,width=30)
insert_nume_ang.grid(row=19,column=1,padx=20)
insert_prenume_ang = Entry(interface,width=30)
insert_prenume_ang.grid(row=20,column=1,padx=20)
insert_adresa_ang = Entry(interface,width=30)
insert_adresa_ang.grid(row=21,column=1,padx=20)
insert_numar_ang = Entry(interface,width=30)
insert_numar_ang.grid(row=22,column=1,padx=20)
insert_poz_ang = Entry(interface,width=30)
insert_poz_ang.grid(row=23,column=1,padx=20)
insert_salariu_ang = Entry(interface,width=30)
insert_salariu_ang.grid(row=24,column=1,padx=20)
insert_data_ang_ang = Entry(interface,width=30)
insert_data_ang_ang.grid(row=25,column=1,padx=20)



insert_id_angajat_ang_lab = Label(interface, text="ID Angajat")
insert_id_angajat_ang_lab.grid(row=16,column=0)
insert_id_dealer_ang_lab = Label(interface, text="ID Dealer")
insert_id_dealer_ang_lab.grid(row=17,column=0)
insert_id_depart_ang_lab = Label(interface, text="ID Departament")
insert_id_depart_ang_lab.grid(row=18,column=0)
insert_nume_ang_lab = Label(interface, text="Nume")
insert_nume_ang_lab.grid(row=19,column=0)
insert_prenume_ang_lab = Label(interface, text="Prenume")
insert_prenume_ang_lab.grid(row=20,column=0)
insert_adresa_ang_lab = Label(interface, text="Adresa")
insert_adresa_ang_lab.grid(row=21,column=0)
insert_numar_ang_lab = Label(interface, text="Nr Telefon")
insert_numar_ang_lab.grid(row=22,column=0)
insert_poz_ang_lab = Label(interface, text="Pozitie")
insert_poz_ang_lab.grid(row=23,column=0)
insert_salariu_ang_lab = Label(interface, text="Salariu")
insert_salariu_ang_lab.grid(row=24,column=0)
insert_data_ang_lab = Label(interface, text="Data Angajarii")
insert_data_ang_lab.grid(row=25,column=0)

submit_insert_car = Button(interface, text = "Introduceti angajat", command=insert_angajati)
submit_insert_car.grid(row=26,column=0,columnspan=2,pady=10,padx=10,ipadx=100)
#endregion

#region update
update_id_angajat_ang = Entry(interface,width=30)
update_id_angajat_ang.grid(row=16,column=11,padx=20)
update_id_dealer_ang = Entry(interface,width=30)
update_id_dealer_ang.grid(row=17,column = 11,padx=20)
update_id_depart_ang = Entry(interface,width=30)
update_id_depart_ang.grid(row=18,column=11,padx=20)
update_nume_ang = Entry(interface,width=30)
update_nume_ang.grid(row=19,column=11,padx=20)
update_prenume_ang = Entry(interface,width=30)
update_prenume_ang.grid(row=20,column=11,padx=20)
update_adresa_ang = Entry(interface,width=30)
update_adresa_ang.grid(row=21,column=11,padx=20)
update_numar_ang = Entry(interface,width=30)
update_numar_ang.grid(row=22,column=11,padx=20)
update_poz_ang = Entry(interface,width=30)
update_poz_ang.grid(row=23,column=11,padx=20)
update_salariu_ang = Entry(interface,width=30)
update_salariu_ang.grid(row=24,column=11,padx=20)
update_data_ang_ang = Entry(interface,width=30)
update_data_ang_ang.grid(row=25,column=11,padx=20)



update_id_angajat_ang_lab = Label(interface, text="ID Angajat")
update_id_angajat_ang_lab.grid(row=16,column=10)
update_id_dealer_ang_lab = Label(interface, text="ID Dealer")
update_id_dealer_ang_lab.grid(row=17,column=10)
update_id_depart_ang_lab = Label(interface, text="ID Departament")
update_id_depart_ang_lab.grid(row=18,column=10)
update_nume_ang_lab = Label(interface, text="Nume")
update_nume_ang_lab.grid(row=19,column=10)
update_prenume_ang_lab = Label(interface, text="Prenume")
update_prenume_ang_lab.grid(row=20,column=10)
update_adresa_ang_lab = Label(interface, text="Adresa")
update_adresa_ang_lab.grid(row=21,column=10)
update_numar_ang_lab = Label(interface, text="Nr Telefon")
update_numar_ang_lab.grid(row=22,column=10)
update_poz_ang_lab = Label(interface, text="Pozitie")
update_poz_ang_lab.grid(row=23,column=10)
update_salariu_ang_lab = Label(interface, text="Salariu")
update_salariu_ang_lab.grid(row=24,column=10)
update_data_ang_lab = Label(interface, text="Data Angajarii")
update_data_ang_lab.grid(row=25,column=10)

submit_update_ang = Button(interface, text = "Actualizati angajat", command=update_angajati)
submit_update_ang.grid(row=26,column=10,columnspan=2,pady=10,padx=10,ipadx=100)
#endregion

#region delete
delete_id_ang_lab = Label(interface, text="ID Angajat")
delete_id_ang_lab.grid(row=22, column=17)

delete_id_angajat = Entry(interface, width=30)
delete_id_angajat.grid(row=22, column=18, padx=20)

submit_delete_ang = Button(interface, text="Stergeti angajat", command=delete_angajati)
submit_delete_ang.grid(row=26, column=18, columnspan=1, pady=10, padx=50, ipadx=100)
#endregion
########## STOP ANGAJATI ##########

label_titlu = Label(interface,text="Baza de date AutoSH",font="Helvetica")
label_titlu.grid(row=0,column=1,columnspan=1)
label_2 = Label(interface)
label_2.grid(row=27,column=0,columnspan=30,pady = 10)

#region interogari simple
task1_b = Button(interface, text = "** Task 1**", command = task_1)
task1_b.grid(row=0,column=19,columnspan=1,pady=10,padx=15)

task2_b = Button(interface, text = "Task 2", command=task_2)
task2_b.grid(row=0,column=20,columnspan=1,pady=10,padx=15)

task3_b = Button(interface, text = "Task 3", command=task_3)
task3_b.grid(row=0,column=21,columnspan=1,pady=10,padx=15)

task4_b = Button(interface, text = "Task 4", command=task_4)
task4_b.grid(row=0,column=22,columnspan=1,pady=10,padx=15)

task5_b = Button(interface, text = "Task 5", command=task_5)
task5_b.grid(row=0,column=23,columnspan=1,pady=10,padx=15)

task6_b = Button(interface, text = "Task 6", command=task_6)
task6_b.grid(row=1,column=19,columnspan=1,pady=10,padx=15)

#endregion

#region interogari complexe
task7_b = Button(interface, text = "Task 7", command=task_7)
task7_b.grid(row=1,column=20,columnspan=1,pady=10)

task8_b = Button(interface, text = "Task 8", command=task_8)
task8_b.grid(row=1,column=21,columnspan=1,pady=10)

task9_b = Button(interface, text = "** Task 9 **", command=task_9)
task9_b.grid(row=1,column=22,columnspan=1,pady=10)

task10_b = Button(interface, text = "Task 10", command=task_10)
task10_b.grid(row=1,column=23,columnspan=1,pady=10)
#endregion

#region instructiuni
label_titlu = Label(instructiuni,text="Indicatii : ",font='Helvetica')

label_task_1 = Label(instructiuni, text = '''
1)	Sa se gaseasca cele mai mari 3 salarii ale angajatilor ce lucreaza pentru departamentul introdus de dvs in fereastra care se va deschide cand apasati pe buton
''')
label_task_2 = Label(instructiuni, text = '''
2)	Afisati numele, prenumele si salariul pentru toti angajatii, precum si procentul salariului acestora fata de managerul departamentului.
''')
label_task_3 = Label(instructiuni, text = '''
3)	Afișează departamentele și numărul de angajați din fiecare departament.
''')
label_task_4 = Label(instructiuni, text = '''
4)	Afișează detalii despre toți clienții și tranzactiile pe care le au efectuat (model si stare masina, suma, tip tranzactie )
''')
label_task_5 = Label(instructiuni, text = '''
5)	Afișează totalul tranzactiilor realizate de fiecare angajat
''')
label_task_6 = Label(instructiuni, text = '''
6)	Angajatii care au realizat tranzactii cu masini neavariate + detalii despre masina
''')
label_task_7 = Label(instructiuni, text = '''
7)	Afișează numele și prenumele angajaților care nu au procesat nicio tranzacție.
''')
label_task_8 = Label(instructiuni, text = '''
8)	Clienti care au facut mai multe rezervari, pentru masini diferite
''')
label_task_9 = Label(instructiuni, text = '''
9)	Ultima tranzactie de tipul selectat de dvs in fereastra care se va deschide,pentru fiecare client
''')
label_task_10 = Label(instructiuni, text = '''
10)	Dealer-urile care au numarul maxim de masini cu modelul Dacia mai noi de 2005
''')

label_titlu.grid(row=0,column = 1,columnspan=1,pady=20)
label_task_1.grid(row=1,column = 1,columnspan=1,sticky=W)
label_task_2.grid(row=2,column = 1,columnspan=1,sticky=W)
label_task_3.grid(row=3,column = 1,columnspan=1,sticky=W)
label_task_4.grid(row=4,column = 1,columnspan=1,sticky=W)
label_task_5.grid(row=5,column = 1,columnspan=1,sticky=W)
label_task_6.grid(row=6,column = 1,columnspan=1,sticky=W)
label_task_7.grid(row=7,column = 1,columnspan=1,sticky=W)
label_task_8.grid(row=8,column = 1,columnspan=1,sticky=W)
label_task_9.grid(row=9,column = 1,columnspan=1,sticky=W)
label_task_10.grid(row=10,column = 1,columnspan=1,sticky=W)
#endregion

# Buton quit
quit_b = Button(interface, text = "Quit", command=quit)
quit_b.grid(row=27,column=23,columnspan=1)
    
interface.mainloop()