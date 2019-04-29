AllFreqs = [16.351597831287414, 17.323914436054505, 18.354047994837977, 19.445436482630058, 20.601722307054366, 21.826764464562746, 23.12465141947715, 24.499714748859326, 25.956543598746574, 27.5, 29.13523509488062, 30.86770632850775, 
32.70319566257483, 34.64782887210901, 36.70809598967594, 38.890872965260115, 41.20344461410875, 43.653528929125486, 46.2493028389543, 48.999429497718666, 51.91308719749314, 55.0, 58.27047018976124, 61.7354126570155, 
65.40639132514966, 69.29565774421802, 73.41619197935188, 77.78174593052023, 82.4068892282175, 87.30705785825097, 92.4986056779086, 97.99885899543733, 103.82617439498628, 110.0, 116.54094037952248, 123.47082531403103, 
130.8127826502993, 138.59131548843604, 146.8323839587038, 155.56349186104046, 164.81377845643496, 174.61411571650194, 184.9972113558172, 195.99771799087463, 207.65234878997256, 220.0, 233.08188075904496, 246.94165062806206, 
261.6255653005986, 277.1826309768721, 293.6647679174076, 311.1269837220809, 329.6275569128699, 349.2282314330039, 369.9944227116344, 391.99543598174927, 415.3046975799451, 440.0, 466.1637615180899, 493.8833012561241, 
523.2511306011972, 554.3652619537442, 587.3295358348151, 622.2539674441618, 659.2551138257398, 698.4564628660078, 739.9888454232688, 783.9908719634985, 830.6093951598903, 880.0, 932.3275230361799, 987.7666025122483] 

notes0 = ["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0", "A#0","B0"]
notes1 = ["C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1", "A#1","B1"]
notes2 = ["C2","C#2","D2","D#2","E2","F2","F#2","G2","G#2","A2", "A#2","B2"]
notes3 = ["C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3", "A#3","B3"]
notes4 = ["C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4", "A#4","B4"]
notes5 = ["C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5", "A#5","B5"]

Dict ={}
def generate():
    for note in notes0:
        Dict[note] = AllFreqs[notes0.index(note)]
    for note in notes1:
        Dict[note] = AllFreqs[12 + notes1.index(note)]
    for note in notes2:
        Dict[note] = AllFreqs[24 + notes2.index(note)]
    for note in notes3:
        Dict[note] = AllFreqs[36 + notes3.index(note)]
    for note in notes4:
        Dict[note] = AllFreqs[48 + notes4.index(note)]
    for note in notes5:
        Dict[note] = AllFreqs[60 + notes5.index(note)]

    return Dict