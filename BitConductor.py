#!/usr/bin/python3
import argparse

SONGS = {
    'mario':
        ['G3', '-', 'G3', '---', 'G3', '---', 'D#3', '-', 'G3', '---', 'A#3', '-------', 'A#3',
        '-------', 'D#3', '-------', 'A#2', '---', 'G2', '-----', 'C3',
        '---', 'D3', '---', 'C#3', '-', 'C3', '---', 'A#2', '--', 'G3', '-', 'A#3', '--', 'C4', '---', 'G#3',
        '-', 'A#3', '---', 'G3', '---', 'D#3', '-', 'F3', '-', 'D3', '-----', 'D#3', '-----', 'A#2'
        '-----', 'G2', '-----', 'C3', '---', 'D3', '---', 'C#3', '-', 'C3', '---', 'A#2',
        '--', 'G3', '-', 'A#3', '--', 'C4', '---', 'G#3', '-', 'A#3', '---', 'G3', '---', 'D#3', '-', 'F3', '-', 'D3'],
    'taylor_swift':
        ['F#4', '-', 'A4', '-', 'E5', '-', 'D5', '-', 'E5', '-', 'D5', '-', 'A4', '-', 'D5', '-', 
        'F#4', '-', 'A4', '-', 'E5', '-', 'D5', '-', 'E5', '-', 'D5', '-', 'A4', '-', 'D5', '-',
        'E4', '-', 'A4', '-', 'E5', '-', 'D5', '-', 'E5', '-', 'D5', '-', 'A4', '-', 'D5', '-'] 
}


def getFrequency(note):
    A4 = 440
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    octave = int(note[2]) if len(note) == 3 else int(note[1])
        
    keyNumber = notes.index(note[0:-1]);
    
    if (keyNumber < 3) :
        keyNumber = keyNumber + 12 + ((octave - 1) * 12) + 1; 
    else:
        keyNumber = keyNumber + ((octave - 1) * 12) + 1; 

    return int(A4 * 2** ((keyNumber- 49) / 12))

def convert(song):
    rob_triplets = []
    for idx,i in enumerate(song):
        last_note = idx == len(song) - 1
        if last_note:
            delay = 0
        else:
            if '-' in song[idx + 1]:
                delay = len(song[idx + 1]) * 70
            elif '-' in i:
                continue
        
        if '-' not in i:
            freq = getFrequency(i)
            rob_triplets.append((freq, 180, delay))

    return rob_triplets

def formatRob(triplets):
    cmd = ''
    base_cmd = 'rob call applications.beeper customBeep "{('

    chunks = [triplets[i:i + 15] for i in range(0, len(triplets), 15)]
    for chunk in chunks:
        tmp_base_cmd = ''       
        num_notes = len(chunk)
        i_str = '{iii}' * num_notes
        tmp_base_cmd += base_cmd + i_str + ')}" song'
        for note in chunk:
            f, d, o = note
            rob_note = f' frequency {f} duration {d} offDuration {o}'
            tmp_base_cmd += rob_note

        print('----------')
        print(tmp_base_cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--song', choices=['mario', 'taylor_swift'], help='Display the ROB command to play the chosen song', required=True)
    args = parser.parse_args()

    print(f'Converting: {args.song}')
    triplets = convert(SONGS.get(args.song))
    formatRob(triplets)
