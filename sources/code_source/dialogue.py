import pygame
from sources.code_source.enigme_code import interact_ecrit

        

class inforamtion :

    def __init__(self,screen : pygame.surface.Surface,texte : str) :
        """créé un object information qui affiche selon le rect de get_object_by_name(texte) de pytmx"""
        self.screen = screen
        self.largeur = int(screen.get_width()//10.8)
        self.hauteur = int(screen.get_height()//48)
        police = int(self.screen.get_height()//72)

        self.font = pygame.font.Font("sources/sprite/autre/texte/dialog_font.ttf",police)
        self.position = [screen.get_width()//21.6,screen.get_height()//1.058823529]

        self.position_texte = [self.position[0] + 3,self.position[1]]

        self.background = pygame.transform.scale(pygame.image.load("sources/sprite/autre/texte/bulle_image_enigme.png"),(self.largeur,self.hauteur))

        self.texte_pas_surf = texte
        self.texte = self.font.render(texte,1,(0,0,0),None,self.largeur)
        self.entrer = self.font.render("entrer pour confirmer",1,(0,0,0),None,self.largeur)
        self.background_entrer = pygame.transform.scale(pygame.image.load("sources/sprite/autre/texte/bulle_image_enigme.png"),(self.largeur,int(screen.get_height()//24)))
        self.position_texte_entrer = [self.position[0] + 3,self.position[1] + 3]
        self.space = self.font.render("espace suivant",1,(0,0,0),None,self.largeur)
        

        

    def afficher_information(self,curent_tiping,curent_dialogue) :
        """ afficher les information contenue dans self.texte"""

        
        if curent_dialogue :
            if curent_tiping :
                self.screen.blit(self.background_entrer, self.position)
                self.screen.blit(self.entrer,self.position_texte_entrer)
            else :
                self.screen.blit(self.background, self.position)
                self.screen.blit(self.space,self.position_texte)
        elif self.texte_pas_surf != "":
            self.screen.blit(self.background, self.position)
            self.screen.blit(self.texte,self.position_texte)



class Dialogue :
    lettre = True
    def __init__(self,screen : pygame.surface.Surface,interact : interact_ecrit) :
        """créé un obect Dialogue"""
        definition = screen.get_width()*screen.get_height()
        self.inte = interact
        self.Fin = False
        police = int(definition//48600/2)
        if self.inte.nom == "armure" :
            police = int(definition//21016.21622/2)
        
        elif self.inte.nom == "code" :
            police = int(definition//25920/2)
        
        if self.inte.nom == "lettre" or self.inte.texts == "" :
            self.lettre = False
            self.font = pygame.font.Font("sources/sprite/autre/texte/lettre_font.ttf",int(definition//35345.45455/1.71))
        else :
            self.font = pygame.font.Font("sources/sprite/autre/texte/dialog_font.ttf",police)
        


        self.police_tiping = police
        
        
        self.curent_tipping = False
        self.screen = screen
        self.letter_index = 0
        self.curent_txt = 0
        self.nom = self.inte.nom
        self.nom_dialogue = self.inte.nom_dialogue

        self.affichagation = False
        if self.inte.nom == "start" :
            self.affichagation = True

        
        
        self.frame = True #ça sert juste a TAB pour accelerer les dialogues
        if self.inte.position_tiping == () :
            self.position_tiping = [self.inte.position_text[0],self.inte.position_text[1] + self.screen.get_height()//33.75]
        else :
            self.position_tiping = self.inte.position_tiping
        


    def update(self,touche,une_entrer,un_espace,curent_tiping) :
        "mis a jour du dialogue"
        if curent_tiping :
            if une_entrer :
                self.text_suivant()
                self.lettre_suivante(touche)
        else :
            if un_espace :
                self.text_suivant()
        if self.lettre :
            self.lettre_suivante(touche)

        if not self.inte.doit_afficher : self.affichagation = False
        
        return self.chec_tiping()
    
    def chec_tiping(self) :
        """regarde si il faut activer curent tiping"""
        if self.inte.texts != "" :
            if self.inte.texts[self.curent_txt] == " " or self.inte.texts[self.curent_txt] == "entrer votre reponse" :
                return True
            else : 
                return False

        
    


    def afficher(self) :
        """affiche le dialgoue"""
        self.afficher_bckgrnd()
        if self.inte.texts != "" :
            self.afficher_txt()



    def afficher_bckgrnd(self):
        """affiche ce qui est contenue dans self.inte.background"""
        self.screen.blit(self.inte.background,self.inte.position)
    
    def afficher_txt(self) :
        """affiche ce qui est contenue dans self.inte.texts[self.curent_txt]"""
        if self.lettre :
            strf = self.font.render(self.inte.texts[self.curent_txt][0 : self.letter_index],True,self.inte.couleur,None,self.inte.background.get_width()-50)
            self.screen.blit(strf,self.inte.position_text)
        
        else :
            surf = self.font.render(self.inte.texts[self.curent_txt],True,self.inte.couleur,None,self.inte.background.get_width()-50)
            self.screen.blit(surf,self.inte.position_text)



    def text_suivant(self) :
        """ hyp : sert a passer au text survant et si on a tout lu bah bing on ferme le dialogue
        """
        self.curent_txt += 1        

        if self.curent_txt >= len(self.inte.texts) :
            self.affichagation = False
            self.curent_txt = 0
            if not self.inte.recurence : 
                self.inte.doit_afficher = False
            
            if self.inte.nom == "dialogue_final" :
                self.Fin = True
        self.letter_index = 0

        
    def lettre_suivante(self,touche) :
        """ affiche une lettre apprès l'autre pour faitre styler"""
        if self.inte.texts == "" :
            return
        if self.letter_index < len(self.inte.texts[self.curent_txt]) :
            if not touche[pygame.K_TAB] :
                if self.frame == True :
                    self.letter_index +=1
                    self.frame = False
                else :
                    self.frame = True
            else :
                self.letter_index +=1
    
    def W_H(self, W_:int, H_:int)-> tuple[int, int]:
        """ transphorme un cohordonner sur un screen de 1080 par 720 en cohordonner en fonction du screen"""
        W = 1080
        H = 720
        return self.screen.get_width()*W_/W,self.screen.get_height()*H_/H
    
    def H(self, W_:int, H_:int)-> tuple[int, int]:
        """ transphorme un cohordonner sur un screen de 1080 par 720 en cohordonner en fonction du screen en gadans les propostions"""
        H = 720
        return self.screen.get_height()*W_/H,self.screen.get_height()*H_/H