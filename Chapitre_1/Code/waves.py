
import Chapitre_1.Code.class_Enemy as class_Enemy
import Chapitre_1.Code.groups as groups

#class Wave:
    #def __init__(self, wave_number, enemies, enemy_spawn_interval):
        #self.wave_number = wave_number
        #self.enemies = enemies
        #self.enemy_spawn_interval = enemy_spawn_interval
        #self.enemies_left_to_spawn = sum([count for _, count in enemies])
        #self.in_progress = False

    #def start_wave(self):
        #self.in_progress = True

startpos_x = 1042
startpos_y = 160

def generate_waves():
    waves = [
    [("Croix", 10)],
    [("Croix", 5), ("Losange", 6)],
    [("Croix", 5), ("Rectangle", 3)],
    [("GrandeCroix", 2), ("Fleche", 2)],
    [("Losange", 10), ("Coeur", 2)],
    [("Rectangle", 5), ("Fleche", 3)],
    [("Croix", 5), ("GrandeCroix", 2), ("Losange", 5)],
    [("Losange", 5), ("Rectangle", 5), ("Fleche", 2), ("Coeur", 2)],
    [("Croix", 5), ("GrandeCroix", 3), ("Rectangle", 3), ("Fleche", 3), ("Coeur", 3)],
    [("Croix", 10), ("Losange", 5), ("Rectangle", 5), ("Hexagone", 1), ("Fleche", 3), ("Coeur", 3)],
    ]

    return waves

    
def spawn_next_ennemy(wave,index,cpt,len_wave) :
    new_len_wave = len_wave

    duo = wave[index]
    try :
        cpt[index] += 1
        if cpt[index] == duo[1] :
                
            del wave[index]
            del cpt[index]
            new_len_wave -= 1
        
    except   IndexError :
        if duo[1]== 1:
            del wave[index]
            new_len_wave -= 1
        else :
            cpt.append(1)

    ennemy = class_Enemy.enemy_classes[duo[0]]
    groups.enemy_group.add(ennemy(startpos_x ,startpos_y))
    if index+1 >= new_len_wave:
        return 0,new_len_wave
    else :
        return index+1,new_len_wave
            

    
