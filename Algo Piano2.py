#!/usr/bin/env python

from collections import OrderedDict
from midiutil.MidiFile import MIDIFile
from random import randint
"""This program creates melody and accompaniment in the form of a MIDI file.  It takes a melodic motive,
a key area, a scale and a meter as input.  """

class serializer():
    def __init__(self, row):
        self.row = row #input motive as a list of strings
        self.P0_num = [] #input row  as a list of integers
        self.R0_num = [] #P0_num backwards
        self.I0_num = [] #Mirror image version of P0_num
        self.RI_num = [] #I0_num backwards
        self.P_num = []  #List of lists which holds all rows.
        
        
    def string_to_int(self, pitch_class_dict, valid):
        """Convert string melodic motive (row)input to integers (P0_num)"""
        P0 = self.row.split() #Create list from melodic motive input.  This is the Prime row
        for items in P0:
            if items in pitch_class_dict:
                self.P0_num.append(pitch_class_dict[items])
            else:
                print 'Remember-- capital letters A-G with sharps (not flats)'
                break
        self.P_num.append(self.P0_num)
        
    
    def reverse_row(self):
        """Reverses P0_num and I0_num and appends to P_num"""
        self.R0_num = self.P0_num[::-1]
        self.P_num.append(self.R0_num)
    
    def inverse_row(self):
        """Produces the mirror image of P0_num (I0_num"""
        count = 1
        intervals = []
        while count <= len(self.P0_num) - 1:
            x = 0
            x = self.P0_num[count] - self.P0_num[count - 1]
            intervals.append(x)
            count += 1
        x = self.P0_num[0]
        self.I0_num.append(x)
        for i in range(len(intervals)):
            x = x-intervals[i]
            self.I0_num.append(x)
        self.P_num.append(self.I0_num)
        
    def transpositions(self):
        """Generates all 12 transpositions of items in P_num (12 notes in the chromatic scale)"""
        for items in range(0,4):
            for i in range(1,13):
                x = self.P_num[items][0]
                y = [x+i for x in self.P_num[items]]
                self.P_num.append(y)
                i += 1
    
#Find scale of piece by looking up scale_type input in scale_dict
scale_dict = {
    'major': [0, 2, 4, 5, 7, 9 , 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'harmonic minor': [0, 2, 3, 5, 7, 8, 11],
    'gypsy': [0, 1, 2, 5, 6, 8, 9],
    'octatonic 1': [0, 1, 3, 4, 6, 7, 9, 10],
    'octatonic 2': [0, 2, 3, 5, 6, 8, 9, 11],
    'acoustic': [0, 2, 4, 6, 7, 9, 10],
    'augmented': [0, 3, 4, 7, 8, 11],
    'altered': [0, 1, 3, 4, 6, 8, 10],
    'bebop dominant': [0, 2, 4, 5, 7, 9, 10, 11],
    'blues': [0, 3, 5, 6, 7, 10],
    'double harmonic': [0, 1, 4, 5, 7, 8, 11],
    'flamenco': [0, 1, 4, 5, 7, 8, 11],
    'harmonic major': [0, 2, 4, 5, 7, 8, 11],
    'hungarian minor': [0, 2, 3, 6, 7, 8, 11],
    'lydian augmented': [0, 2, 4, 6, 8, 9, 11],
    'major bebop': [0, 2, 4, 5, 7, 8, 9, 11],
    'neapolitan minor': [0, 1, 3, 5, 7, 8, 11],
    'phrygian dominant': [0, 1, 4, 5, 7, 8, 10],
    'prometheus': [0, 2, 4, 6, 9, 10],
    'tritone': [0, 1, 4, 6, 7, 10],
    'ukranian dorian': [0, 2, 3, 6, 7, 9, 10],
}

class diatonic():
    def __init__(self, key_area, scale_type):
        self.key_area = key_area #Root of scale as a string e.g. A, B, C
        self.scale_type = scale_type #type of scale e.g., major, minor
        self.key_area_num = 0  #Root of scale expressed as an integer
        self.key_of_piece = [] #1 octave of scale
        self.key_of_piece2 = [] #6 octaves of scale
        self.tonal_P_num = [] #version of P_num where all notes are diatonic to key_of_piece
        self.P_num2 = [] #version of tonal_P_num where repeated notes are removed
    
    def find_key_num(self, pitch_class_dict):
        """Convert string key_area input to integer (key_area_num)"""
        if key_area in pitch_class_dict:
            self.key_area_num = pitch_class_dict[key_area]

    def make_key(self, scale_type, scale_dict):
        """Look up scale_type in scale_dict and create 1 octave of scale in key of piece"""
        if scale_type in scale_dict:
            scale_temp = scale_dict[scale_type]
            self.key_of_piece = [self.key_area_num + x for x in scale_temp]
     
    def make_transpositions(self, num1):
        """make transpositions of scale for several octaves"""
        for items in range(0,len(self.key_of_piece)):
            self.key_of_piece2.append(self.key_of_piece[items] + num1)
   
    def nearest_scale_degree(self, P_num):
        """Goes through P_num looking for items the are not in the key of the piece.
        when it finds one, it changes that item to equal the nearest scale degree"""
        for sub_list in P_num:
            list5 = []
            for items in sub_list:
                if items in self.key_of_piece2:
                    list5.append(items)
                else:
                    list3 = []
                    for z in self.key_of_piece2:
                        diff = z - items
                        list3.append(diff)
                    list4 = [abs(i) for i in list3]
                    a = min(list4)
                    if -a in list3:
                        items = items - a
                        list5.append(items)
                    else:
                        items = items + a
                        list5.append(items)
            self.tonal_P_num.append(list5)
   

    def remove_duplicate_notes(self):
        """nearest_scale_degree sometimes results in 2 identical notes in a row.
        This function removes duplicate notes from tonal_P_num"""
        self.P_num2 = list(self.tonal_P_num)
        for items in self.P_num2:
            items = list(OrderedDict.fromkeys(items))
            

class harmonic_progression():
    def __init__(self, meter):
        self.meter = meter #3/4 or 4/4 time
        self.harm_rh = [] #Holds a single harmonic rhythm
        self.harm_choices = [] #holds all harm_rh
        self.chord_choices = [] #analogous to harm_choices, but instead of durations, it hold chord roots
        self.harm_length = [] #list of integers holding number of beats each chord is to be held
        self.harm_final = [] #contains final harmonic rhythm and chords sequence 
        self.chords_final = [] #Final sequence of chords
    
    def set_harm_lengths(self):
        """Depending on meter, this determines the length of time each chord will be held."""
        if self.meter == 4:
            self.harm_length = [[2,2],[2,2],[4],[4],[4],[4],[8],[8],[16]] #number of beats a harmony is held
        else:
            self.harm_length = [[3],[3],[6],[6],[12]] #number of beats a harmony is held


    def make_harm_prog1(self):
        """Generates a harmonic rhythm """
        if self.meter == 4:
            progs = [8, 16]
        else:
            progs = [6, 12]
        x = randint(0,len(progs)-1)
        prog_length = progs[x]
        time = 0
        self.harm_rh = []
        while time < prog_length:
            z = randint(0,len(self.harm_length)-1)
            for items in self.harm_length[z]:
                self.harm_rh.append(items)
            time = sum(self.harm_rh)
        if sum(self.harm_rh) > prog_length:
            self.harm_rh.pop()
            x = prog_length - sum(self.harm_rh)
            if x > 0:
                self.harm_rh.append(x)
        self.harm_choices.append(self.harm_rh)
    
    def make_harm_prog2(self, P_num2):
        """Picks chords roots from tonal_P_num2 for each entry in harm_rh"""
        time = 0
        chord_prog = []
        chord_count = 0
        no_chords = [2,3,3,4,4,4,5,6,7]
        allowed_chords1 = randint(0,len(no_chords)-1)
        allowed_chords2 = no_chords[allowed_chords1]
        while len(chord_prog)< len(self.harm_rh):
            last_chord = 0
            if chord_count < allowed_chords2:
                z =randint(0,len(P_num2)-1)
                while P_num2[z][0] == last_chord:
                    z =randint(0,len(P_num2)-1)
                for items in P_num2[z]:
                    chord_prog.append(items)
                    chord_count += 1
                    last_chord = items
                    if len(chord_prog) > len(self.harm_rh):
                        break
            else:
                z =randint(0,len(chord_prog)-1)
                chord_prog.append(chord_prog[z])
            if len(chord_prog) > len(self.harm_rh):
                chord_prog.pop()
        self.chord_choices.append(chord_prog)

    def make_harm_final(self):
        """Randomly chooses chord progressions and harmonic rhythms to fill the length of the piece.
        The chords and the harmonic lengths are placed in separate lists, and then those lists are
        packed into one master list (harm_final)."""
        list1 = []
        list2 = []
        no_repeats = -1
        while sum(list1) < 256:
            z = randint(0,len(self.harm_choices)-1)
            while z == no_repeats:
                z = randint(0,len(self.harm_choices)-1)
            no_repeats = z
            for items in self.harm_choices[z]:
                list1.append(items)
            for items in self.chord_choices[z]:
                list2.append(items)
            if sum(self.harm_choices[z]) < 16:
                for items in self.harm_choices[z]:
                    list1.append(items)
                for items in self.chord_choices[z]:
                    list2.append(items)
        self.harm_final.append(list1)
        self.harm_final.append(list2)

    def make_chords_final(self, key_of_piece2, chord_dict):
        """Looks up chord roots in chord_dict to determine chord type (major,minor), the other 2 members of
        the chord's triad as well as voicings and inversions"""
        notes_chords = True
        for items in self.harm_final[1]:
            for chords in chord_dict:
                for notes in chord_dict[chords]:
                    if notes + items in key_of_piece2:
                        notes_chords = True
                    else:                
                        notes_chords = False
                        break
                if notes_chords == True:
                    list1 = []
                    for notes in chord_dict[chords]:
                        list1.append(notes + items)
                    self.chords_final.append(list1)
                    break

class accompaniment():
    def __init__(self):
        self.time = 0.0
        self.eighth_patterns = [self.acc1_pattern, self.acc3_pattern]
        self.quarter_patterns2 = [self.acc10_pattern, self.acc11_pattern]
        self.quarter_patterns4 = [self.acc2_pattern, self.acc4_pattern, self.acc5_pattern, self.acc6_pattern, self.acc7_pattern]
        self.waltz_patterns = [self.acc12_pattern, self.acc13_pattern, self.acc14_pattern, self.acc15_pattern, self.acc15_pattern]

    def acc1_pattern(self, list1, items):
        """A left hand pattern consisting of 1/8 notes, duration 2 beats"""
        pitch = list1[items][0] -12
        duration = 0.5
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 0.5
        pitch = list1[items][2] -12
        duration = 0.5
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 0.5
        pitch = list1[items][1] -12
        duration = 0.5
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 0.5
        pitch = list1[items][2] -12
        duration = 0.5
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        
        
    def acc2_pattern(self, list1, items):
        """quarter note pattern, duration 4 beats"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][2] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][2] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
       
    def acc3_pattern(self, list1, items):
        """1/8 notes pattern, duration 2 beats"""
        pitch = list1[items][0] -12
        duration = 0.5
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 0.5
        pitch = list1[items][1] -12
        duration = 0.5
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 0.5
        pitch = list1[items][2] -12
        duration = 0.5
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 0.5
        pitch = list1[items][1] -12
        duration = 0.5
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        
        

    def acc4_pattern(self, list1, items):
        """quarter note pattern, duration 4 beats"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][2] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        

    def acc5_pattern(self, list1, items):
        """quarter note pattern, duration 4 beats"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] 
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] - 12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] 
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] - 12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        
        

    def acc6_pattern(self, list1, items):
        """quarter note pattern, duration 4 beats"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] 
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] 
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)      

    def acc7_pattern(self, list1, items):
        """quarter/half note pattern, duration 4 beats"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] 
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] 
        duration = 2
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] -12
        duration = 2
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        
        
    def acc9_pattern(self, list1, items):
        """quarter note pattern, duration 1 beat"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][1] - 12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        

    def acc10_pattern(self, list1, items):
        """half note pattern, duration 2 beats"""
        pitch = list1[items][0] -12
        duration = 2
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][1] 
        duration = 2
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] -12
        duration = 2
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        
        

    def acc11_pattern(self, list1, items):
        """quarter note pattern, duration 2 beats"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1]
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] -12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        

    def acc12_pattern(self, list1, items):
        """waltz pattern, duration 3 beats"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1]
        duration = 2
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2]-12
        duration = 2
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
       
        

    def acc13_pattern(self, list1, items):
        """waltz pattern, duration 3 beats"""
        pitch = list1[items][0] -12
        duration = 3
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][1] -12
        duration = 3
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] -12
        duration = 3
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        

    def acc14_pattern(self, list1, items):
        """waltz pattern, duration 3 beats"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1]
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] - 12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1]
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] - 12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        

    def acc15_pattern(self, list1, items):
        """waltz pattern, duration 3 beats"""
        pitch = list1[items][0] -12
        duration = 1
        time = self.time
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] 
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] - 12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        time += 1
        pitch = list1[items][1] - 12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        pitch = list1[items][2] - 12
        duration = 1
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        
       

    def fourfour_acc(self, harm_final, chords_final):
        """If the piece is in 4/4, for each item in harm_final/chords_final, choose and ac
        accompaniment function to fill out the left hand part of the piece"""
        for items in range(0,len(harm_final[0])-1):
            time_chord = 0.0
            while time_chord < harm_final[0][items]:
                if harm_final[0][items] % 2 != 0:
                    self.notes_durations_time = self.acc9_pattern(hp.chords_final, items)
                    self.time += 1
                    time_chord += 1
                elif harm_final[0][items] % 4 == 0:
                    i = randint(0,len(self.quarter_patterns4)-1)
                    self.notes_durations_time = self.quarter_patterns4[i](hp.chords_final, items)
                    self.time += 4
                    time_chord += 4
                elif harm_final[0][items] % 2 == 0:
                    i = randint(0,len(self.quarter_patterns2)-1)
                    self.notes_durations_time = self.quarter_patterns2[i](hp.chords_final, items)
                    self.time += 2
                    time_chord += 2

    def threefour_acc(self, harm_final, chords_final):
        """If the piece is in 3/4, for each item in harm_final/chords_final, choose and ac
        accompaniment function to fill out the left hand part of the piece"""
        for items in range(0,len(harm_final[0])-1):
            time_chord = 0.0
            while time_chord < harm_final[0][items]:
                i = randint(0,len(self.waltz_patterns)-1)
                self.notes_durations_time = self.waltz_patterns[i](hp.chords_final, items)
                self.time += 3
                time_chord += 3
                
                
class melody():
    
    def __init__(self):
        self.durations_for_chord_tones = [0.5,1,1,1,2,2,3,4]
        self.durations_for_non_chord_tones = [0.5,1]
    
    def compose_melody(self, tonal_P_num, chords_final, harm_final):
        """Generates melody for each item in harm_final by randomly choosing motives from
        tonal_P_num.  The 1st melody note of each chord must be a chord member.  Otherwise,
        consonance is achieved by allowing chord tones to ring out longer than non-chord tones"""
        count1 = 0
        time = 0.0
        for items in harm_final[0]:
            time_chord = 0.0
            count2 = 0 
            while time_chord < items:
                j = randint(0, len(tonal_P_num)-1)
                if count2 == 0:
                    if tonal_P_num[j][0] not in chords_final[count1]:
                        consonant = False
                        while consonant == False:
                            j = randint(0, len(tonal_P_num)-1)
                            if tonal_P_num[j][0] in chords_final[count1]:
                                consonant = True
                for notes in tonal_P_num[j]:
                    if notes in chords_final[count1]:
                        i = randint(0, len(self.durations_for_chord_tones)-1)
                        duration = self.durations_for_chord_tones[i]
                    else:
                        i = randint(0, len(self.durations_for_non_chord_tones)-1)
                        duration = self.durations_for_non_chord_tones[i]
                    pitch = notes + 12
                    if duration > (items - time_chord) and (items - time_chord)> 0:
                        duration = (items - time_chord)
                    if duration > (items - time_chord) and (items - time_chord)<= 0:
                        break
                    MyMIDI.addNote(track,channel,pitch,time,duration,volume)
                    time_chord += duration
                    time += duration
                    if time_chord >= items:
                        break
                    count2 += 1
            count1 += 1        


        
pitch_class_dict = {'A': 57 , 'A#' : 58, 'B': 59, 'C' : 60, 'C#' : 61, 'D' : 62 , 'D#' : 63, 'E' : 64, 'F' : 65,
                    'F#' : 66, 'G' : 67, 'G#' : 68}
chord_dict = {1: [0, 4, 7] , 2: [0, 3, 7], 3: [0,3,8], 4: [0,4,9], 5: [0,5,9], 6: [0,5,8], 7: [0,4,0], 8: [0,3,0]}

#Get input
valid = False
while valid == False:
    row = raw_input('Please enter a melodic motive. A A# B C C# D D# E F F# G G#')
    row_obj = serializer(row)
    row_obj.string_to_int(pitch_class_dict, valid)
    if len(row_obj.P0_num) > 0:
        valid = True

valid = False
while valid == False:
    meter = raw_input('4 or 3?')
    METERS = ['4','3']
    if meter in METERS:
        valid = True
        meter = int(meter)

valid = False
while valid == False:
    key_area = raw_input('What key will this piece be in?')
    key_row = serializer(key_area)
    key_row.string_to_int(pitch_class_dict, valid)
    if len(key_row.P0_num) > 0:
        valid = True

valid = False
while valid == False:
    scale_type = raw_input('What type of scale? major, minor, harmonic minor, gypsy,\n'
                           'octatonic 1, octatonic 2, acoustic, augmented, altered,\n'
                           'bebop dominant, blues, double harmonic, flamenco, harmonic major,\n'
                           'hungarian minor, lydian augmented, major bebop, neapolitan minor,\n'
                           'phrygian dominant, prometheus, tritone, ukranian dorian')
    if scale_type in scale_dict:
        valid = True
                       

title = raw_input('Give it a title.')
title2 = title + ".mid"
row_obj.reverse_row()
row_obj.inverse_row()
row_obj.reverse_row()
row_obj.transpositions()
key_obj = diatonic(key_area, scale_type)
key_obj.find_key_num(pitch_class_dict)
key_obj.make_key(scale_type, scale_dict)
key_obj.make_transpositions(0)
key_obj.make_transpositions(12)
key_obj.make_transpositions(24)
key_obj.make_transpositions(-12)
key_obj.make_transpositions(-24)
key_obj.make_transpositions(36)
key_obj.make_transpositions(-36)
key_obj.nearest_scale_degree(row_obj.P_num)
key_obj.remove_duplicate_notes()


hp = harmonic_progression(meter)
hp.set_harm_lengths()
i =  randint(3,5)

#Make 3 harmonic progressions
hp.make_harm_prog1()
hp.make_harm_prog2(key_obj.tonal_P_num)
hp.make_harm_prog1()
hp.make_harm_prog2(key_obj.tonal_P_num)
hp.make_harm_prog1()
hp.make_harm_prog2(key_obj.tonal_P_num)
hp.make_harm_final()
hp.make_chords_final(key_obj.key_of_piece2, chord_dict)


#Create MIDI object and initialize variables
MyMIDI = MIDIFile(1)
time = 0.0
track = 0
channel = 0
pitch = 60
time = 0.0
duration = 1
volume = 100

MyMIDI.addTrackName(track, time, 'Sample')
MyMIDI.addTempo(track, time, 70)

acc = accompaniment()
if meter == 4:
    acc.fourfour_acc(hp.harm_final, hp.chords_final)
else:
    acc.threefour_acc(hp.harm_final, hp.chords_final)

for items in hp.chords_final:
    for notes in range(0,3):
        items.append(items[notes]+12)
        items.append(items[notes]-12)
        
m = melody()
m.compose_melody(key_obj.tonal_P_num, hp.chords_final, hp.harm_final)

binfile = open(title2, 'wb')
MyMIDI.writeFile(binfile)
binfile.close()


