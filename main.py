import pygame
import random
import sys
import math
import numpy as np

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)

class DrawInformation :
    #COLORS
    
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREY = 128,128,128
    RED = 255,0,0
    GREEN = 0,255,0
    BLUE = 0,0,255
    CUSTOMCOLORS = [
        (210, 224, 251),
        (254, 249, 217),
        (222, 229, 212),
        (142, 172, 205),
        (255, 138, 138),
        (204, 224, 172)
    ]
    BACKGROUND_COLOR = WHITE
    
    SIDE_PADDING = 100
    TOP_PADDING = 150
    BOTTOM_PADDING = 50
    
    BASEWIDTH = 2
    
    GRADIENT = [
        CUSTOMCOLORS[0],
        CUSTOMCOLORS[1],
        CUSTOMCOLORS[2],
    ]
    
    FONT = pygame.font.SysFont('consolas',20)
    LARGE_FONT = pygame.font.SysFont('consolas',30)
    
    BORDER_TOP = 2
    
    def __init__ (self, width=1100, height = 600, lst = [], min_trs = 1, max_trs = 100):
        self.width = width
        self.height = height
        self.min_trs = min_trs
        self.max_trs = max_trs
        self.window = pygame.display.set_mode( (width, height) )
        pygame.display.set_caption( "Sorting Algorithm Visualization" )
        if lst : self.set_lst(lst)
        
    def set_lst (self, lst: list) :
        self.lst = lst
        self.max_val = max(lst) if lst else None
        self.min_val = min(lst) if lst else None
        
        self.block_width = round((  self.width - self.SIDE_PADDING ) / len(lst))
        self.block_height = math.floor(( self.height - self.TOP_PADDING - self.BOTTOM_PADDING) / ( self.max_trs - self.min_trs ))
        self.start_xpos = self.SIDE_PADDING / 2

def draw(draw_info: DrawInformation, algo_name, ascending = True,n = 0,delay = 0):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    
    title = draw_info.LARGE_FONT.render(f"{n} - {algo_name} - {'Ascending' if ascending else 'Descending'} | + {delay}ms", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 20))
    pygame.draw.line(draw_info.window,draw_info.BLACK,(draw_info.start_xpos,draw_info.block_height * draw_info.max_trs + draw_info.TOP_PADDING),\
                    (draw_info.width - draw_info.start_xpos,draw_info.block_height * draw_info.max_trs + draw_info.TOP_PADDING),draw_info.BASEWIDTH)
    
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | Q - Ascending/Descending | N - chane n",1,draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 60))
    
    controls_2 = draw_info.FONT.render("M - Mute/Unmute | E - Change Algorithm | D - Change delay",1,draw_info.BLACK)
    draw_info.window.blit(controls_2, (draw_info.width/2 - controls_2.get_width()/2 , 100))
    
    draw_list(draw_info)
    pygame.display.update()
    
def draw_list(draw_info : DrawInformation,color_positions = {}, clear_bg = False):
    lst = draw_info.lst
    
    if clear_bg :
        clear_rect = (draw_info.SIDE_PADDING//2, draw_info.TOP_PADDING,draw_info.width - draw_info.SIDE_PADDING, draw_info.height - draw_info.TOP_PADDING - draw_info.BOTTOM_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    
    for i,val in enumerate(lst) :
        x = draw_info.start_xpos + i * draw_info.block_width
        y = ((draw_info.height) - (val - draw_info.min_trs) * draw_info.block_height) - draw_info.BOTTOM_PADDING
        color = draw_info.GRADIENT[i % 3]
        if i in color_positions :
            color = color_positions[i]
        
        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.block_width, draw_info.block_height * (val - draw_info.min_trs)),border_top_left_radius=draw_info.BORDER_TOP,border_top_right_radius=draw_info.BORDER_TOP)
       
    if clear_bg :
        pygame.display.update()

def generate_starting_list (n : int, min_val : int, max_val : int):
    """generate lst that consisting of number betwen min and max value.

    Args:
        n (int): amount of member in the list
        min_val (int): minimum number that possible
        max_val (int): maximum number that possible
    """
    
    lst = []
    for _ in range(n) :
        lst.append(random.randint(min_val,max_val))
    
    return lst

def bubble_sort(draw_info, ascending=True,sound = False,delay = 0):
    lst = draw_info.lst
    
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            
            if delay > 0 :
                pygame.time.delay(delay)
                
            num1 = lst[j]
            num2 = lst[j + 1]
            if sound :
                play_sound(round(num2/draw_info.max_val),0.25)  
                
            draw_list(draw_info, {j: draw_info.CUSTOMCOLORS[5], j + 1: draw_info.CUSTOMCOLORS[4]}, True)
            
            if (num1 >= num2 and ascending) or (num1 <= num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
               
                yield True
            
    return lst
    
def insertion_sort(draw_info, ascending=True,sound = False,delay = 0):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            
            if delay > 0 :
                pygame.time.delay(delay)
            
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending
            draw_list(draw_info, {i - 1: draw_info.CUSTOMCOLORS[5], i: draw_info.CUSTOMCOLORS[4]}, True)
            if sound :
                play_sound(round(lst[i]/draw_info.max_val),0.25)
                
            if not ascending_sort and not descending_sort:
                break
            
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            
            yield True
            
    return lst
               
def play_sound(value, duration):
    NOTES = {
        0: 130.81,   # C3
        1: 146.83,   # D3
        2: 164.81,   # E3
        3: 174.61,   # F3
        4: 196.00,   # G3
        5: 220.00,   # A3
        6: 246.94,   # B3
        7: 261.63,   # C4
        8: 293.66,   # D4
        9: 329.63,   # E4
        10: 349.23,   # F4
    }
    frequency = NOTES.get(math.ceil(value*10))
    sample_rate = 44100  # sample rate 
    amplitude = 512     # Volume level

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = amplitude * np.sin(2 * np.pi * frequency * t)

    sound = np.int16(waveform).tobytes()
    
    # Create a Pygame Sound object from the waveform and play it
    sound_object = pygame.mixer.Sound(buffer=sound)
    sound_object.play()
    
def main ():
    run = True
    clock = pygame.time.Clock()
    
    ns = [10,20,25,40,50,100,125,200,250,500,1000]
    n_index = 4
    
    min_val = 1
    max_val = 101
    lst = generate_starting_list(ns[n_index],min_val,max_val)
    draw_info = DrawInformation(1100,600,lst,min_val,max_val)
    
    sorting = False
    ascending = True
    
    sorting_algorithm_generator = None
    
    sorting_algo_lst = [
        ("Bubble Sort",bubble_sort),
        ("Insertion Sort",insertion_sort)
    ]
    sorting_algo_lst_index = 0
    sorting_algo_name, sorting_algorithm = sorting_algo_lst[sorting_algo_lst_index]
    
    
    sound = True
    
    delays = [0,1,2,5,10,25,50,100,250,500]
    delay_index = 0
    
    while run :
        clock.tick(120) #fps
        if sorting :
            try :
                next(sorting_algorithm_generator)
            except StopIteration :
                sorting = False
        else :    
            draw(draw_info, sorting_algo_name, ascending,n = ns[n_index], delay = delays[delay_index])
                
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
                
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_r :
                    lst = generate_starting_list(ns[n_index], min_val, max_val)
                    draw_info.set_lst(lst)
                    sorting = False
                
                if event.key == pygame.K_m and not sorting:
                    sound = not sound
                if event.key == pygame.K_d and not sorting:
                    delay_index = delay_index + 1 if delay_index < len(delays) -1  else 0
                    
                if event.key == pygame.K_n and not sorting:
                    n_index = n_index + 1 if n_index < len(ns) -1 else 0
                    lst = generate_starting_list(ns[n_index], min_val, max_val)
                    draw_info.set_lst(lst)
                    
                elif event.key == pygame.K_SPACE and not sorting:
                    
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info, ascending,sound=sound,delay = delays[delay_index])
                    
                elif event.key == pygame.K_q and not sorting:
                    ascending = not ascending
                    
                elif event.key == pygame.K_e and not sorting:
                    sorting_algo_lst_index += 1
                    if sorting_algo_lst_index >= len(sorting_algo_lst) :
                        sorting_algo_lst_index = 0
                    (name,func) = sorting_algo_lst[sorting_algo_lst_index]
                    sorting_algorithm = func
                    sorting_algo_name = name
                    
                
                    
    pygame.quit()
    pygame.mixer.quit()
    sys.exit()

if __name__ == "__main__" :
    main()