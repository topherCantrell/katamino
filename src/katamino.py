"""
Katamino Simulator
"""

import copy
import datetime

import board
import pieces

# These are the challenges as listed in the manual
CHALLENGES = [
    {'title': 'Small Slam', 'page': '6', 'lines': [
        'A-3:AHGEBFLD', 'B-3:DECAFHGB', 'C-3:ALEHDCFK', 'D-3:HECDLKBG', 'E-3:ADLFCGHB', 'F-3:ECKHGDAB', 'G-3:ALEFHBDK']
     },
    {'title': 'Slam 1', 'page': '7,8', 'lines': [
        'A-5:AECKBHFDL', 'B-5:HDECFLGAK', 'C-5:AHLGBFKCE', 'D-5:DLECKBAFG', 'E-5:AHDEBGLKC', 'F-5:AECFGKDBH', 'G-5:ALECBDHGF',
        'H-5:ADEGBFHKL', 'I-5:AHLCFKBDG', 'J-5:ALEKBHCGD', 'K-5:AHDCBKELF', 'L-5:HLEFBDKGC', 'M-5:AHLEKCGFB', 'N-5:AHEFBDCLG',
        'O-6:AHDCKGFE',  'P-6:ADLEFKGH',  'Q-6:AHEFKBLC',  'R-6:ADLECGBK',  'S-6:HLECGBAF',  'T-6:AHLFKGEB',  'U-6:ADLECKFG',
        'V-6:DLECFGKH',  'W-6:DLECFKHB',  'X-6:HDLEGBFC',  'Y-6:ADCFKGLH',  'Z-6:AHEKGBCF',
        'Spades-6:HDECFGKB', 'Hearts-6:ADLCKBHG', 'Diamonds-6:ADLEKGBF', 'Clubs-6:ALECKGDH']
     },
    {'title': 'Ultimate Challenges 1', 'page': '9', 'lines': [
        'A-4:ADLFCGEJKIB', 'B-4:AHCKFLJEIDG', 'C-4:AHLEKBDCFGI', 'D-4:HECKGJALBFD', 'E-4:AHEFBDGKICJ', 'F-4:AECKJHIDGBL',
        'G-4:AHEBDCLFJIK', 'H-4:HDLGKIFBAJC', 'I-4:ALEFDKBIDGJ', 'J-4:AHEGBDILCJF', 'K-4:HDECLFJIBKG', 'L-4:AHLCFIKGJEB'
    ]},
    {'title': 'Ultimate Challenges 2', 'page': '10a', 'lines': [
        'A-5:ADEGBFLICHK', 'B-5:AHDLEGBJKIF', 'C-5:AECKBIFDLGJ', 'D-5:HDECFAJLGBI', 'E-5:HLEFBDGIJCK', 'F-5:DLECKJHAIGB',
        'G-5:AECGJKDFHLI', 'H-5:ALEKBICGJFH', 'I-5:AECFGHIJDKB', 'J-5:AHLGBFKICJD', 'K-5:ADECFJIHBKL', 'L-5:ALECBHJKFDG'
    ]},
    {'title': 'Ultimate Challenges 3', 'page': '10b', 'lines': [
        'A-9:IAHDLECFK', 'B-9:HLECFKGBJ', 'C-9:IADLEFKGJ', 'D-9:IAHECKGBJ', 'E-9:IDLECFKGB', 'F-9:IAHDLECBJ',
        'G-9:IHDECFKGJ', 'H-9:IAHDLKGBJ', 'I-9:AHDLCFKGJ', 'J-9:IAHDLEFGB', 'K-9:IALECFGBJ', 'L-9:IAHDCFKBJ'
    ]},
    {'title': 'Ultimate Challenges 4', 'page': '11', 'lines': [
        'No1-7:IAHECBJGLK',  'No2-7:AHEFKGBJDC',  'No3-7:IADLCFGHKE',  'No4-7:AHEKGBJIFL',  'No5-7:IHDLCKBAEJ',
        'No6-7:ALEKGBJFCD',  'No7-7:HDECFKGLJI',  'No8-7:IADECGJBFH',  'No9-7:ILECFKBDHA',  'No10-7:IHDLCGJKBF',
        'No11-7:IADEFGBKJC', 'No12-7:IHDLCFKGBA', 'No13-7:AHLCFKBJID', 'No14-7:DLECKGJHAB', 'No15-7:IAHLCKBEFJ',
        'No16-7:AHLEFBJGCI', 'No17-7:IHECFGBDLK', 'No18-7:IDLECKJBGF', 'No19-7:ADEFKGBLJH', 'No20-7:IADEFKGJHL',
        'No21-7:IDLECFGJAB', 'No22-7:IAHCKGBFDJ', 'No23-7:HDLEFKGBJC', 'No24-7:IAHDCGJLFE', 'No25-7:IHDLEKBJGF',
        'No26-7:AHLCKGJDBI', 'No27-7:IAHECFBJKG', 'No28-7:ADLEKGBCIH', 'No29-7:IALECFJKBD', 'No30-7:IHLCFGBEJK',
        'No31-7:AHDEKGBJIF', 'No32-7:IHECFKGDBJ', 'No33-7:AHDLEFBJKI', 'No34-7:IAHCKGJFDL', 'No35-7:IHDLCGBEJK',
        'No36-7:ADLCGBJIKE', 'No37-7:IAECKGBFLH', 'No38-7:IADCFKGLJB', 'No39-7:AHDLCKJBFG', 'No40-7:IALEFGBJHD',
    ]},

]


def main():
    """main"""

    with open('results.txt', 'w') as out:
        num = 0
        for sequence in SMALL_SLAM_3:
            num = num + 1
            pcs = []
            for pos in range(2):
                pcs.append(pieces.get_piece_by_name(sequence[pos]))
            pos += 1
            while pos < len(sequence):
                pcs.append(pieces.get_piece_by_name(sequence[pos]))
                brd = board.new_board(len(pcs))
                s = str(num) + ': '
                for p in pcs:
                    s = s + p.name
                print(s, end='')
                out.write(s + '\n')
                now = datetime.datetime.now()
                solve(brd, pcs, 0, out)
                after = datetime.datetime.now()

                print((after - now).seconds)
                pos += 1


def print_text_challenge():
    chal = CHALLENGES[5]
    line = chal['lines'][0]
    line = line[line.index(':') + 1:]
    brd = board.new_board(len(line) * 6, len(chal['lines']) * 6)

    for y in range(len(chal['lines'])):
        line = chal['lines'][y]
        line = line[line.index(':') + 1:]
        for x in range(len(line)):
            piece = pieces.get_piece_by_name(line[x])
            piece.place(
                brd, x * 6 + piece.print_ofs[0], y * 6 + piece.print_ofs[1], 0)

    board.print_board(brd)
