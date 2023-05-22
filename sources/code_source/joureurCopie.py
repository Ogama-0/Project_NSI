import pygame
class Player(pygame.sprite.Sprite) :

    def __init__(self, x ,y):
        super().__init__()
        
        self.deplacement = [0,0] #pour géré le deplacement (velocité*vitesse)
        self.position = [x,y]#position actuelle du joueurs
        self.sprint = 0
        self.imageux = pygame.image.load("sources/sprite/sprite nanit/sprite nanit droite/nanit_droite_yeux_fermer.png").convert_alpha()
        self.rect = self.imageux.get_rect(x=self.position[0] , y=self.position[1] )# position et hitbox qui est get de l'image par pygame et que on associe a la position de notre personnage
        self.vitesse = 2 #vitesse du perso (2 c'est random t'a capter)
        self.layer = 8
        self.name = "Nanit"
        self.velocite =[0,0] #la velocyté c'est de cb1 le person vas se deplacer en [x,y] en 1 frame(multiplier a self.vitesse)
        self.curent_dezoom = False
        # ------------------- Collision ---------------------------#
        self.position_pour_les_colision = pygame.Rect(0, 0, self.rect.width*0.70, 15)
        self.old_position = self.position.copy()
        self.move_back_var = False
        # ------------------- Graphiquement ------------------------#
        self.deplacement_final = list()

        self.animation = 0
        self.animation_yeux = 0
        self.curent_sprite = "face"
        self.curent_taille_sprite = "grand"
        self.curent_etat_yeux = "ouvert"
        self.images_fermer = {}
        self.images_ouvert = {}
        # ------------------------- IMAGE NANIT -------------------------- #
        self.images = {}
            # ---------------- image_grand ---------------------- #
            
         
        self.images_fermer["droite"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit droite/nanit_droite_yeux_fermer.png").convert_alpha()
        self.images_ouvert["droite"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit droite/nanit_droite_yeux_ouver.png").convert_alpha()
        self.images_fermer["gauche"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit gauche/nanit_gauche_yeux_fermer.png").convert_alpha()
        self.images_ouvert["gauche"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit gauche/nanit_gauche_yeux_ouver.png").convert_alpha()
        self.images_fermer["face"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit face/nanit_face_yeux_fermé.png").convert_alpha()
        self.images_ouvert["face"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit face/nanit_face_yeux_ouverts.png").convert_alpha()
        self.images_ouvert["dos"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_base.png").convert_alpha()
        self.images_fermer["dos"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_base.png").convert_alpha()
        self.images_ouvert["dos_gauche"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_gauche.png").convert_alpha()
        self.images_fermer["dos_gauche"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_gauche.png").convert_alpha()
        self.images_ouvert["dos_droite"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_droite.png").convert_alpha()
        self.images_fermer["dos_droite"] = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_droite.png").convert_alpha()
        # ---------------- image_petit ---------------------- #
        

        
        self.images["grand"] = dict()
        self.images["petit"] = dict()
        self.images["grand"]["fermer"] = self.images_fermer
        self.images["grand"]["ouvert"] = self.images_ouvert
        self.images["petit"]["fermer"] = dict()
        self.images["petit"]["ouvert"] = dict()
        for F_O in self.images["grand"].keys() :
                for K_SPRITE in self.images["grand"][F_O].keys() :
                    self.images["petit"][F_O][K_SPRITE] = pygame.transform.smoothscale(self.images["grand"][F_O][K_SPRITE],(18,32))

        self.image = self.images[self.curent_taille_sprite][self.curent_etat_yeux][self.curent_sprite] #big dico sa grand-mère qui contient tout les images du perso, petit et grand, yeux ouvert et fermer, de face de profil et de dos
    #--------------- update  ---------------#
    
    def update(self) :
        self.rect.midbottom = self.position.midbottom
        self.position_pour_les_colision.midbottom = self.position.midbottom
        if self.curent_taille_sprite == "grand" :
            self.position_pour_les_colision.height = 15
            self.position_pour_les_colision.width = self.rect.width*0.70
        else :
            self.position_pour_les_colision.width = self.rect.width*0.70
            self.position_pour_les_colision.height = self.rect.height*0.90


    #---------------------------- Animation ---------------------------#
    def attribuer_sprite(self) : self.image = self.images[self.curent_taille_sprite][self.curent_etat_yeux][self.curent_sprite]

    def Animation(self) :
        """gere toutes les animation du perso"""
        self.attribuer_sprite()
        if self.velocite[0] + self.velocite[1] == 0 : self.animation_yeuxfonc()#savoir si l'anime s'est deja passer

    def animation_yeuxfonc(self) :
        self.animation_yeux += 1
        if self.animation_yeux >= 301 : self.animation_yeux = 0
        elif self.animation_yeux >= 250 : self.curent_etat_yeux = "fermer"
        else : self.curent_etat_yeux = "ouvert"

    def changer_zoom(self, zoom:bool)-> None :
        if zoom :
            self.curent_taille_sprite = "petit"
            self.rect = self.images[self.curent_taille_sprite][self.curent_etat_yeux][self.curent_sprite].get_rect(x=self.position[0], y=self.position[1])

        else : 
            self.curent_taille_sprite = "grand"
            self.rect = self.images[self.curent_taille_sprite][self.curent_etat_yeux][self.curent_sprite].get_rect(x=self.position[0], y=self.position[1])