import random

#constants
WIDTH = 1280
HEIGHT = 720
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)
orange = (255,165,0)
SPEED = 5
TITLE = "SE game"
TILESIZE = 48
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE
SPRITESHEET = "spritesheet.png"
MAP = "main_map.txt"
PLAYER_SPEED = 220

# Projects

# project name, description, time limit(day), base reputation, methods, bonus

PROJECT_LIST = [
    ["Complaint Registration Portal","Register some complaint",50,random.randrange(5,20),[1,2,3],False],
    ["Voice Prescription","Provide voice prescription",55,random.randrange(5,20),[3,2,1],False],
    ["Spacecraft electricity optimizer","Reduce the energy consumed by rockets",60,random.randrange(20,65),[2,3,1],False],
    ["Electic vehicle ecosystem","Make the vehicles talk",60,random.randrange(65,80),[3,2,1],False]
]

# Company list

COMPANY_LIST = [
    ["TESCO",5],
    ["ISRO",20],
    ["DRDO",20],
    ["Tesla",15],
    ["Release my add",0],
    ["Gnani",0]
]