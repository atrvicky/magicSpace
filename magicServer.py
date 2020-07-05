import pygame, time
import paho.mqtt.client as mqtt


pygame.init()

pygame.display.set_caption(u'Magic Server')

pygame.display.set_mode((600, 600), pygame.RESIZABLE)

mqttc = mqtt.Client()
mqttc.username_pw_set(username="magicSpace", password="magicspace")
mqttc.connect("192.168.0.105")
#mqttc.loop_start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            print(type(pos))
            pos = str(pos[0]) + '$' + str(pos[1])
            mqttc.publish('magicSpaceMousePos', pos, qos=0)
            #mqttc.publish('magicSpaceMouseY', str(pos[1]), qos=0)
            print (pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('mouse click')
            mqttc.publish('magicSpaceMouse', str(1), qos=0)
            #pygame.quit()
            
        elif event.type == pygame.MOUSEBUTTONUP:
            print('mouse click release')
            mqttc.publish('magicSpaceMouse', str(0), qos=0)
            
        elif event.type == pygame.KEYDOWN:
            keystroke = pygame.key.get_pressed()
            print(keystroke)
            mqttc.publish('magicSpace', keystroke, qos=0)
    
    
pygame.quit()