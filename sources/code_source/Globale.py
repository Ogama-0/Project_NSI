from screeninfo import get_monitors
import pygame
class Globale :
    SIZE_SCREEN = (get_monitors()[0].width,get_monitors()[0].height)

    def W_H(W_:int, H_:int)-> tuple[int, int]: return int(Globale.SIZE_SCREEN[0] * (W_ / 1080)), int(Globale.SIZE_SCREEN[1] * (H_ / 720))
    
    def H(W_:int, H_:int)-> tuple[int, int]: return int(Globale.SIZE_SCREEN[1] * (W_ / 720)), int(Globale.SIZE_SCREEN[1] * (H_ / 720))
    
    def W(W_:int, H_:int)-> tuple[int, int]: return int(Globale.SIZE_SCREEN[0] * (W_ / 1080)), int(Globale.SIZE_SCREEN[0] * (H_ / 1080))
    
    def MID_H_W(taille:tuple[int, int])-> tuple[int, int]:
        """prend un tuple en entrer, et retrun un tuple qui donne les cohordoné ou une potentielle surface de taille du tuple en entrer peu etre blit pour que cette surface soit exactement center """
        co = list(taille)
        co[0] = int(Globale.SIZE_SCREEN[0]//2) - int(taille[0]//2)
        co[1] = int(Globale.SIZE_SCREEN[1]//2) - int(taille[1]//2)
        return co

    def MID_H(taille:tuple[int ,int], coo_par_defaut:list[int, int]=None)-> tuple[int, int]:
        """prend un tuple en entrer, et retrun un tuple qui donne les cohordoné ou une potentielle surface de taille du tuple en entrer peu etre blit pour que cette surface soit exactement center au niveau des y   """
        if coo_par_defaut!= None :co = list(coo_par_defaut)
        else :co = list(taille)
        co[1] = int(Globale.SIZE_SCREEN[1]//2) - int(taille[1]//2)
        return co


    def MID_W(taille:tuple[int ,int], coo_par_defaut:list[int, int]=None)-> tuple[int, int]:
        """prend un tuple en entrer, et retrun un tuple qui donne les cohordoné ou une potentielle surface de taille du tuple en entrer peu etre blit pour que cette surface soit exactement center au niveau des x  """
        if coo_par_defaut!= None :co = list(coo_par_defaut)
        else :co = list(taille)
        co[0] = int(Globale.SIZE_SCREEN[0]//2) - int(taille[0]//2)
        return co

    def map_to_screenlist(li:list[int, int], vecteur_mapscreen:tuple[int, int], zoom:int)-> list[int]:
        """ça marche :)"""
        end_li = []
        j=0
        for i in li :
            end_li.append((i + vecteur_mapscreen[j])*zoom)
            j += 1
        return end_li