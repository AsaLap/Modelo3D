from tkinter import *
from tkinter import ttk
import test
import cube_test

#Fonctions 

def verif(champ,checkvar1,checkvar2):
    """
    Récupère les entrées des champs et le choix des cases
    Le choix des cases renvoie 1 pour OUI (case 'oui' oui cochée et case 'non' décochée), 
    2 pour NON et 3 si l'utilisateur ne cose aucune case ou s'il coche les deux 

    """
    CSV=champ.get()
    Lidar=0
    if ((checkvar1.get()==True) and (checkvar2.get()==False)):
        Lidar=1
    elif ((checkvar1.get()==False) and (checkvar2.get()==True)):
        Lidar=2
    elif (checkvar1.get()==checkvar2.get()):
        Lidar=3
    return CSV,Lidar


def verif_fic_run(champ,checkvar1,checkvar2,checkvar3,checkvar4,modul):
    """
    Récupère la totalité des entrées du premier onglet
    Liée au bouton OK du premier onglet
    """
    CSV,Lidar=verif(champ,checkvar1,checkvar2)
    modulo,socle=verif(modul,checkvar3,checkvar4)
    test.file_to_run(CSV,Lidar,socle,modulo)

def verif_fic_store(champ1,checkvar1,checkvar2,checkvar3,checkvar4,pla,com):
    CSV,Lidar=verif(champ1,checkvar1,checkvar2)
    planete,socle=verif(pla,checkvar3,checkvar4)
    comm=com.get()
    test.file_to_store(CSV,Lidar,socle,planete,comm)
    



#Initialisation

glob=Tk()
glob.title('Modélisation')

style=ttk.Style(glob)
#Position verticale et sur la gauche w : west et n : north
style.configure('lefttab.TNotebook', tabposition='wn') 
n = ttk.Notebook(glob, style='lefttab.TNotebook')
n.pack()


    #Création des onglets 

file_to_run=ttk.Frame(n)
file_to_run.pack()

run_process=ttk.Frame(n)
file_to_run.pack()

file_to_store=ttk.Frame(n)
file_to_store.pack()

view=ttk.Frame(n)
view.pack()

get_csv_obj=ttk.Frame(n)
get_csv_obj.pack()

mode_libre=ttk.Frame(n)
mode_libre.pack()

stockage=ttk.Frame(n)
stockage.pack()

    #Ajout des onglets

n.add(file_to_run,text="Source locale                        ")
n.add(run_process,text="Source sur base de données")
n.add(file_to_store,text="Sauvegarder dans BDD        ")
n.add(view,text="View                                      ")
n.add(get_csv_obj,text="Fichier CSV ou OBJ              ")
n.add(mode_libre,text="Mode libre (Dev                    ")
n.add(stockage,text="Stockage                               ")


#////FILE TO RUN _ Source locale


    #Entrée du nom de fichier
test_text=Label(file_to_run,text="Nom du fichier (et chemin d'accès complet)")
entree_nom=Entry(file_to_run)

    #Provenance 
provenance=Label(file_to_run,text="Fichier en provenance d'une acquisition Lidar")

CheckVar1=BooleanVar()
CheckVar2=BooleanVar()

check_yes=Checkbutton(file_to_run,text="Oui",variable=CheckVar1)
check_no=Checkbutton(file_to_run,text="Non",variable=CheckVar2)

    #Proposition d'un socle 
ajout = Label(file_to_run, text = "Ajouter un socle au traitement permettant l'impression 3D")

CheckVar3 = BooleanVar()
CheckVar4 = BooleanVar()

check_yes1 = Checkbutton(file_to_run, text = "Oui", variable = CheckVar3)
check_no1 = Checkbutton(file_to_run, text = "Non", variable = CheckVar4)

    #modulo
modulo_proposition = Label(file_to_run, text = "Modulo désiré")
mod = Entry(file_to_run)

    #acquisition des entrées CSV, Lidar, Socle, Modulo

select_ok=Button(file_to_run,text='OK',command=lambda : verif_fic_run(entree_nom,CheckVar1,CheckVar2,CheckVar3,CheckVar4,mod),
    width=10,height=3)

    #Ajout des widgets

test_button=Button(file_to_run,text="test",command=lambda:cube_test.main())
test_button.grid(column=1000,row=1000)

test_text.grid(column=0,row=0)
entree_nom.grid(column=1,row=0,pady=10)

provenance.grid(column=1,row=2,pady=10)
check_yes.grid(column=0,row=3)
check_no.grid(column=2,row=3,padx=40)

ajout.grid(column=1,row=4,pady=10)
check_yes1.grid(column=0,row=5)
check_no1.grid(column=2,row=5,pady=10)

modulo_proposition.grid(column=0,row=6)
mod.grid(column=1,row=6,pady=10)

select_ok.grid(column=1,row=7,pady=15)


#////RUN PROCESS _ Source sur base de données

lab=Label(run_process,text='Voulez vous sauvegarder ?')
first_check=Checkbutton(run_process, text="Oui")
scnd_check=Checkbutton(run_process,text="Non")
btn=Button(run_process,text='QUIT',command=glob.destroy)
slc=Button(run_process,text="OK",command=None)

lab.grid(column=0,row=0)
first_check.grid(column=1,row=0)
scnd_check.grid(column=1,row=1)
slc.grid(column=2,row=0)
btn.config(height=1, width=25)
btn.grid(column=2,row=2)

#FILE TO STORE _ Sauvegarde dans BDD

    #Entrée du nom de fichier
test_text=Label(file_to_store,text="Nom du fichier (et chemin d'accès complet)")
nom1=Entry(file_to_store)

    #Provenance 
provenance=Label(file_to_store,text="Fichier en provenance d'une acquisition Lidar")

CheckVar5=BooleanVar()
CheckVar6=BooleanVar()

check_yes2=Checkbutton(file_to_store,text="Oui",variable=CheckVar5)
check_no2=Checkbutton(file_to_store,text="Non",variable=CheckVar6)

    #Proposition d'un socle 
ajout = Label(file_to_store, text = "Ajouter un socle au traitement permettant l'impression 3D")

CheckVar7 = BooleanVar()
CheckVar8 = BooleanVar()

check_yes3 = Checkbutton(file_to_store, text = "Oui", variable = CheckVar7)
check_no3 = Checkbutton(file_to_store, text = "Non", variable = CheckVar8)



    #planete et commentaire
ann_planete=Label(file_to_store,text="Nom de la planète/astre")
planete=Entry(file_to_store)
ann_commentaire=Label(file_to_store,text="Commentaires (facultatif)")
commentaire=Entry(file_to_store)

    #Button
select_ok1=Button(file_to_store,text='OK',command=lambda : verif_fic_store(nom1,CheckVar5,CheckVar6,CheckVar7,CheckVar8,planete,commentaire),
    width=10,height=3)

    #Ajout des widgets

test_text.grid(column=0,row=0)
nom1.grid(column=1,row=0,pady=10)

provenance.grid(column=1,row=2,pady=10)
check_yes2.grid(column=0,row=3)
check_no2.grid(column=2,row=3,padx=40)

ajout.grid(column=1,row=4,pady=10)
check_yes3.grid(column=0,row=5)
check_no3.grid(column=2,row=5,pady=10)

ann_planete.grid(column=0,row=6)
planete.grid(column=1,row=6,pady=10)

ann_commentaire.grid(column=0,row=7)
commentaire.grid(column=1,row=7,pady=10)

select_ok1.grid(column=1,row=8,pady=15)


#VIEW

#GET CSV OBJ

#MODE LIBRE

#Stockage


glob.mainloop()
