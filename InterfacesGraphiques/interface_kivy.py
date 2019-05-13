import sys
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
import vtk

#Non compatible avec utilisation vtk : annulé

#ScreenManager

class MainMenu(Screen):

    def remove_hide(self):
        self.remove_widget(self.showable)
        
    def show_hide(self):
        self.s1=TEST()
        self.hideable.add_widget(self.showable)


    def display_FTR(self):
        ftr=File_to_run(id='ftr')
        self.hideable.add_widget(ftr)
    
    def display_RP(self):
        rp=Run_process()
        self.hideable.add_widget(rp)

    def close(self):
        self.remove_widget(self.hideable).test

class File_to_run(FloatLayout): #fic_input
    nom_fichier=ObjectProperty()
    result_spinner=ObjectProperty()
    def close(self):
        app.root.close()

    def return_file(self):
        re='Error'
        i=0
        re=self.nom_fichier.text #retourne le path entré
        if self.result_spinner.text=='Oui': #retourne le choix sous forme 1 ou 2
            i=1
        elif self.result_spinner.text=='Non':
            i=2
        return re,i

    def test_result(self):
        result=''
        d,c=self.return_file()
        result=(d,c)
        print(result)

class Run_process(BoxLayout): #get_one_or_two
    def check_choice(self):
        ans=0
        if self.chk_male.active:
            ans=1
        elif self.chk_female.active:
            ans=2
        return ans

    def return_choice(self):
        print(self.check_choice())
        

class File_to_store(Screen): #fic_input
    pass

class View(Screen):
    pass

class Get_csv_obj(Screen): #get_one_or_two
    pass

class Mode_libre(Screen):
    pass

class Garbage(Screen): #get_one_or_two
    pass

class QuitButton(Button):

    def _sure(self):
        poo=Quit()
        poo.open()

class Quit(Popup):
    
    def _quit(self):
        sys.exit(0)


Builder.load_file(filename='inter.kv')


class SwipApp(App):
    def build(self):
        self.title="Modelo"
        sm = ScreenManager()
        e1=MainMenu()
        e4=File_to_store()
        e5=View()
        e6=Get_csv_obj()
        e7=Mode_libre()
        e8=Garbage()
        sm.add_widget(e1)
        sm.add_widget(e4)
        sm.add_widget(e5)
        sm.add_widget(e6)
        sm.add_widget(e7)
        sm.add_widget(e8)

        return sm




if __name__=="__main__":
    SwipApp().run()    