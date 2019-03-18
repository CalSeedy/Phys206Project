
tunings = {}

def genFreqs():
    global tunings
    f_0 = 440
	#Reference is A4 (440 Hz)
	#each tuning mode has an offset list of 6 offsets, each representing a note - i.e. 22 (= -2*12 + 2) would be B2
	# or 18 = (1*12 + 6) the D#/Eb5 note
    offsets = {"standard": [-2*12 - 5, -2*12, -1*12 - 7, -1*12 - 2, -1*12 + 2, -5], 
                "dropd": [-2*12 - 7, -2*12, -1*12 - 7, -1*12 - 2, -1*12 + 2, -5], 
                "openg": [-2*12 - 7, -2*12 -2, -1*12 - 7, -1*12 - 2, -1*12 + 2, -7], 
                "dadgad": [-2*12 - 7, -2*12, -1*12 - 7, -1*12 - 2, -1*12, -7], 
                "opend": [-2*12 - 7, -2*12, -1*12 - 7, -1*12 - 3, -1*12, -7]}
    keys = ["standard", "dropd", "openg", "dadgad", "opend"]
    # f_n = f_0 * 2^(1/12)| f_n = frequency, n semitones (notes) away | f_0, reference frequency (A4, 440Hz) | 2^(1/12) assuming the equal tempered scale
    for mode in range(len(offsets)):
        freqs = []
        key  = keys[mode]
        off = offsets[key]
        for i in range(6):
            s = off[i]
            f = f_0 * 2**(s/12)
            freqs.append(f)

        tunings[key] = freqs
        #print(freqs)

def getFreqs(mode: str) -> list:
    global tunings
    if (len(tunings) == 0 ):
        genFreqs()

    print("dfkjfskjbdfskj", tunings[mode])
    return tunings[mode.lower()]