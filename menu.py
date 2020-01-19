import pygame as pg
import math
import os
from settings import *

game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder,"assets")
font = os.path.join(assets_folder,"PixelEmulator-xq08.ttf")

money = 10500
model_time=0
agile_iter = 1
agile_initial = 1
time_available = 0
coder_count = 1
tester_count = 1 
bugs_number = 0
model_selected = 0
project = []
def text_format(message, textFont, textSize, textColor):
        newFont=pg.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)
    
        return newText

def menu_background(surf,game, x, y):
    image = game.spritesheet.get_image(57,91,112,32)
    #text_surface.fill(BLACK)
    image = pg.transform.scale(image,(1008,576))
    image.set_colorkey(BLACK)
    text_rect = image.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(image,text_rect)

def hud_background(surf,game, x, y):
    image = game.spritesheet.get_image(72,1,92,77)
    #text_surface.fill(BLACK)
    image = pg.transform.scale(image,(184,77))
    image.set_colorkey(BLACK)
    text_rect = image.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(image,text_rect)

def hud_background_cover(surf,game, x, y):
    image = game.spritesheet.get_image(491,40,14,15)
    #text_surface.fill(BLACK)
    image = pg.transform.scale(image,(162,69))
    image.set_colorkey(BLACK)
    text_rect = image.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(image,text_rect)

def hud(surf,game):
    global money
    title = text_format("$" + str(money), font, 25, orange)
    dev = text_format("C:" + str(game.coder_count) + "  T:" + str(game.tester_count), font, 25, orange)
    surf.blit(title, (1100, 20))
    surf.blit(dev, (1100, 45))
    
def menu_vendor(surf,game,x,y):
    isMenu = True
    global project
    project = random.randrange(0,len(PROJECT_LIST)-1)
    company = random.randrange(0,len(COMPANY_LIST)-1)
    global model_time
    global time_available
    selected = "ACCEPT"
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="ACCEPT"
                elif event.key==pg.K_DOWN:
                    selected="DECLINE"
                if event.key==pg.K_RETURN:
                    if selected=="ACCEPT":
                        print(selected)
                        isMenu = False
                        menu_model(surf,game,x,y)
                        return
                    if selected=="DECLINE":
                        isMenu = False
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        model_time = PROJECT_LIST[project][2]
        time_available = model_time
        title=text_format(PROJECT_LIST[project][0], font, 30, BLACK)
        company_name = text_format(COMPANY_LIST[company][0], font, 20, BLACK)
        description = text_format(PROJECT_LIST[project][1], font, 20, BLACK)
        duration = text_format(str(PROJECT_LIST[project][2]) + " days", font, 20, BLACK)

        if selected=="ACCEPT":
            accept=text_format("ACCEPT", font, 30, yellow)
        else:
            accept = text_format("ACCEPT", font, 30, BLACK)

        if selected=="DECLINE":
            decline= text_format("DECLINE", font, 30, yellow)
        else:
            decline = text_format("DECLINE", font, 30, BLACK)

        title_rect=title.get_rect()
        company_name_rect = company_name.get_rect()
        description_rect = description.get_rect()
        duration_rect = duration.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()

        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(company_name, (WIDTH/2 - (company_name_rect[2]/2), 110))
        surf.blit(description, (WIDTH/2 - (description_rect[2]/2), 170))
        surf.blit(duration, (WIDTH/2 - (duration_rect[2]/2), 200))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()
        
def menu_model(surf,game,x,y):
    isMenu = True
    selected = "Ad-hoc"
    model_count=0
    global time_available, model_selected
    global model_time
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    if model_count!=0:
                        model_count = model_count - 1
                elif event.key==pg.K_DOWN:
                    if model_count!=2:
                        model_count = model_count + 1
                if model_count==0:
                    selected="Ad-hoc"
                elif model_count==1:
                    selected="Waterfall"
                else:
                    selected="Agile"
                if event.key==pg.K_RETURN:
                    if selected=="Ad-hoc":
                        print(selected)
                        isMenu = False
                        model_selected = 1
                        menu_adhoc_code(surf,game,x,y)
                        return
                    if selected=="Waterfall":
                        isMenu = False
                        model_selected = 2
                        menu_waterfall_design(surf,game,x,y)
                        return
                    if selected=="Agile":
                        isMenu=False
                        model_selected = 3
                        menu_agile_design1(surf,game,x,y)
                        return
        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)

        if selected=="Ad-hoc":
            adhoc = text_format("Ad-hoc", font, 30, yellow)
        else:
            adhoc = text_format("Ad-hoc", font, 30, BLACK)

        if selected=="Waterfall":
            waterfall= text_format("Waterfall", font, 30, yellow)
        else:
            waterfall = text_format("Waterfall", font, 30, BLACK)
        
        if selected=="Agile":
            agile = text_format("Agile", font, 30, yellow)
        else:
            agile = text_format("Agile", font, 30, BLACK)
        
        title=text_format("Select a SDLC Model", font, 30, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title_rect=title.get_rect()
        adhoc_rect = adhoc.get_rect()
        waterfall_rect = waterfall.get_rect()
        agile_rect = agile.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(adhoc, (WIDTH/2 - (adhoc_rect[2]/2), 260))
        surf.blit(waterfall, (WIDTH/2 - (waterfall_rect[2]/2), 290))
        surf.blit(agile, (WIDTH/2 - (agile_rect[2]/2), 320))

        pg.display.update()

def menu_adhoc_code(surf,game,x,y):
    isMenu = True
    selected = 1
    global time_available
    global coder_count
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    if selected<game.coder_count:
                        selected = selected + 1
                        coder_count = selected
                elif event.key==pg.K_DOWN:
                    if selected>1:
                        selected = selected - 1
                        coder_count = selected
                if event.key==pg.K_RETURN:
                    isMenu = False
                    menu_adhoc_test(surf,game,x,y)
                    return
        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        count = text_format(str(selected), font, 30, yellow)
        title=text_format("Select number of coders", font, 30, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title_rect=title.get_rect()
        count_rect = count.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(count, (WIDTH/2 - (count_rect[2]/2), 260))
        pg.display.update()

def menu_adhoc_test(surf,game,x,y):
    isMenu = True
    selected = 1
    global coder_count
    global time_available
    global model_time
    global tester_count
    global bugs_number
    time_available = time_available - math.floor(0.3 * model_time / coder_count)
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    if selected<game.tester_count:
                        selected = selected + 1
                        tester_count = selected
                elif event.key==pg.K_DOWN:
                    if selected>1:
                        selected = selected - 1
                        tester_count = selected
                if event.key==pg.K_RETURN:
                    isMenu = False
                    bugs_number = 10
                    time_available = time_available - math.floor(0.2 * model_time / tester_count)
                    menu_adhoc_debug(surf,game,x,y)
                    return
        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        count = text_format(str(selected), font, 30, yellow)
        title=text_format("Select number of testers", font, 30, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title_rect=title.get_rect()
        count_rect = count.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(count, (WIDTH/2 - (count_rect[2]/2), 260))
        pg.display.update()

def menu_adhoc_debug(surf,game,x,y):
    isMenu = True
    global coder_count
    global time_available
    global model_time
    global tester_count
    global bugs_number
    if bugs_number != 0:
        bugs_number = random.randrange(0,bugs_number)
    store = ""
    if bugs_number != 0:
        store = str(bugs_number)
    else:
        store = "No"
    selected = "DON'T DEBUG"
    print(tester_count)
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="DON'T DEBUG"
                elif event.key==pg.K_DOWN:
                    selected="DEBUG"
                if event.key==pg.K_RETURN:
                    if selected=="DON'T DEBUG":
                        print(selected)
                        isMenu = False
                        menu_deploy(surf,game,x,y)
                        return
                    if selected=="DEBUG":
                        isMenu = False
                        time_available = time_available - math.ceil(0.02 * model_time * bugs_number /(coder_count + tester_count))
                        menu_adhoc_debug(surf,game,x,y)
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title1 = text_format(store + " bugs found!!!", font, 30, BLACK)
        title=text_format("Do you want to debug?", font, 30, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        title1_rect = title1.get_rect()
        time_rect = time.get_rect()
        if selected=="DON'T DEBUG":
            accept=text_format("DON'T DEBUG", font, 30, yellow)
        else:
            accept = text_format("DON'T DEBUG", font, 30, BLACK)

        if selected=="DEBUG":
            decline= text_format("DEBUG", font, 30, yellow)
        else:
            decline = text_format("DEBUG", font, 30, BLACK)

        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 80))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 120))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()

def menu_deploy(surf,game,x,y):
    isMenu = True
    selected = "DEPLOY"
    global time_available
    global model_time
    required = math.floor(0.4*model_time)
    if time_available < required:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="DEPLOY"
                elif event.key==pg.K_DOWN:
                    selected="DON'T DEPLOY"
                if event.key==pg.K_RETURN:
                    if selected=="DEPLOY":
                        print(selected)
                        isMenu = False
                        menu_report(surf,game,x,y)
                        return
                    if selected=="DON'T DEPLOY":
                        isMenu = False
                        menu_adhoc_try_again(surf,game,x,y)
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title=text_format("Do you want to deploy?", font, 30, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        time1 = text_format("Time required : "+str(required)+" days", font, 20, red)
        time1_rect = time1.get_rect()
        if selected=="DEPLOY":
            accept=text_format("DEPLOY", font, 30, yellow)
        else:
            accept = text_format("DEPLOY", font, 30, BLACK)

        if selected=="DON'T DEPLOY":
            decline= text_format("DON'T DEPLOY", font, 30, yellow)
        else:
            decline = text_format("DON'T DEPLOY", font, 30, BLACK)

        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(time1, (WIDTH/2 - (time1_rect[2]/2), 70))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 110))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()

def menu_adhoc_try_again(surf,game,x,y):
    isMenu = True
    selected = "TRY AGAIN"
    global time_available
    global tester_count,coder_count
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="TRY AGAIN"
                elif event.key==pg.K_DOWN:
                    selected="REJECT PROJECT"
                if event.key==pg.K_RETURN:
                    if selected=="TRY AGAIN":
                        print(selected)
                        isMenu = False
                        time_available = model_time
                        coder_count = 1
                        tester_count = 1
                        menu_model(surf,game,x,y)
                        return
                    if selected=="REJECT PROJECT":
                        isMenu = False
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title=text_format("Do you want to retry?", font, 30, BLACK)

        if selected=="TRY AGAIN":
            accept=text_format("TRY AGAIN", font, 30, yellow)
        else:
            accept = text_format("TRY AGAIN", font, 30, BLACK)

        if selected=="REJECT PROJECT":
            decline= text_format("REJECT PROJECT", font, 30, yellow)
        else:
            decline = text_format("REJECT PROJECT", font, 30, BLACK)

        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()

        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()
                
def menu_waterfall_design(surf,game,x,y):
    isMenu = True
    selected = "OK"
    global time_available
    time_available = time_available - math.floor(0.1 * model_time)
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                
                if event.key==pg.K_RETURN:
                    if selected=="OK":
                        print(selected)
                        isMenu = False
                        menu_waterfall_code(surf,game,x,y)
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title=text_format("Design process completed", font, 30, BLACK)
        title1 = text_format("Class and Sequence diagrams generated", font, 30, BLACK)
        if selected=="OK":
            accept=text_format("OK", font, 30, yellow)
      

        title_rect=title.get_rect()
        title1_rect = title1.get_rect()
        accept_rect = accept.get_rect()

        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 180))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 290))

        pg.display.update()
                

def menu_waterfall_code(surf,game,x,y):
    isMenu = True
    selected = 1
    global time_available,coder_count
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    if selected<game.coder_count:
                        coder_count += 1
                        selected = selected + 1
                elif event.key==pg.K_DOWN:
                    if selected>1:
                        coder_count -= 1
                        selected = selected - 1
                if event.key==pg.K_RETURN:
                    isMenu = False
                    menu_waterfall_test(surf,game,x,y)
                    return
        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        count = text_format(str(selected), font, 30, yellow)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title=text_format("Select number of coders", font, 30, BLACK)
        title_rect=title.get_rect()
        count_rect = count.get_rect()
        
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(count, (WIDTH/2 - (count_rect[2]/2), 260))
        pg.display.update()

def menu_waterfall_test(surf,game,x,y):
    isMenu = True
    selected = 1
    global time_available
    global coder_count,model_time,tester_count, bugs_number
    time_available = time_available - math.floor(0.3 * model_time/coder_count)
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    if selected<game.tester_count:
                        tester_count += 1
                        selected = selected + 1
                elif event.key==pg.K_DOWN:
                    if selected>1:
                        tester_count -= 1
                        selected = selected - 1
                if event.key==pg.K_RETURN:
                    isMenu = False
                    bugs_number=7
                    time_available = time_available - math.floor(0.2 * model_time/tester_count)
                    menu_waterfall_debug(surf,game,x,y)
                    return
        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        count = text_format(str(selected), font, 30, yellow)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title=text_format("Select number of testers", font, 30, BLACK)
        title_rect=title.get_rect()
        count_rect = count.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(count, (WIDTH/2 - (count_rect[2]/2), 260))
        pg.display.update()

def menu_waterfall_debug(surf,game,x,y):
    isMenu = True
    selected = "DON'T DEBUG"
    global time_available,tester_count
    global bugs_number
    if bugs_number != 0:
        bugs_number = random.randrange(0,bugs_number)
    store = ""
    if bugs_number != 0:
        store = str(bugs_number)
    else:
        store = "No"
    selected = "DON'T DEBUG"
    print(tester_count)
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="DON'T DEBUG"
                elif event.key==pg.K_DOWN:
                    selected="DEBUG"
                if event.key==pg.K_RETURN:
                    if selected=="DON'T DEBUG":
                        print(selected)
                        isMenu = False
                        menu_option_btesting(surf,game,x,y)
                        return
                    if selected=="DEBUG":
                        isMenu = False
                        time_available = time_available - math.ceil(0.02 * model_time * bugs_number /(coder_count + tester_count))
                        print(0.02 * model_time * bugs_number /(coder_count + tester_count))
                        menu_waterfall_debug(surf,game,x,y)
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title1 = text_format(store + " bugs found!!!", font, 30, BLACK)
        title=text_format("Do you want to debug?", font, 30, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        if selected=="DON'T DEBUG":
            accept=text_format("DON'T DEBUG", font, 30, yellow)
        else:
            accept = text_format("DON'T DEBUG", font, 30, BLACK)

        if selected=="DEBUG":
            decline= text_format("DEBUG", font, 30, yellow)
        else:
            decline = text_format("DEBUG", font, 30, BLACK)

        title1_rect = title1.get_rect()
        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()

        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 80))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 120))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()

def menu_option_btesting(surf,game,x,y):
    isMenu = True
    selected = "YES"
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="YES"
                elif event.key==pg.K_DOWN:
                    selected="NO"
                if event.key==pg.K_RETURN:
                    if selected=="YES":
                        print(selected)
                        isMenu = False
                        menu_btesting(surf,game,x,y)
                        return
                    if selected=="NO":
                        isMenu = False
                        menu_deploy(surf,game,x,y)
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title=text_format("Do you want to perform beta testing?", font, 30, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()

        if selected=="YES":
            accept=text_format("YES", font, 30, yellow)
        else:
            accept = text_format("YES", font, 30, BLACK)

        if selected=="NO":
            decline= text_format("NO", font, 30, yellow)
        else:
            decline = text_format("NO", font, 30, BLACK)

        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()

        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()

def menu_btesting(surf,game,x,y):
    isMenu = True
    selected = "DON'T DEBUG"
    global time_available
    time_available = time_available - 3
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="DON'T DEBUG"
                elif event.key==pg.K_DOWN:
                    selected="DEBUG"
                if event.key==pg.K_RETURN:
                    if selected=="DON'T DEBUG":
                        print(selected)
                        isMenu = False
                        menu_deploy(surf,game,x,y)
                        return
                    if selected=="DEBUG":
                        isMenu = False
                        menu_beta_debug(surf,game,x,y)
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title1 = text_format("Some bugs have been found during beta testing?", font, 20, BLACK)
        title=text_format("Do you want to debug?", font, 30, BLACK)

        if selected=="DON'T DEBUG":
            accept=text_format("DON'T DEBUG", font, 30, yellow)
        else:
            accept = text_format("DON'T DEBUG", font, 30, BLACK)

        if selected=="DEBUG":
            decline= text_format("DEBUG", font, 30, yellow)
        else:
            decline = text_format("DEBUG", font, 30, BLACK)
        title1_rect = title1.get_rect()
        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 80))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 120))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()

def menu_beta_debug(surf,game,x,y):
    isMenu = True
    selected = "OK"
    global time_available
    time_available = time_available - random.randrange(0,4)
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                
                if event.key==pg.K_RETURN:
                    if selected=="OK":
                        print(selected)
                        isMenu = False
                        menu_deploy(surf,game,x,y)
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title=text_format("Debug process complete", font, 30, BLACK)
        title1 = text_format("Press Enter to continue to deployment", font, 30, BLACK)
        if selected=="OK":
            accept=text_format("OK", font, 30, yellow)
      

        title_rect=title.get_rect()
        title1_rect = title1.get_rect()
        accept_rect = accept.get_rect()

        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 180))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 290))

        pg.display.update()

def menu_agile_design1(surf,game,x,y):
    isMenu = True
    selected = 1
    global agile_iter
    global agile_initial
    global time_available
    global model_time
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    if selected<5:
                        selected = selected + 1
                        agile_iter = agile_iter + 1
                        agile_initial = agile_initial + 1
                elif event.key==pg.K_DOWN:
                    if selected>1:
                        selected = selected - 1
                        agile_iter = agile_iter - 1
                        agile_initial = agile_initial - 1
                if event.key==pg.K_RETURN:
                    isMenu = False
                    time_available -= math.ceil(0.1 * model_time)
                    menu_agile_code(surf,game,x,y)
                    return
        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        count = text_format(str(selected), font, 30, yellow)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title=text_format("Select number of scrums to divide the project", font, 20, BLACK)
        title_rect=title.get_rect()
        count_rect = count.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(count, (WIDTH/2 - (count_rect[2]/2), 260))
        pg.display.update()

def menu_agile_code(surf,game,x,y):
    isMenu = True
    selected = 1
    global time_available, coder_count
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    if selected<game.coder_count:
                        selected = selected + 1
                        coder_count += 1
                elif event.key==pg.K_DOWN:
                    if selected>1:
                        selected = selected - 1
                        coder_count -= selected
                if event.key==pg.K_RETURN:
                    isMenu = False
                    menu_agile_review(surf,game,x,y)
                    return
        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        count = text_format(str(selected), font, 30, yellow)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title=text_format("Select number of coders", font, 30, BLACK)
        title_rect=title.get_rect()
        count_rect = count.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(count, (WIDTH/2 - (count_rect[2]/2), 260))
        pg.display.update()

def menu_agile_review(surf,game,x,y):
    isMenu = True
    selected = "YES"
    global agile_iter
    global agile_initial, time_available, coder_count, model_time
    time_available -= math.floor(0.3 * model_time / (coder_count * agile_initial))
    print("hello " + str(agile_initial))
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="YES"
                elif event.key==pg.K_DOWN:
                    selected="NO"
                if event.key==pg.K_RETURN:
                    if selected=="YES":
                        print(selected)
                        isMenu = False
                        menu_agile_response(surf,game,x,y)
                        return
                    if selected=="NO":
                        isMenu = False
                        if agile_iter != agile_initial and agile_initial != 1:
                            menu_agile_test(surf, game, x, y)
                        else:
                            agile_iter = agile_iter - 1
                            menu_agile_code(surf, game, x, y)
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title1 = text_format("Unit testing completed", font, 20, BLACK)
        title=text_format("Do you want to take customer review?", font, 30, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        if selected=="YES":
            accept=text_format("YES", font, 30, yellow)
        else:
            accept = text_format("YES", font, 30, BLACK)

        if selected=="NO":
            decline= text_format("NO", font, 30, yellow)
        else:
            decline = text_format("NO", font, 30, BLACK)
        title1_rect = title1.get_rect()
        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()
        surf.blit(time, (WIDTH/2 - (time_rect[2]/2), 40))
        surf.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 80))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 120))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()



def menu_agile_response(surf,game,x,y):
    isMenu = True
    selected = "OK"
    global agile_iter
    global agile_initial, time_available, model_time
    time_available -= math.floor(0.1 * model_time)
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                
                if event.key==pg.K_RETURN:
                    if selected=="OK":
                        print(selected)
                        isMenu = False
                        if agile_initial != agile_iter and agile_initial != 1:
                            menu_agile_test(surf, game, x, y)
                        else:
                            agile_iter = agile_iter - 1
                            menu_agile_code(surf, game, x, y)
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title=text_format("Customer gave some suggestions", font, 20, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title1 = text_format("Implement these changes during next scrum", font, 20, BLACK)
        if selected=="OK":
            accept=text_format("OK", font, 30, yellow)
      

        title_rect=title.get_rect()
        title1_rect = title1.get_rect()
        accept_rect = accept.get_rect()
        surf.blit(time, (WIDTH/2 - (title_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 180))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 290))

        pg.display.update()


def menu_agile_test(surf,game,x,y):
    isMenu = True
    selected = 1
    global agile_iter
    global agile_initial, time_available, model_time
    time_available -= math.floor(0.2 * model_time / agile_initial)
    if time_available < 0:
        menu_failure(surf,game,x,y)
        return
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    if selected<game.tester_count:
                        selected = selected + 1
                elif event.key==pg.K_DOWN:
                    if selected>1:
                        selected = selected - 1
                if event.key==pg.K_RETURN:
                    isMenu = False
                    if agile_iter > 1:
                        agile_iter  = agile_iter - 1
                        menu_agile_code(surf, game, x, y)
                    else:
                        menu_option_btesting(surf, game, x, y)
                    return
        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        count = text_format(str(selected), font, 30, yellow)
        title=text_format("Select number of testers for integration testing", font, 20, BLACK)
        time = text_format("Time available : "+str(time_available)+" days", font, 20, red)
        time_rect = time.get_rect()
        title_rect=title.get_rect()
        count_rect = count.get_rect()
        surf.blit(time, (WIDTH/2 - (title_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(count, (WIDTH/2 - (count_rect[2]/2), 260))
        pg.display.update()

def menu_failure(surf,game,x,y):
    isMenu = True
    selected = "TRY AGAIN"
    global time_available
    global tester_count,coder_count
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="TRY AGAIN"
                elif event.key==pg.K_DOWN:
                    selected="REJECT PROJECT"
                if event.key==pg.K_RETURN:
                    if selected=="TRY AGAIN":
                        print(selected)
                        isMenu = False
                        time_available = model_time
                        coder_count = 1
                        tester_count = 1
                        menu_model(surf,game,x,y)
                        return
                    if selected=="REJECT PROJECT":
                        isMenu = False
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title1=text_format("You don't have enough time!!", font, 30, BLACK)
        title=text_format("Do you want to retry?", font, 30, BLACK)

        if selected=="TRY AGAIN":
            accept=text_format("TRY AGAIN", font, 30, yellow)
        else:
            accept = text_format("TRY AGAIN", font, 30, BLACK)

        if selected=="REJECT PROJECT":
            decline= text_format("REJECT PROJECT", font, 30, yellow)
        else:
            decline = text_format("REJECT PROJECT", font, 30, BLACK)
        title1_rect=title1.get_rect()
        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()

        surf.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 40))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()    

def menu_report(surf,game,x,y):
    isMenu = True
    selected = "OK"
    global money,bugs_number, project
    addition = 0
    rating = 0
    if PROJECT_LIST[project][4][0] == model_selected:
        addition = 5
    elif PROJECT_LIST[project][4][1] == model_selected:
        addition = 3
    else:
        addition = 1
    if bugs_number <= 4:
        rating = addition + 5 - bugs_number
    else:
        rating = addition
    credit = random.randrange(7,12) * model_time - random.randrange(1,10) * bugs_number + addition * model_time
    money += credit
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                
                if event.key==pg.K_RETURN:
                    if selected=="OK":
                        print(selected)
                        isMenu = False
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title=text_format("Project successfully completed!!", font, 20, BLACK)
        title1=text_format("Number of bugs: " + str(bugs_number), font, 20, BLACK)
        title3=text_format("Project rating : " + str(rating) + " / 10", font, 20, BLACK)
        title2=text_format("Money Credited $" + str(credit), font, 20, BLACK)
        if selected=="OK":
            accept=text_format("OK", font, 30, yellow)
      
        title_rect=title.get_rect()
        title1_rect=title1.get_rect()
        title2_rect=title2.get_rect()
        title3_rect = title3.get_rect()
        accept_rect = accept.get_rect()
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 120))
        surf.blit(title3, (WIDTH/2 - (title3_rect[2]/2), 160))
        surf.blit(title2, (WIDTH/2 - (title2_rect[2]/2), 200))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 290))

        pg.display.update()

def menu_shop(surf,game,x,y):
    isMenu = True
    selected = "CODER"
    global time_available,money
    tester_val = (35 * game.tester_count)** 2
    coder_val = (30 * game.coder_count)** 2
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.key==pg.K_UP:
                    selected="CODER"
                elif event.key==pg.K_DOWN:
                    selected="TESTER"
                elif event.key==pg.K_ESCAPE:
                    return
                if event.key==pg.K_RETURN:
                    if selected=="CODER":
                        print(selected)
                        isMenu = False
                        if money < coder_val:
                            menu_recipt(surf,game,x,y,"Insufficient Funds")
                            return
                        money -= coder_val
                        game.coder_count += 1
                        menu_recipt(surf,game,x,y,"Purchase Successful ")
                        return
                    if selected=="TESTER":
                        isMenu = False
                        if money < tester_val:
                            menu_recipt(surf,game,x,y,"Insufficient Funds")
                            return
                        money -= tester_val
                        game.tester_count += 1
                        menu_recipt(surf,game,x,y,"Purchase Successful ")
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title=text_format("Who do you want to buy?", font, 30, BLACK)

        if selected=="CODER":
            accept=text_format("CODER  $" + str(coder_val), font, 30, yellow)
        else:
            accept = text_format("CODER  $" + str(coder_val), font, 30, BLACK)

        if selected=="TESTER":
            decline= text_format("TESTER  $" + str(tester_val), font, 30, yellow)
        else:
            decline = text_format("TESTER  $" + str(tester_val), font, 30, BLACK)
        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        decline_rect = decline.get_rect()

        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 260))
        surf.blit(decline, (WIDTH/2 - (decline_rect[2]/2), 290))

        pg.display.update()

def menu_recipt(surf,game,x,y,res):
    isMenu = True
    selected = "OK"
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                
                if event.key==pg.K_RETURN:
                    if selected=="OK":
                        print(selected)
                        isMenu = False
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title=text_format(res, font, 30, BLACK)
        if selected=="OK":
            accept=text_format("OK", font, 30, yellow)
      
        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 290))

        pg.display.update()

def menu_tutorial(surf,game,x,y):
    isMenu = True
    selected = "OK"
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                
                if event.key==pg.K_RETURN:
                    if selected=="OK":
                        print(selected)
                        isMenu = False
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title=text_format("Go to your office for ", font, 30, BLACK)
        title2 = text_format("developing softwares and contact the", font, 30, BLACK)
        title3 = text_format(" vendor for hiring more developers.", font, 30, BLACK)
        if selected=="OK":
            accept=text_format("OK", font, 30, yellow)
      
        title_rect=title.get_rect()
        title2_rect=title2.get_rect()
        title3_rect=title3.get_rect()
        accept_rect = accept.get_rect()
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(title2, (WIDTH/2 - (title2_rect[2]/2), 120))
        surf.blit(title3, (WIDTH/2 - (title3_rect[2]/2), 160))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 290))

        pg.display.update()

def menu_intro(surf,game,x,y):
    isMenu = True
    selected = "OK"
    while isMenu:
        for event in pg.event.get(): 
            if event.type==pg.KEYDOWN:
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                
                if event.key==pg.K_RETURN:
                    if selected=="OK":
                        print(selected)
                        isMenu = False
                        return

        pg.time.Clock().tick(FPS)
        menu_background(surf,game,x,y)
        title2 = text_format("GETTING STARTED:-", font, 30, BLACK)
        title=text_format("Find an old man under a tree.", font, 30, BLACK)
        if selected=="OK":
            accept=text_format("OK", font, 30, yellow)

        title2_rect=title2.get_rect()
        title_rect=title.get_rect()
        accept_rect = accept.get_rect()
        surf.blit(title2, (WIDTH/2 - (title_rect[2]/2), 80))
        surf.blit(title, (WIDTH/2 - (title_rect[2]/2), 160))
        surf.blit(accept, (WIDTH/2 - (accept_rect[2]/2), 290))

        pg.display.update()