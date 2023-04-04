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
pygame.Rect(3400, 400, 150, 20), pygame.Rect(3400, 550, 150, 20), pygame.Rect(3600, 300, 150, 20), pygame.Rect(3900, 650, 520, 20), pygame.Rect(4600, 1010, 3000, 500),
pygame.Rect(5100, 910, 80, 20), pygame.Rect(4900, 850, 80, 20), pygame.Rect(5080, 760, 80, 20), pygame.Rect(5270, 690, 80, 20), pygame.Rect(5100, 590, 80, 20),
pygame.Rect(5250, 510, 80, 20), pygame.Rect(5420, 430, 80, 20), pygame.Rect(5650, 510, 80, 20), pygame.Rect(5820, 590, 80, 20), pygame.Rect(6050, 40, 50, 750),
pygame.Rect(5650, 690, 80, 20), pygame.Rect(5670, 840, 80, 20), pygame.Rect(5450, 620, 150, 50), pygame.Rect(5810, 870, 80, 20), pygame.Rect(5810, 740, 1250, 50),
pygame.Rect(5950, 920, 120, 20), pygame.Rect(6050, 860, 50, 150)]

towers = [Tower("classique", -600, -600), Tower("degats_de_zone", -1000, -450), Tower("classique", -1900, -1000), Tower("degats_de_zone",-2250, -425), 
Tower("classique", -2740, -1000), Tower("classique", -2915, -1000), Tower("classique", -3500, -700), Tower("degats_de_zone", -4300, -300),
Tower("degats_de_zone", -5000, -320), Tower("sniper", -5850, -350), Tower("degats_de_zone", -6125, -985)]

traps = [Trap(-800, -1000), Trap(-2225, -935), Trap(-2175, -985), Trap(-3980, -640)]
spikes = [Spike(-2740, -910), Spike(-2915, -910), Spike(-4040, -980), Spike(-3680, -280), Spike(-3250, -1070), Spike(-3250, -1070), Spike(-3300, -1070),
Spike(-3350, -1070), Spike(-3400, -1070), Spike(-3450, -1070), Spike(-3500, -1070), Spike(-3550, -1070), Spike(-3600, -1070), Spike(-3650, -1070), 
Spike(-3700, -1070), Spike(-3750, -1070), Spike(-3800, -1070), Spike(-3850, -1070), Spike(-3900, -1070), Spike(-3950, -1070), Spike(-4000, -1070), 
Spike(-4200, -630), Spike(-4625, -990), Spike(-5250, -990), Spike(-5300, -990), Spike(-5350, -990), Spike(-5400, -990), Spike(-5450, -990), Spike(-5500, -990),
Spike(-5550, -990), Spike(-5600, -990), Spike(-5650, -990), Spike(-5700, -990), Spike(-5750, -990), Spike(-5800, -990), Spike(-5850, -990), Spike(-5900, -990),
Spike(-5950, -990), Spike(-6000, -990), Spike(-5475, -600), Spike(-5525, -600), Spike(-5575, -600), Spike(-5835, -720), Spike(-5885, -720),Spike(-5935, -720), 
Spike(-5985, -720), Spike(-6035, -720)]
