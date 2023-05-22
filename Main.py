# Name : Project_Z
#
# Purpose : RPG en 2D d'enigme 
#
# Author :  Oscar Cornut
#           Laura NOPHAKHOUN
#           Ludivine FORFAIT
#           Ewen BONNET
#
# Created : entre 01/03/2023 et 17/04/2023
# Copyright : (c) Oscar Cornut 2023
# Licence : GPL V3+
# ----------------------------------------------------------------------------------------------------------------------------------------------- #
import pygame
from sources.code_source.joureurCopie import Player
from sources.code_source.Cartecode import Map_manager
from sources.code_source.Menu_princ import Menu, Degrader
from sources.code_source.dialogue import Dialogue
from dataclasses import dataclass
import time
@dataclass
class stk_bouton :
    nom : str
    position : tuple[int]
    cliquable : bool = False


class Game : # ici c'est la classe scène
    
    def __init__ (self) :
        self.screen = pygame.display.set_mode((1080,720))
        pygame.display.set_caption('Project_Z')
        self.continuer = True
        self.clock = pygame.time.Clock()
        self.degrader = Degrader(self.screen)
        self.premier_passage_souris = False
        self.clique_souris = False
        self.menu_credit_princ_actif = False
        self.frame = 0

        
        #----------------------------minuteur--------------------------------#
        self.font_debaze = pygame.font.SysFont("monospace",16)
        self.start_time = time.time()
        self.nombre_de_frame = 0
        self.seconde_de_jeu = 0
        self.minute_de_jeu = 0
        self.heure_de_jeu = 0
        self.texte_minuteur = ""
        
        #--------------------------- joueur ---------------------------------#
        
        self.player = Player(0,0)
        self.tiping = False
        # ------------------------- Globale -------------------------------- #
        self.menu_princ_actif = True
        self.menu_comande_actif = False
        self.menu_princ_option_actif = False
        self.menu_princ_comande_actif = False
    # ------------------------------ GESTION DES MENUS ---------------------------- #
    # pour rajouter un bouton a un menue le créé juste en dessou, en faisant une list avec ["le nom du bouton (le fichier image est chercher avec sprite/autre/menu/{nom}_bouton et sprite/autre/menu/{nom}_bouton_appuyer pour quand on passe la souris dessu),(les coo du bouton dans le sceen)"]
        # boutons des menus
        hauteur_minimum = 230
        x_bouton = 419
        bouton_start = stk_bouton("start",(x_bouton,hauteur_minimum))
        bouton_options = stk_bouton("option",(x_bouton,hauteur_minimum + 60*2))
        bouton_credit = stk_bouton("credit",(x_bouton,hauteur_minimum + 60*4))
        bouton_switch = stk_bouton("switch",(x_bouton,hauteur_minimum + 60*2))
        bouton_musique = stk_bouton("musique",(x_bouton,hauteur_minimum + 60*4),True)
        bouton_comande = stk_bouton("comande",(x_bouton,hauteur_minimum + 60*2))
        bouton_reprendre = stk_bouton("resume",(x_bouton,hauteur_minimum))
        bouton_quitter_menu = stk_bouton("quitter_menu",(90,90))

        self.frame_ = 0

        background_menu_principale = []
        for i in range(3) :
            background_menu_principale.append(pygame.transform.scale(pygame.image.load(f"sources/sprite/autre/menu/backgound_Principal_{i+1}.png"),(1080,720)))
        
        background_menue_pause = []
        for i in range(3) :
            background_menue_pause.append(pygame.transform.scale(pygame.image.load(f"sources/sprite/autre/menu/backgound_Pause_{i+1}.png"),(1080,720)))

        background_menue_option = []
        for i in range(3) :
            background_menue_option.append(pygame.transform.scale(pygame.image.load(f"sources/sprite/autre/menu/backgound_Option_{i+1}.png"),(1080,720)))
         
        background_menue_comande = []
        for i in range(3) : 
            background_menue_comande.append(pygame.transform.scale(pygame.image.load(f"sources/sprite/autre/menu/backgound_Commande_{i+1}.png"),(1080,720)))
        
        background_FIN = []
        for i in range(3) :
            background_FIN.append(pygame.transform.scale(pygame.image.load(f"sources/sprite/autre/menu/backgound_FIN_{i+1}.png"),(1080,720)))

        background_credit = []
        for i in range(1) :
            background_credit.append(pygame.transform.scale(pygame.image.load(f"sources/sprite/autre/menu/backgound_credit_{i+1}.png"),(1080,720)))
        

        self.premier_passage4 = True

        #pour modifier ou rajourter une action a des bouton il faut aller dans la loop du menu corespondant
        self.menus = []

        bouton_menu_principale = [bouton_start,bouton_options,bouton_credit,bouton_quitter_menu]
        self.menu_princ = Menu(self.screen,bouton_menu_principale,background_menu_principale)

        bouton_menue_pause = [bouton_reprendre,bouton_musique,bouton_comande,bouton_quitter_menu]
        self.menu_pause = Menu(self.screen,bouton_menue_pause,background_menue_pause)

        boutons_menu_option = [bouton_musique,bouton_comande,bouton_quitter_menu]
        self.menu_option = Menu(self.screen,boutons_menu_option,background_menue_option)
        self.menu_princ_option = Menu(self.screen,boutons_menu_option,background_menue_option)
        

        bouton_menu_comande = [bouton_quitter_menu]
        self.menu_comande = Menu(self.screen,bouton_menu_comande,background_menue_comande)


        self.menu_comandePAUSE = Menu(self.screen,bouton_menu_comande,background_menue_comande)
        self.menu_comande1PRIN = Menu(self.screen,bouton_menu_comande,background_menue_comande)

        self.bouton_fin = [bouton_credit,bouton_quitter_menu]
        self.menu_fin = Menu(self.screen,self.bouton_fin,background_FIN)
    

        boutons_credit = [bouton_quitter_menu]
        self.menu_credit = Menu(self.screen,boutons_credit,background_credit)
        self.menus = [self.menu_princ,self.menu_pause,self.menu_option,self.menu_princ_option,self.menu_comande,self.menu_comandePAUSE,self.menu_comande1PRIN,self.menu_fin]

        self.menu_princ_credi = Menu(self.screen,boutons_credit,background_credit)


        self.curent_option = False
        self.curent_credit = False
        
        # --------------------------------- MAP -----------------------------#
        self.map_manager = Map_manager(self.screen, self.player)

        
        # --------------------------- clef ----------------------------------#
        self.clef_image = pygame.image.load("sources/sprite/sprint_enigme/autre/clef.png")
        self.pass_image = pygame.transform.scale(pygame.image.load("sources/sprite/sprint_enigme/autre/passe_future.png"),(64,64))
        self.position_clef = {}

        for nom_map in self.map_manager.maps.keys() :
            x = 930
            y = 70
            for k in self.map_manager.get_map(nom_map).clefs.keys() :
                
                if k != nom_map :
                    x += 30
                    if x >= 1080 :
                        y += 70
                        x = 960
                    self.position_clef[k] = (x,y)

        
        #------------------------------Dialogue------------------------------#
        self.afficeher_texte_tiping = True
        self.touches_une_fois_espace = False
        self.touches_une_fois_e = False
        self.premier_passage0 = True
        self.premier_passage1 = True
        self.premier_passage2 = True
        self.premier_passage3 = True
        self.texte_afficher = ""
        self.stok = 0

    #------------------------------------------------------ FONCTION ----------------------------------------------------#
    def touches_appuiller(self):
        """loop d'event stoker dans self.touches"""
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                self.continuer = False
            if self.tiping and self.get_curent_tiping() :
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE :
                        self.texte_afficher = self.texte_afficher[:-1]
                        
                    elif event.key == pygame.K_RETURN :
                        if self.map_manager.verifier_enigme(self.texte_afficher) :
                            self.texte_afficher = ""
                    elif event.key != pygame.K_ESCAPE :    
                        self.texte_afficher+=event.unicode
        
        self.touches = pygame.key.get_pressed()

    def minueur(self):
        """permet d'avoir le temps de jeu avec self.seconde_de_jeu puis self.minute_de_jeu puis self.heure_de_jeu"""

        elapsed_time = time.time() - self.start_time
        seconde = int(float("{:.2f}".format(elapsed_time)))

        if self.stok != seconde :
            self.seconde_de_jeu +=1
        
        
        
        self.nombre_de_frame += 1
        if self.nombre_de_frame == 60 :
            self.nombre_de_frame = 0
        
        
        if self.seconde_de_jeu // 60 == self.seconde_de_jeu/60 and self.seconde_de_jeu != 0 :
            self.seconde_de_jeu = 0
            self.minute_de_jeu += 1
        if self.minute_de_jeu >= 60 :
            self.minute_de_jeu = 0
            self.heure_de_jeu += 1   
        self.stok = seconde     

    def gestion_sprint(self) :
        """savoir si la touche shift et apuiller et si oui il met la valeur self.player.sprint a 2 sinon à 0"""

        if self.touches[pygame.K_LSHIFT] :
            self.player.sprint = 2
        else :
            self.player.sprint = 0

    def gestion_deplacement(self):
        
        """savoir quelle touches sont activer et modifi les variable en consequance"""

        a=0 #savoir s i l'anime s'est deja passer  
        if self.touches[pygame.K_UP] :
            self.player.velocite[1] = -1
            self.player.etat_regard_yeux_nanit['etat_regard'] = 3
        elif self.touches[pygame.K_DOWN] :
            self.player.velocite[1] = 1
            self.player.etat_regard_yeux_nanit['etat_regard'] = 4
        else :
            self.player.velocite[1] = 0
            a+=1

        if self.touches[pygame.K_LEFT] :
            self.player.velocite[0] = -1
            self.player.etat_regard_yeux_nanit['etat_regard'] = 1 
        elif self.touches[pygame.K_RIGHT] :
            self.player.velocite[0] = 1
            self.player.etat_regard_yeux_nanit['etat_regard'] = 2
        else :
            self.player.velocite[0] = 0
            a+=1
        if self.touches[pygame.K_UP] and self.touches[pygame.K_RIGHT] :
            self.player.etat_regard_yeux_nanit['etat_regard'] = 5
        if self.touches[pygame.K_UP] and self.touches[pygame.K_LEFT] :
            self.player.etat_regard_yeux_nanit['etat_regard'] = 6
        self.player.vitesse += self.player.sprint
        
        self.player.deplacement = self.player.velocite[0]*self.player.vitesse, self.player.velocite[1]*self.player.vitesse
         

        # -----------------Animation----------------- #
        self.player.Animation(a)

        

    def update_dialogue(self):
        """ mis a jour des dialogues"""
        if self.get_affichagation() :
            transition = self.map_manager.get_Dialogue().update(self.touches,self.touches_une_fois_entrer,self.touches_une_fois_espace,self.get_stockage().curent_tiping)
            self.get_stockage().Fin = self.map_manager.get_Dialogue().Fin
            if self.get_stockage().Fin : self.get_stockage().curent_degrader = True
            self.get_stockage().curent_tiping = transition
    


    
        
    def  touche_une_foie(self) : 
        """ met la variable self.touches_une_fois_espace True seulement a la frame ou on apuit sur espace, la frame d'après ça le remet en false
        """
        self.touches_une_fois_espace = False
        self.touches_une_fois_entrer = False
        self.touches_une_fois_e = False

        if self.touches[pygame.K_SPACE] :
            if self.premier_passage0 :
                self.touches_une_fois_espace = True 
                self.premier_passage0 = False
            
        else :
            self.premier_passage0 = True
            self.touches_une_fois_espace = False
            self.touches_une_fois_entrer = False
        if self.touches[pygame.K_RETURN] :
            if self.premier_passage1 :
                self.touches_une_fois_entrer = True
                self.premier_passage1 = False
            
        else :
            self.premier_passage1 = True
            self.touches_une_fois_entrer = False
        
        if self.touches[pygame.K_e] :
            if self.premier_passage2 :
                self.touches_une_fois_e = True
                self.premier_passage2 = False
            
        else :
            self.premier_passage2 = True
            self.touches_une_fois_e = False

    
    def affichage_tiping(self) :

        if self.get_curent_tiping() and self.get_affichagation() :
            position_tiping = self.map_manager.get_position_tiping()
            font = self.get_dialogue().font
            self.texte_afficher_surface = font.render(self.texte_afficher,1,(0,0,0))
            self.screen.blit(self.texte_afficher_surface,position_tiping)
        
            
        
         
    def GestionEvent(self) : 
        """ici que sont géré les différents évenement comme l'appuit des touches ou le alt f4 ->(QUIT)"""

        self.touche_une_foie()
        self.player.deplacement = [0,0]
        if not self.get_affichagation() :
            self.gestion_sprint()
            self.gestion_deplacement()
        

    
    def update (self,touches) : #gestion de logique et la misa a jour des différents perso du jeu et les colisions
        """gestion de logique et la misa a jour des différents perso du jeu et les colisions"""
        if self.get_affichagation() :
            self.tiping = self.map_manager.get_tiping()

        
        self.map_manager.update(touches,self.touches_une_fois_e)
        
        self.update_dialogue()
        if touches[pygame.K_ESCAPE] :
            self.get_stockage().pause = True


    def affichage_dialogue(self) :
        """afiche le dialogue self.map_manageur.curent_dialogue"""
        for D in self.map_manager.get_Dialogues().keys() :
            if self.get_dialogue(D).affichagation and self.get_dialogue(D).inte.doit_afficher  :
                self.get_dialogue(D).afficher()


    def afficher_clefs(self):
        """choisi celfs ou pass et appelle la bonne fonction"""
        for k in self.map_manager.get_clefs().keys() :
            
            if self.map_manager.get_clefs()[k]  :
                if k != self.map_manager.curent_map :
                    if self.map_manager.curent_map == "futur" :
                        self.afficher_pass(k)
                    else : 
                        self.affichage_clefs(k)
                

    
    def afficher_pass(self,k) :
        """afffiche le pass"""
        self.screen.blit(self.pass_image,self.position_clef[k])
                    
    

    def affichage_clefs(self,k) :
        """affiche la celf"""
        self.screen.blit(self.clef_image,self.position_clef[k])

            
            

    def texte_to_surf(self,txt : str, color = (0,0,0), background = None, px_de_long : int = 0) :
        "convertie un str en surf affichage avec blit()"
        surf = self.get_dialogue().font.render(txt,1,color,background,px_de_long)
        return surf

    def get_affichagation(self) -> bool : return self.map_manager.get_affichagation()
    def get_dialogue(self,nom = None) -> Dialogue : return self.map_manager.get_Dialogue(nom)
    def get_curent_tiping(self) -> bool : return self.get_stockage().curent_tiping         
    def get_stockage(self): return self.map_manager.stockage_valeur
        


    def affichage(self) : #tout ce qui vas etre afficher dans le screen
        """ gère tout ce qui s'affiche sur le screen"""
         #initialisation de l'écrant (c'étais au debut je laisse tout pour l'instant pour corriger des erreurs plus facilement)
        
        
        self.map_manager.dessier_la_carte(self.nombre_de_frame)


        self.afficher_minuteur()

        self.affichage_dialogue()

        self.affichage_tiping()
       
        self.afficher_clefs()
        if not self.get_affichagation() :
            self.map_manager.stockage_valeur.curent_tiping = False 
        
        
    
    def afficher_degrader(self) : 
        if self.get_stockage().curent_degrader :
            self.degrader.curent_degrader = True
            self.degrader.afficher()
        if not self.degrader.curent_degrader :
            self.get_stockage().curent_degrader = False
        if self.get_stockage().contre_curent_degrader :
            self.degrader.contre_curent_degrader = True
            self.degrader.afficher_contre()
        if not self.degrader.contre_curent_degrader :
            self.get_stockage().contre_curent_degrader = False
            

    
    def afficher_minuteur(self) :
        """permet d'afficher le minuteur de la fonction minuteur() avec la police monospace"""
        
        
        if  self.heure_de_jeu == 0 :
            if self.minute_de_jeu == 0 :
                self.texte_minuteur = f"{self.seconde_de_jeu} seconde"
                
            else :
                self.texte_minuteur = f"{self.minute_de_jeu} minute et {self.seconde_de_jeu} seconde"
        else :
            if self.minute_de_jeu == 0 :
                self.texte_minuteur = f"{self.heure_de_jeu} heure et {self.seconde_de_jeu} seconde"
            else :
                self.texte_minuteur = f"{self.heure_de_jeu} heure {self.minute_de_jeu} minute et {self.seconde_de_jeu} seconde"
        

        self.score_text = self.font_debaze.render(f"temps de jeu : {self.texte_minuteur}",9,(255,255,255))

        self.screen.blit(self.score_text,(20,20))

    def run_game(self) :
        
        self.minueur()
        self.GestionEvent()
        
        self.update(self.touches)            
        self.affichage()
        
        

    # -------------------------------- MENU_PRINCIPALE ----------------------------- #
    
    def run_menue_princ(self) :
        if self.menu_princ_option_actif :
            if self.menu_princ_comande_actif : self.affichage_menu_comande()
            else : self.affichage_menu_option()
        elif self.menu_credit_princ_actif : self.afficher_menu_credit_prin()
        else :
            self.affichage_menu_princ()
    
    def premier_clique_souirs(self) -> bool :
        if pygame.mouse.get_pressed()[0] : 
            if self.premier_passage_souris :
                cliqued = True
                self.premier_passage_souris = False
            else  : cliqued = False
        else : 
            self.premier_passage_souris = True
            cliqued = False
        return cliqued
        

    

    def affichage_menu_comande(self) :
        boton_appuyer = self.menu_comande1PRIN.afficher(self.clique_souris)
        if boton_appuyer == "quitter_menu" :
            self.menu_princ_comande_actif = False
            self.menu_princ_option_actif = True

    

    def affichage_menu_option(self) :
        bouton_appuyer = self.menu_princ_option.afficher(self.clique_souris)
        if bouton_appuyer == "comande" :
            self.menu_princ_comande_actif = True
        elif bouton_appuyer == "quitter_menu" :
            self.menu_princ_option_actif = False       
        if bouton_appuyer == "musique" :
            if self.get_stockage().musique :
                self.get_stockage().musique = False
            else :
                self.get_stockage().musique = True

    def afficher_menu_credit_prin(self) :
        bouton_appuyer = self.menu_princ_credi.afficher(self.clique_souris)
        if bouton_appuyer == "quitter_menu" :
            self.menu_credit_princ_actif = False


        



    def affichage_menu_princ(self) :
        bouton_appuyer = self.menu_princ.afficher(self.clique_souris)
        if bouton_appuyer == "start" :
            self.menu_princ_actif = False
            self.get_stockage().curent_degrader = True
        elif bouton_appuyer == "option" :
            self.menu_princ_option_actif = True
        elif bouton_appuyer == "credit" :
            self.menu_credit_princ_actif = True
        elif bouton_appuyer == "quitter_menu" :
            self.continuer = False
    
    def firtst_run_Fin(self) :
        self.chec_fin_screen()
        

    def chec_fin_screen(self) :
        
        self.screen.blit(self.get_stockage().Fin_backgrounds[self.frame_],(0,0))
        self.maj_frame()
        self.frame += 1
        if self.frame == 60*4-40 :
            self.get_stockage().contre_curent_degrader = True
            self.get_stockage().decrechendo = True
        if self.frame > 60*4 :
            self.get_stockage().Fin = False
            self.get_stockage().curent_fin = True
    
    def maj_frame(self) :
        if self.frame//15 == self.frame/15 :
            self.frame_+=1
            if self.frame_ > len(self.get_stockage().Fin_backgrounds)-1 :
                self.frame_ = 0
        

    
# -------------------------------- MENUE PAUSE ------------------------------------ #
    def run_pause(self):
        self.get_stockage().volume_musique = 0.1
        if self.curent_option :
            self.afficher_option()
        elif self.menu_comande_actif :
            self.afficher_commande()
        else :
            self.afficher_pause()


    def afficher_pause(self) :
        
        menu_a_afficher = self.menu_pause.afficher(self.clique_souris)
        if menu_a_afficher == "quitter_menu" :
            self.continuer = False
        elif menu_a_afficher == "resume" :
            self.get_stockage().pause = False
            self.get_stockage().volume_musique = 0.25
            self.get_stockage().curent_degrader = True
        elif menu_a_afficher == "option" :
            self.curent_option = True
        elif menu_a_afficher == "musique" :
            if self.get_stockage().musique :
                self.get_stockage().musique = False
            else :
                self.get_stockage().musique = True
        elif menu_a_afficher == "comande" :
            self.menu_comande_actif = True
        
    
    def afficher_option(self) :
        boutons = self.menu_credit.afficher(self.clique_souris) 
        if boutons == "option" :
            self.curent_option = False
        if boutons == "musique" :
            if self.get_stockage().musique :
                self.get_stockage().musique = False
            else :
                self.get_stockage().musique = True
    
    def afficher_commande(self) :
        boutons = boutons = self.menu_comande.afficher(self.clique_souris)
        if boutons == "quitter_menu" :
            self.menu_comande_actif = False
    # écrant de fin 
    def run_fin(self):
        if self.curent_credit :
            self.afficher_credit()
        else :
            self.afficher_fin()


    def afficher_credit(self) :
        boutons = self.menu_credit.afficher(self.clique_souris)
        if boutons == "quitter_menu" :
            self.curent_credit = False


    def afficher_fin(self) :
        boutons = self.menu_fin.afficher(self.clique_souris)
        if boutons == "quitter_menu" :
            self.continuer = False
        elif boutons == "credit" :
            self.curent_credit = True
    
    def chec_globals(self) :
        self.clique_souris = self.premier_clique_souirs()
        if self.get_stockage().musique :
            self.map_manager.get_sound().set_volume(self.get_stockage().volume_musique)
            self.menu_pause.boutons["musique"].cliqued = False
        else :
            self.map_manager.get_sound().set_volume(0)
            self.menu_pause.boutons["musique"].cliqued = True
        
        for d in self.map_manager.get_Dialogues().values() :
            if d.affichagation : 
                self.get_stockage().dialogue_afficher = True
                return
            else : self.get_stockage().dialogue_afficher = False
        
    def decrechendo(self):
        if self.get_stockage().decrechendo :
            if self.get_stockage().volume_musique >= 0.001 :
                self.get_stockage().volume_musique -= 0.001
            else :
                self.get_stockage().volume_musique = 0
                self.get_stockage().decrechendo = False
    
    def afficher_autres_global(self) :
            self.afficher_degrader()
            self.decrechendo()



    def run (self): #boucle de jeu (tout globalemnt et c'est ça qui se rafraichie tout les frames )
        """run de tout le jeu"""

        while self.continuer :             
            self.chec_globals()
            
            self.screen.fill("black")   
            self.touches_appuiller()
            if self.get_stockage().Fin :
                self.firtst_run_Fin()

            elif self.get_stockage().curent_fin :
                if self.premier_passage3 :
                    self.get_stockage().curent_degrader = True
                    self.premier_passage3 = False
                self.run_fin()
                
            elif self.menu_princ_actif :
                self.run_menue_princ()

            elif self.get_stockage().pause :
                self.run_pause()

            else :
                self.run_game()

            self.afficher_autres_global()
            pygame.display.flip()#on met a jour l'écrant
            self.clock.tick(60)# gère a cb1 de fps le jeu tourne (60 c'est bien)
            

 # ----------------------------Programe pour initialiser le jeu --------------------------#


if __name__ == "__main__" :
    pygame.init()
    game = Game() 
    game.run()
    pygame.quit()