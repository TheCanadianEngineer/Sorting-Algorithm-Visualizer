import pygame
import sys
import random
import numpy as np

# Initialize pygame
pygame.init()

# Create a window
width, height = 1200, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sorting Algorithms")

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Text
font = pygame.font.Font(None, 24)  
# None = default font, 48 = size


# List Vars

numAmount = 1200

numbers = random.sample(range(1, numAmount + 1), numAmount)
print(numbers)
# numbers.sort()

# Graph Vars

rectScale = height / numAmount

# Global Vars

delay = 0 # milliseconds

smallerNum = 0
biggerNum = 0

# Main Functions

pygame.mixer.init(frequency=44100)

def play_tone(number, duration=0.2):
    frequency = 200 + number * 10
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(frequency * t * 2 * np.pi)
    sound = np.int16(wave * 32767)

    # Convert numpy array to bytes
    sound_bytes = sound.tobytes()
    snd = pygame.mixer.Sound(buffer=sound_bytes)
    snd.play()

def drawScreen(funcName = "Undefined"):
    screen.fill(BLACK)
    numIdx = 0

    # Drawing Rec
    for x in numbers:
        if x == smallerNum: 
            play_tone(x)
            pygame.draw.rect(screen, GREEN, ((width / numAmount) * numIdx, height - x * rectScale, width / numAmount, x * rectScale))
        elif x == biggerNum:
            pygame.draw.rect(screen, RED, ((width / numAmount) * numIdx, height - x * rectScale, width / numAmount, x * rectScale))
        else:
            pygame.draw.rect(screen, WHITE, ((width / numAmount) * numIdx, height - x * rectScale, width / numAmount, x * rectScale))
        numIdx += 1

    # Drawing Text

    textSpacing = 20

    text_surface = font.render(f"Algorithm: {funcName}", True, WHITE)
    screen.blit(text_surface, (20, textSpacing))

    text_surface = font.render(f"Number of elements: {numAmount}", True, WHITE)
    screen.blit(text_surface, (20, textSpacing * 2))

    text_surface = font.render("Smaller Number", True, GREEN)
    screen.blit(text_surface, (20, textSpacing * 3))

    text_surface = font.render("Bigger Number", True, RED)
    screen.blit(text_surface, (20, textSpacing * 4))


    pygame.display.flip()
    pygame.time.wait(delay)

# Sorting Functions

def bubbleSort():
    global smallerNum, biggerNum, algName
    algName = "Bubble Sort"
    n = len(numbers)

    for i in range(n - 1):
        for j in range(n - i - 1):
            # Highlight the elements being compared
            smallerNum = numbers[j + 1]
            biggerNum = numbers[j]
            yield  # pause here to show the comparison

            # Swap if out of order
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                yield  # pause here to show the swap


def selectionSort():
    global smallerNum, biggerNum, algName
    algName = "Selection Sort"
    n = len(numbers)
    
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            # Highlight the current pair being compared
            smallerNum = numbers[j]
            biggerNum = numbers[min_idx]
            yield  # pause to visualize

            # Update min_idx if a smaller element is found
            if numbers[j] < numbers[min_idx]:
                min_idx = j
                smallerNum = numbers[min_idx]
                biggerNum = numbers[i]
                yield  # pause to visualize

        # Swap the found minimum element with the first unsorted element
        numbers[i], numbers[min_idx] = numbers[min_idx], numbers[i]
        smallerNum = numbers[i]
        biggerNum = numbers[min_idx]
        yield  # pause to visualize


def insertionSort():
    global smallerNum, biggerNum, algName
    algName = "Insertion Sort"
    for x in range(1, len(numbers)):
        current = x
        while current > 0 and numbers[current - 1] > numbers[current]:
            smallerNum = numbers[current]
            biggerNum = numbers[current - 1]

            numbers[current], numbers[current - 1] = numbers[current - 1], numbers[current]
            drawScreen(algName)

            yield

            current -= 1  # move left
    yield

def quickSort(arr=numbers, start=0, end=None):
    global numbers, smallerNum, biggerNum, algName
    algName = "Quick Sort"

    if end is None:
        end = len(arr) - 1

    if start >= end:
        return

    # Partition
    pivot = arr[end]
    biggerNum = pivot
    i = start

    for j in range(start, end):
        smallerNum = arr[j]
        yield  # show comparison

        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            yield  # show swap
            i += 1

    # Move pivot to correct position
    arr[i], arr[end] = arr[end], arr[i]
    yield  # show pivot placement

    # Recursive calls
    yield from quickSort(arr, start, i - 1)
    yield from quickSort(arr, i + 1, end)

def combSort():
    global smallerNum, biggerNum, algName
    algName = "Comb Sort"
    
    n = len(numbers)

    gap = n
    swapped = False

    while gap > 1 or swapped:
        gap = max(1, int(gap / 1.3))
        swapped = False
        for j in range(n  - gap):
            # Highlight the elements being compared
            smallerNum = numbers[j + gap]
            biggerNum = numbers[j]
            yield  # pause here to show the comparison

            # Swap if out of order
            if numbers[j] > numbers[j + gap]:
                numbers[j], numbers[j + gap] = numbers[j + gap], numbers[j]
                swapped = True
                yield  # pause here to show the swap
        


# Main loop
running = True
sort_gen = combSort()
algName = "Undefined"
fullyFinished = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    numbers2 = numbers.copy()
    numbers2.sort()
    if numbers == numbers2 :
        if  not fullyFinished:
            numIdx = 0
            while numIdx < numAmount:
                screen.fill(BLACK)
                for i in range(len(numbers)):
                    x = numbers[i]
                    if i < numIdx:
                        color = GREEN
                    else:
                        color = WHITE
                    if numIdx == numbers[i - 1]:
                        play_tone(numbers[i - 1])
                        print(numbers[i-1], i)
                    pygame.draw.rect(screen, color, ((width / numAmount) * i, height - x * rectScale, width / numAmount, x * rectScale))

                pygame.display.flip()
                pygame.time.delay(int(1000 / numAmount))  # optional, controls animation speed
                numIdx += 1

            fullyFinished = True
        else:
            screen.fill(BLACK)
            numIdx = 0
            for x in numbers:
                pygame.draw.rect(screen, GREEN, ((width / numAmount) * numIdx, height - x * rectScale, width / numAmount, x * rectScale))
                numIdx += 1
            pygame.display.flip()
    else:
        
        try:
            next(sort_gen)  # perform one swap/step
            drawScreen(algName)
        except StopIteration:
        # Sorting is done
            drawScreen("Sorted")

pygame.quit()
sys.exit()
