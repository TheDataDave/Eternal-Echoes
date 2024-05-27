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


class Action:
    '''
    Used in Status to represent actions, have ease of access methods.

    A string representation of an action. If the action is valid __str__ will prefix it 
    with an underscore. Otherwise action is empty and __str__ will return "" instead. Class also 
    has data descriptors, and equality testing.
    '''
    def __init__(self, action):
        self.action = action

    def __get__(self, instance, owner):
        return self.action

    def __set__(self, instance, value):
        self.action = value

    def __eq__(self, other):
        return self.action == other
    
    def __str__(self):
        '''Format the action to have an underscore if there is an action'''
        if self.action != '':
            return f'_{self.action}'
        else:
            return f'{self.action}'



class Status:
    '''
    String representation of a status, handles string formatting. {status}{action} where
    action handles formatting (see Action). Allows ease of access and checking that actions actually
    change prior to update the action and status.
    '''
    def __init__(self, status):
        self._status = status
        self._total = None
        self.action = Action('')

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        self._set('')

    def _set(self, action):
        '''Adds action to status'''
        if self.action != action: # only run if the actions are different
            self.action = Action(action)
            self._total = f'{self.status}{self.action}'

    def __add__(self, action: str):
        '''Allows for + useage'''
        self._set(action)
        return self

    def __iadd__(self, action: str):
        '''Allows for inplace + useage'''
        self._set(action)
        return self

    def __str__(self):
        return f'{self._total}'