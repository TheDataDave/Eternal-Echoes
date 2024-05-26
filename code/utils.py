import pygame

from csv import reader
from os import walk
from os.path import join

def import_csv_layout(path):
    '''Loads tile map csv map data'''
    layout = []
    with open(path, 'r') as file:
        csv_reader = reader(file, delimiter=',')
        for row in csv_reader:
            layout.append(list(row))
    return layout


def import_folder(path):
    '''Iterates through a folder and turns all images into pygame.images'''
    images = []
    for _, _, img_files in walk(path):
        for img in img_files:
            images.append(pygame.image.load(join(path, img)))
    return images