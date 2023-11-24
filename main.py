from collections import defaultdict
import time
import pygame

def display(two_d_array):
    for row in two_d_array:
        #print('\n' + '-'*60, end = '\n| ')
        for col in row:
            #print(str(col).center(3), end = ' | ')
            pass
    #print('\n' + '-'*60)

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
        window.fill('black')
        draw_maxtrix()
        pygame.display.update()

def draw_maxtrix():
        for i, row in enumerate(path):
            for j, col in enumerate(row):
                if path[i][j] == 'e':
                    pygame.draw.rect(window, (0, 0, 255), pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))
                elif path[i][j] == 's':
                    pygame.draw.rect(window, (100, 0, 100), pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))
                else:
                    #print(i, j, col)
                    pygame.draw.rect(window, colors[col%len(colors)], pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))
                if directional_map_2[i][j]:
                    val = directional_map_2[i][j]
                    if 's' in val:
                        pygame.draw.rect(window, (255, 255, 0), pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))
                    if 'd' in val:
                        pygame.draw.rect(window, (255, 0, 255), pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))
                if (i, j) in heading_back:
                    pygame.draw.rect(window, (0, 255, 0), pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))

                if mapp[i][j] == 2:
                    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(pixel_size_x * (j + .2), pixel_size_y * (i + .2), pixel_size_x*6/10, pixel_size_y*6/10))

                

                # pygame.draw.rect(window, colors[(col-1)%len(colors)], pygame.Rect(pixel_size_x * j, pixel_size_y * i, pixel_size_x, pixel_size_y))


map_size = 70
mapp = [[1] * map_size for i in range(map_size)]
directional_map = [[[] for j in range(map_size)] for i in range(map_size)]
directional_map_2 = [[[] for j in range(map_size)] for i in range(map_size)]
for i in range(map_size-1):
    directional_map[i][0].append((i + 1, 0))
    directional_map[-1][i].append((-1, i + 1))
    directional_map_2[i][0].append('s')
    directional_map_2[-1][i].append('d')

path_is_complete = False
path = [[0] * map_size for i in range(map_size)]
# number_up_to = 0
convergiant_times = defaultdict(list)
convergiant_times[0].append((0, 0))
is_heading_back = False
heading_back = [(map_size-1, map_size-1)]
#pygame code
pygame.init()
width, height = 800, 800
pixel_size_x, pixel_size_y = width//len(mapp[0]), height//len(mapp)
window = pygame.display.set_mode((width, height))
colors = [(i*2, 0, i*2) for i in range(100)]




mapp[0][0] = 0
path[0][0] = 's'
path[-1][-1] = 'e'

while True:
    boiler()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_s] or keys[pygame.K_d]:
        mx, my = pygame.mouse.get_pos()
        row, col = my//pixel_size_y, mx//pixel_size_x
        directional_map_2[row][col].append('s' if keys[pygame.K_s] else 'd')
        directional_map[row][col].append((row, col+1) if keys[pygame.K_d] else (row+1, col))
    
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        row, col = my//pixel_size_y, mx//pixel_size_x
        mapp[row][col] = 2
    
    if keys[pygame.K_SPACE]:
        break

while True:
    # display(path)
    boiler()
    if is_heading_back:
        #print('heading back')
        reversing()
    else:
        #print('converging')
        converge()