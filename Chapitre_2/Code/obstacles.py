import pygame
from tower import Tower
from trap import Trap
from spike import Spike

obstacles = [pygame.Rect(1100, 950, 50, 50), pygame.Rect(0, 1010, 3100, 500), pygame.Rect(1000, 700, 50, 250), pygame.Rect(500, 950, 150, 50), 
pygame.Rect(660, 870, 60, 20), pygame.Rect(760, 790, 60, 20), pygame.Rect(860, 710, 60, 20), pygame.Rect(1400, 700, 250, 350), pygame.Rect(1300, 845, 60, 20),
pygame.Rect(1350, 935, 60, 20), pygame.Rect(1350, 760, 60, 20), pygame.Rect(1750, 650, 80, 20), pygame.Rect(2000, 850, 80, 20), pygame.Rect(2200, 780, 100, 20),
pygame.Rect(2300, 910, 250, 100), pygame.Rect(2300, 680, 250, 120), pygame.Rect(2200, 960, 50, 50), pygame.Rect(2250, 910, 50, 100), pygame.Rect(2400, 640, 150, 50),
pygame.Rect(2400, 590, 150, 50), pygame.Rect(2625, 830, 50, 200), pygame.Rect(2800, 830, 50, 180), pygame.Rect(2975, 830, 50, 180), pygame.Rect(3200, 250, 150, 20),
pygame.Rect(3200, 1000, 80, 20), pygame.Rect(3400, 1000, 80, 20), pygame.Rect(3600, 1000, 80, 20),pygame.Rect(3800, 1000, 80, 20), pygame.Rect(4000, 1000, 80, 20), 
pygame.Rect(3400, 400, 150, 20), pygame.Rect(3400, 550, 150, 20), pygame.Rect(3600, 300, 150, 20), pygame.Rect(3900, 650, 520, 20), pygame.Rect(4600, 1010, 3000, 500)]

towers = [Tower("classique", -600, -600), Tower("degats_de_zone", -1000, -450), Tower("classique", -1900, -1000), Tower("degats_de_zone",-2250, -425), 
Tower("classique", -2740, -920), Tower("classique", -2915, -920), Tower("classique", -3500, -700), Tower("degats_de_zone", -4300, -300)]

traps = [Trap(-800, -1000), Trap(-2225, -935), Trap(-2175, -985), Trap(-3980, -640)]
spikes = [Spike(-2740, -1000), Spike(-2915, -1000), Spike(-4040, -980), Spike(-3680, -280), Spike(-3250, -1070), Spike(-3250, -1070), Spike(-3300, -1070),
Spike(-3350, -1070), Spike(-3400, -1070), Spike(-3450, -1070), Spike(-3500, -1070), Spike(-3550, -1070), Spike(-3600, -1070), Spike(-3650, -1070), 
Spike(-3700, -1070), Spike(-3750, -1070), Spike(-3800, -1070), Spike(-3850, -1070), Spike(-3900, -1070), Spike(-3950, -1070), Spike(-4000, -1070), 
Spike(-4200, -630), Spike(-4625, -990)]
