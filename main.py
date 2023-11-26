from collections import defaultdict
import time
import pygame
import math
import sys
import json

def smooth_transition(i, num_elements):
    return int(127.5 * (1 + math.cos(math.radians(i * (360 / num_elements)))))

def converge():
    global is_heading_back
    #print(convergiant_times)
    try:
        number_up_to = min(convergiant_times)
    except:
        is_heading_back = True   
        return
    #print(number_up_to)
    for row, col in convergiant_times[number_up_to]:
        #print(row, col)
        if (not path[row][col]) or path[row][col] == 's':
            path[row][col] = number_up_to
            for i, j in directional_map[row][col]:
                try:
                    if path[i][j] == 'e':
                        heading_back.append(i, j)
                        is_heading_back = True                            
                    if not path[i][j]:
                        convergiant_times[number_up_to + mapp[i][j]].append((i, j))
                except:
                    pass
    convergiant_times.pop(number_up_to)

def reversing():
    row, col = heading_back[-1]
    min_val_so_far = 100000
    #print(min_val_so_far)
    for i in range(row-1, row+2):
        if -1 < i < map_size:
            for j in range(col-1, col+2):
                if -1 < j < map_size:
                    if i != row and j != col:
                        continue
                    if path[i][j] == 'e' or not path[i][j]:
                        continue
                    if path[i][j] == 's':
                        heading_back.append((i, j))
                        path_is_complete = True
                        return
                    #print(path[i][j], min_val_so_far)
                    if path[i][j] < min_val_so_far:
                        min_val_so_far = path[i][j]
                        next_head_back = (i, j)
    heading_back.append(next_head_back)
            


#pygame code
def boiler():
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        window.fill((173, 216, 230))
        draw_maxtrix()
        pygame.display.update()

def draw_maxtrix():
        for i, row in enumerate(path):
            for j, col in enumerate(row):
                if path[i][j] == 'e':
                    pygame.draw.rect(window, (0, 0, 255), pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))
                elif path[i][j] == 's':
                    pygame.draw.rect(window, (100, 0, 100), pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))
                elif col:
                    #print(i, j, col)
                    pygame.draw.rect(window, colors[col%len(colors)], pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))
                if (i, j) in heading_back:
                    pygame.draw.rect(window, (0, 255, 0), pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))

                if directional_map_2[i][j]:
                    val = directional_map_2[i][j]
                    for dr in val:
                        window.blit(arrows[dr], (pixel_size_x * j, pixel_size_y * i))

                if other_image_map[i][j]:
                    val = other_image_map[i][j]
                    for image in val:
                        window.blit(images[image], (pixel_size_x * j, pixel_size_y * i))
                
                if mapp[i][j] == 4:
                    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(pixel_size_x * (j + .2), pixel_size_y * (i + .2), pixel_size_x*6/10, pixel_size_y*6/10))
                if mapp[i][j] == 1:
                    pygame.draw.rect(window, (255, 0, 40), pygame.Rect(pixel_size_x * (j + .2), pixel_size_y * (i + .2), pixel_size_x*6/10, pixel_size_y*6/10))

map_size = 30
if len(sys.argv) > 1:
    map_size = int(sys.argv[1])
mapp = [[2] * map_size for i in range(map_size)]
directional_map = [[[] for j in range(map_size)] for i in range(map_size)]
directional_map_2 = [[[] for j in range(map_size)] for i in range(map_size)]
other_image_map = [[[] for j in range(map_size)] for i in range(map_size)]

for i in range(map_size-1):
    directional_map[i][0].append((i + 1, 0))
    directional_map[-1][i].append((-1, i + 1))
    directional_map_2[i][0].append('down')
    directional_map_2[-1][i].append('right')

path_is_complete = False
path = [[0] * map_size for i in range(map_size)]
# number_up_to = 0
convergiant_times = defaultdict(list)
convergiant_times[0].append((0, 0))
is_heading_back = False
heading_back = [(map_size-1, map_size-1)]
#pygame code
pygame.init()
clock = pygame.time.Clock()
width, height = 800, 800
pixel_size_x, pixel_size_y = width//len(mapp[0]), height//len(mapp)
window = pygame.display.set_mode((width, height))
up_to_building_number = 1

num_elements = map_size*4
colors = [(smooth_transition(i, num_elements), smooth_transition(2*i, num_elements), smooth_transition(4*i, num_elements)) for i in range(num_elements)]

arrows = {dr: pygame.transform.scale(pygame.image.load(f'assets/{dr}_arrow.png'), (pixel_size_x, pixel_size_y)) for dr in ['left', 'down', 'right', 'up']}
images = {image: pygame.transform.scale(pygame.image.load(f'assets/{image}.png'), (pixel_size_x * 2, pixel_size_y * 2)) for image in ['tree', 'grass', 'house']}
images.update({f"building{i}": pygame.transform.scale(pygame.image.load(f'assets/building{i}.png'), (pixel_size_x * 10, pixel_size_y * 10)) for i in range(1, 9)})




mapp[0][0] = 0
path[0][0] = 's'
path[-1][-1] = 'e'

while True:
    boiler()

    mx, my = pygame.mouse.get_pos()
    row, col = my//pixel_size_y, mx//pixel_size_x

    keys = pygame.key.get_pressed()

    if keys[pygame.K_s]:
        directional_map_2[row][col].append('down')
        directional_map[row][col].append((row+1, col))
    if keys[pygame.K_d]:
         directional_map_2[row][col].append('right')
         directional_map[row][col].append((row, col+1))
    if keys[pygame.K_w]:
        directional_map_2[row][col].append('up')
        directional_map[row][col].append((row-1, col))
    if keys[pygame.K_a]:
         directional_map_2[row][col].append('left')
         directional_map[row][col].append((row, col-1))

    if keys[pygame.K_t]:
         other_image_map[row][col].append('tree')
    if keys[pygame.K_h]:
         other_image_map[row][col].append('house')
    if keys[pygame.K_g]:
         other_image_map[row][col].append('grass')
    if keys[pygame.K_b]:
         other_image_map[row][col].append(f'building{up_to_building_number}')
         up_to_building_number += 1
         time.sleep(.2)

    if keys[pygame.K_x]:
        with open('save_map.txt', 'w') as file:
            file.write(json.dumps({'1': directional_map, '2': directional_map_2, '3': other_image_map}))
        
    if keys[pygame.K_y]:
        with open('save_map.txt', 'r') as file:
            dictionary = json.loads(file.read())
            directional_map, directional_map_2, other_image_map = (dictionary[i] for i in dictionary)
      

    if pygame.mouse.get_pressed()[0]:
        mapp[row][col] = 4

    if keys[pygame.K_f]:
        mapp[row][col] = 1
    
    if keys[pygame.K_SPACE]:
        break

while True:
    clock.tick(map_size//2)
    print('path: ', path)
    # display(path)
    boiler()
    if is_heading_back:
        #print('heading back')
        reversing()
    else:
        #print('converging')
        converge()