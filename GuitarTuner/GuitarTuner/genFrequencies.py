import csv

notes = ["C","C#","D","D#","E","F","F#","G","G#","A", "A#","B"]
octaves = 6
offsets = [x for x in range(-57, (12*octaves) - 57)] #from C0 to B5 (6 complete octaves)
ref = 440

i = 0
j = 0
freqs = []
for j in range(octaves):
    for i in range(12):
        freq = ref * 2**((offsets[j * 12 + i]) / 12)
        freqs.append(freq)
with open('frequencies.csv', 'w', newline="") as writeFile:
    writer = csv.writer(writeFile)
    for j in range(octaves):
        for i in range(len(notes)):
            writer.writerow([notes[i] + str(j), freqs[i + j * 12]])
    writeFile.close()

    
