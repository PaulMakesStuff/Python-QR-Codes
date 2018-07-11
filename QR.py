#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SVG import SVG
import sys
import math

# 1. for the inital script, all data is to be encoded as alpha numeric
# 2. get the length of the input string
# 3. get the error correction level
# 4. determine the smallest version we can use, using table 7 in the ISO 
#       standard.
# 5. add the mode indicator from table 2 within the ISO standard.
# 6. add the character count indicator from table 3 of ISO
# 7. encode data using the alpha numeric encoding.
# 8. add terminator zeros. 
#       check the required length of the data stream 
#       do this by checking out the required number of data codewords for the 
#           version and error detection level of the code in question, this is 
#           in table 7 of the ISO.
#       multiply the required number of codewords by eight to get the required 
#           number of bits
#       check the length of the datastream to far, if it falls short by greater
#           than four just add four zeros '0000' else, add the number of zeros 
#           required to get it up to the correct length.

class QR(object):

    # Lists the capacity of the code to store [N]umeric or [A]lphanumeric 
    # characters.  As well as the required number of [D]ata codewords and 
    # [E]rror codewords.  Based upon table 7 (and some 9) of the ISO 
    # specification.
    TABLE_7_9 = [{
        'L':{'N':0, 'A':0, 'D':0, 'E':0},
        'M':{'N':0, 'A':0, 'D':0, 'E':0}, 
        'Q':{'N':0, 'A':0, 'D':0, 'E':0}, 
        'H':{'N':0, 'A':0, 'D':0, 'E':0}},{ # V1...
        'L':{'N':41, 'A':25, 'D':19, 'E':7}, 
        'M':{'N':34, 'A':20, 'D':16, 'E':10}, 
        'Q':{'N':27, 'A':16, 'D':13, 'E':13}, 
        'H':{'N':17, 'A':10, 'D':9, 'E':17}},{ # V2...
        'L':{'N':77, 'A':47, 'D':34, 'E':10}, 
        'M':{'N':63, 'A':38, 'D':28, 'E':16}, 
        'Q':{'N':48, 'A':29, 'D':22, 'E':22}, 
        'H':{'N':34, 'A':20, 'D':16, 'E':28}},{ # V3...
        'L':{'N':127, 'A':77, 'D':55, 'E':15}, 
        'M':{'N':101, 'A':61, 'D':44, 'E':26}, 
        'Q':{'N':77, 'A':47, 'D':34, 'E':36}, 
        'H':{'N':58, 'A':35, 'D':26, 'E':44}}]
    TABLE_9 = [{},{
        'L':{'BLOCKS':1,'DATA':19,'ERROR':7},
        'M':{'BLOCKS':1,'DATA':16,'ERROR':10},
        'Q':{'BLOCKS':1,'DATA':13,'ERROR':13},
        'H':{'BLOCKS':1,'DATA':9,'ERROR':17}},{ # v2...
        'L':{'BLOCKS':1,'DATA':34,'ERROR':10},
        'M':{'BLOCKS':1,'DATA':28,'ERROR':16},
        'Q':{'BLOCKS':1,'DATA':22,'ERROR':22},
        'H':{'BLOCKS':1,'DATA':16,'ERROR':28}},{ # v3
        'L':{'BLOCKS':1,'DATA':55,'ERROR':15},
        'M':{'BLOCKS':1,'DATA':44,'ERROR':26},
        'Q':{'BLOCKS':2,'DATA':17,'ERROR':18},
        'H':{'BLOCKS':2,'DATA':13,'ERROR':22}}]
    FORMAT_INFORMATION = {
    'L':['111011111000100','111001011110011','111110110101010',
        '111100010011101','110011000101111','110001100011000',
        '110110001000001','110100101110110'],
    'M':['101010000010010','101000100100101','101111001111100',
        '101101101001011','100010111111001','100000011001110',
        '100111110010111','100101010100000'],
    'Q':['011010101011111','011000001101000','011111100110001',
        '011101000000110','010010010110100','010000110000011',
        '010111011011010','010101111101101'],
    'H':['001011010001001','001001110111110','001110011100111',
        '001100111010000','000011101100010','000001001010101',
        '000110100001100','000100000111011']}

    # Where in the qr code is data inserted, this depends on the version.
    bit_positions = [[], [], [], []]
    bit_positions[0] = []
    bit_positions[1] = [[20,20],[19,20],[20,19],[19,19],[20,18],[19,18],
    [20,17],[19,17],[20,16],[19,16],[20,15],[19,15],[20,14],[19,14],[20,13],
    [19,13],[20,12],[19,12],[20,11],[19,11],[20,10],[19,10],[20,9],[19,9],
    [18,9],[17,9],[18,10],[17,10],[18,11],[17,11],[18,12],[17,12],[18,13],
    [17,13],[18,14],[17,14],[18,15],[17,15],[18,16],[17,16],[18,17],[17,17],
    [18,18],[17,18],[18,19],[17,19],[18,20],[17,20],[16,20],[15,20],[16,19],
    [15,19],[16,18],[15,18],[16,17],[15,17],[16,16],[15,16],[16,15],[15,15],
    [16,14],[15,14],[16,13],[15,13],[16,12],[15,12],[16,11],[15,11],[16,10],
    [15,10],[16,9],[15,9],[14,9],[13,9],[14,10],[13,10],[14,11],[13,11],
    [14,12],[13,12],[14,13],[13,13],[14,14],[13,14],[14,15],[13,15],[14,16],
    [13,16],[14,17],[13,17],[14,18],[13,18],[14,19],[13,19],[14,20],[13,20],
    [12,20],[11,20],[12,19],[11,19],[12,18],[11,18],[12,17],[11,17],[12,16],
    [11,16],[12,15],[11,15],[12,14],[11,14],[12,13],[11,13],[12,12],[11,12],
    [12,11],[11,11],[12,10],[11,10],[12,9],[11,9],[12,8],[11,8],[12,7],[11,7],
    [12,5],[11,5],[12,4],[11,4],[12,3],[11,3],[12,2],[11,2],[12,1],[11,1],
    [12,0],[11,0],[10,0],[9,0],[10,1],[9,1],[10,2],[9,2],[10,3],[9,3],[10,4],
    [9,4],[10,5],[9,5],[10,7],[9,7],[10,8],[9,8],[10,9],[9,9],[10,10],[9,10],
    [10,11],[9,11],[10,12],[9,12],[10,13],[9,13],[10,14],[9,14],[10,15],[9,15],
    [10,16],[9,16],[10,17],[9,17],[10,18],[9,18],[10,19],[9,19],[10,20],[9,20],
    [8,12],[7,12],[8,11],[7,11],[8,10],[7,10],[8,9],[7,9],[5,9],[4,9],[5,10],
    [4,10],[5,11],[4,11],[5,12],[4,12],[3,12],[2,12],[3,11],[2,11],[3,10],
    [2,10],[3,9],[2,9],[1,9],[0,9],[1,10],[0,10],[1,11],[0,11],[1,12],[0,12]]
    bit_positions[2] = [[24,24],[23,24],[24,23],[23,23],[24,22],[23,22],
    [24,21],[23,21],[24,20],[23,20],[24,19],[23,19],[24,18],[23,18],[24,17],
    [23,17],[24,16],[23,16],[24,15],[23,15],[24,14],[23,14],[24,13],[23,13],
    [24,12],[23,12],[24,11],[23,11],[24,10],[23,10],[24,9],[23,9],[22,9],
    [21,9],[22,10],[21,10],[22,11],[21,11],[22,12],[21,12],[22,13],[21,13],
    [22,14],[21,14],[22,15],[21,15],[22,16],[21,16],[22,17],[21,17],[22,18],
    [21,18],[22,19],[21,19],[22,20],[21,20],[22,21],[21,21],[22,22],[21,22],
    [22,23],[21,23],[22,24],[21,24],[20,24],[19,24],[20,23],[19,23],[20,22],
    [19,22],[20,21],[19,21],[20,15],[19,15],[20,14],[19,14],[20,13],[19,13],
    [20,12],[19,12],[20,11],[19,11],[20,10],[19,10],[20,9],[19,9],[18,9],
    [17,9],[18,10],[17,10],[18,11],[17,11],[18,12],[17,12],[18,13],[17,13],
    [18,14],[17,14],[18,15],[17,15],[18,21],[17,21],[18,22],[17,22],[18,23],
    [17,23],[18,24],[17,24],[16,24],[15,24],[16,23],[15,23],[16,22],[15,22],
    [16,21],[15,21],[15,20],[15,19],[15,18],[15,17],[15,16],[16,15],[15,15],
    [16,14],[15,14],[16,13],[15,13],[16,12],[15,12],[16,11],[15,11],[16,10],
    [15,10],[16,9],[15,9],[16,8],[15,8],[16,7],[15,7],[16,5],[15,5],[16,4],
    [15,4],[16,3],[15,3],[16,2],[15,2],[16,1],[15,1],[16,0],[15,0],[14,0],
    [13,0],[14,1],[13,1],[14,2],[13,2],[14,3],[13,3],[14,4],[13,4],[14,5],
    [13,5],[14,7],[13,7],[14,8],[13,8],[14,9],[13,9],[14,10],[13,10],[14,11],
    [13,11],[14,12],[13,12],[14,13],[13,13],[14,14],[13,14],[14,15],[13,15],
    [14,16],[13,16],[14,17],[13,17],[14,18],[13,18],[14,19],[13,19],[14,20],
    [13,20],[14,21],[13,21],[14,22],[13,22],[14,23],[13,23],[14,24],[13,24],
    [12,24],[11,24],[12,23],[11,23],[12,22],[11,22],[12,21],[11,21],[12,20],
    [11,20],[12,19],[11,19],[12,18],[11,18],[12,17],[11,17],[12,16],[11,16],
    [12,15],[11,15],[12,14],[11,14],[12,13],[11,13],[12,12],[11,12],[12,11],
    [11,11],[12,10],[11,10],[12,9],[11,9],[12,8],[11,8],[12,7],[11,7],[12,5],
    [11,5],[12,4],[11,4],[12,3],[11,3],[12,2],[11,2],[12,1],[11,1],[12,0],
    [11,0],[10,0],[9,0],[10,1],[9,1],[10,2],[9,2],[10,3],[9,3],[10,4],[9,4],
    [10,5],[9,5],[10,7],[9,7],[10,8],[9,8],[10,9],[9,9],[10,10],[9,10],[10,11],
    [9,11],[10,12],[9,12],[10,13],[9,13],[10,14],[9,14],[10,15],[9,15],[10,16],
    [9,16],[10,17],[9,17],[10,18],[9,18],[10,19],[9,19],[10,20],[9,20],[10,21],
    [9,21],[10,22],[9,22],[10,23],[9,23],[10,24],[9,24],[8,16],[7,16],[8,15],
    [7,15],[8,14],[7,14],[8,13],[7,13],[8,12],[7,12],[8,11],[7,11],[8,10],
    [7,10],[8,9],[7,9],[5,9],[4,9],[5,10],[4,10],[5,11],[4,11],[5,12],[4,12],
    [5,13],[4,13],[5,14],[4,14],[5,15],[4,15],[5,16],[4,16],[3,16],[2,16],
    [3,15],[2,15],[3,14],[2,14],[3,13],[2,13],[3,12],[2,12],[3,11],[2,11],
    [3,10],[2,10],[3,9],[2,9],[1,9],[0,9],[1,10],[0,10],[1,11],[0,11],[1,12],
    [0,12],[1,13],[0,13],[1,14],[0,14],[1,15],[0,15],[1,16],[0,16]]
    bit_positions[3] = [[28,28],[27,28],[28,27],[27,27],[28,26],[27,26],[28,25],[27,25],[28,24],[27,24],[28,23],[27,23],[28,22],[27,22],[28,21],[27,21],[28,20],[27,20],[28,19],[27,19],[28,18],[27,18],[28,17],[27,17],[28,16],[27,16],[28,15],[27,15],[28,14],[27,14],[28,13],[27,13],[28,12],[27,12],[28,11],[27,11],[28,10],[27,10],[28,9],[27,9],[26,9],[25,9],[26,10],[25,10],[26,11],[25,11],[26,12],[25,12],[26,13],[25,13],[26,14],[25,14],[26,15],[25,15],[26,16],[25,16],[26,17],[25,17],[26,18],[25,18],[26,19],[25,19],[26,20],[25,20],[26,21],[25,21],[26,22],[25,22],[26,23],[25,23],[26,24],[25,24],[26,25],[25,25],[26,26],[25,26],[26,27],[25,27],[26,28],[25,28],[24,28],[23,28],[24,27],[23,27],[24,26],[23,26],[24,25],[23,25],[24,19],[23,19],[24,18],[23,18],[24,17],[23,17],[24,16],[23,16],[24,15],[23,15],[24,14],[23,14],[24,13],[23,13],[24,12],[23,12],[24,11],[23,11],[24,10],[23,10],[24,9],[23,9],[22,9],[21,9],[22,10],[21,10],[22,11],[21,11],[22,12],[21,12],[22,13],[21,13],[22,14],[21,14],[22,15],[21,15],[22,16],[21,16],[22,17],[21,17],[22,18],[21,18],[22,19],[21,19],[22,25],[21,25],[22,26],[21,26],[22,27],[21,27],[22,28],[21,28],[20,28],[19,28],[20,27],[19,27],[20,26],[19,26],[20,25],[19,25],[19,24],[19,23],[19,22],[19,21],[19,20],[20,19],[19,19],[20,18],[19,18],[20,17],[19,17],[20,16],[19,16],[20,15],[19,15],[20,14],[19,14],[20,13],[19,13],[20,12],[19,12],[20,11],[19,11],[20,10],[19,10],[20,9],[19,9],[20,8],[19,8],[20,7],[19,7],[20,5],[19,5],[20,4],[19,4],[20,3],[19,3],[20,2],[19,2],[20,1],[19,1],[20,0],[19,0],[18,0],[17,0],[18,1],[17,1],[18,2],[17,2],[18,3],[17,3],[18,4],[17,4],[18,5],[17,5],[18,7],[17,7],[18,8],[17,8],[18,9],[17,9],[18,10],[17,10],[18,11],[17,11],[18,12],[17,12],[18,13],[17,13],[18,14],[17,14],[18,15],[17,15],[18,16],[17,16],[18,17],[17,17],[18,18],[17,18],[18,19],[17,19],[18,20],[17,20],[18,21],[17,21],[18,22],[17,22],[18,23],[17,23],[18,24],[17,24],[18,25],[17,25],[18,26],[17,26],[18,27],[17,27],[18,28],[17,28],[16,28],[15,28],[16,27],[15,27],[16,26],[15,26],[16,25],[15,25],[16,24],[15,24],[16,23],[15,23],[16,22],[15,22],[16,21],[15,21],[16,20],[15,20],[16,19],[15,19],[16,18],[15,18],[16,17],[15,17],[16,16],[15,16],[16,15],[15,15],[16,14],[15,14],[16,13],[15,13],[16,12],[15,12],[16,11],[15,11],[16,10],[15,10],[16,9],[15,9],[16,8],[15,8],[16,7],[15,7],[16,5],[15,5],[16,4],[15,4],[16,3],[15,3],[16,2],[15,2],[16,1],[15,1],[16,0],[15,0],[14,0],[13,0],[14,1],[13,1],[14,2],[13,2],[14,3],[13,3],[14,4],[13,4],[14,5],[13,5],[14,7],[13,7],[14,8],[13,8],[14,9],[13,9],[14,10],[13,10],[14,11],[13,11],[14,12],[13,12],[14,13],[13,13],[14,14],[13,14],[14,15],[13,15],[14,16],[13,16],[14,17],[13,17],[14,18],[13,18],[14,19],[13,19],[14,20],[13,20],[14,21],[13,21],[14,22],[13,22],[14,23],[13,23],[14,24],[13,24],[14,25],[13,25],[14,26],[13,26],[14,27],[13,27],[14,28],[13,28],[12,28],[11,28],[12,27],[11,27],[12,26],[11,26],[12,25],[11,25],[12,24],[11,24],[12,23],[11,23],[12,22],[11,22],[12,21],[11,21],[12,20],[11,20],[12,19],[11,19],[12,18],[11,18],[12,17],[11,17],[12,16],[11,16],[12,15],[11,15],[12,14],[11,14],[12,13],[11,13],[12,12],[11,12],[12,11],[11,11],[12,10],[11,10],[12,9],[11,9],[12,8],[11,8],[12,7],[11,7],[12,5],[11,5],[12,4],[11,4],[12,3],[11,3],[12,2],[11,2],[12,1],[11,1],[12,0],[11,0],[10,0],[9,0],[10,1],[9,1],[10,2],[9,2],[10,3],[9,3],[10,4],[9,4],[10,5],[9,5],[10,7],[9,7],[10,8],[9,8],[10,9],[9,9],[10,10],[9,10],[10,11],[9,11],[10,12],[9,12],[10,13],[9,13],[10,14],[9,14],[10,15],[9,15],[10,16],[9,16],[10,17],[9,17],[10,18],[9,18],[10,19],[9,19],[10,20],[9,20],[10,21],[9,21],[10,22],[9,22],[10,23],[9,23],[10,24],[9,24],[10,25],[9,25],[10,26],[9,26],[10,27],[9,27],[10,28],[9,28],[8,20],[7,20],[8,19],[7,19],[8,18],[7,18],[8,17],[7,17],[8,16],[7,16],[8,15],[7,15],[8,14],[7,14],[8,13],[7,13],[8,12],[7,12],[8,11],[7,11],[8,10],[7,10],[8,9],[7,9],[5,9],[4,9],[5,10],[4,10],[5,11],[4,11],[5,12],[4,12],[5,13],[4,13],[5,14],[4,14],[5,15],[4,15],[5,16],[4,16],[5,17],[4,17],[5,18],[4,18],[5,19],[4,19],[5,20],[4,20],[3,20],[2,20],[3,19],[2,19],[3,18],[2,18],[3,17],[2,17],[3,16],[2,16],[3,15],[2,15],[3,14],[2,14],[3,13],[2,13],[3,12],[2,12],[3,11],[2,11],[3,10],[2,10],[3,9],[2,9],[1,9],[0,9],[1,10],[0,10],[1,11],[0,11],[1,12],[0,12],[1,13],[0,13],[1,14],[0,14],[1,15],[0,15],[1,16],[0,16],[1,17],[0,17],[1,18],[0,18],[1,19],[0,19],[1,20],[0,20]]

    
    def __init__(self, error, input):
        
        self.mode_char = 'N' if input.isdigit() else 'A'
        self.input = input if self.mode_char == 'N' else input.upper()   
        self.error_char = error.upper()
        self.version = 0
        
        # calculate version of QR code
        for i in range(1, 4, 1):
            if len(self.input) <= (self.TABLE_7_9[i][self.error_char]
                    [self.mode_char]):
                self.version = i 
                break
        if self.version > 3:
            print('ERROR: INPUT IS TOO LONG FOR THIS SCRIPT TO PROCESS, ' \
                'TRY REDUCING ERROR CORRECTION, OR SHORTEN INPUT.')
            sys.exit()
            
        # get data codewords
        stream = self.get_stream(self.version, self.mode_char, self.error_char, self.input)
        
        # generate a blank QR code
        code = self.generate_blank_array(self.version)
        for i in range(len(stream)):
            x = self.bit_positions[self.version][i][1]
            y = self.bit_positions[self.version][i][0]
            code[x][y] = int(stream[i])
        
        # perform masking
        candidates = [[column[:] for column in code] for n in range(8)]
        mask_patterns = [self.get_mask(self.version, p) for p in range(8)]
        for x in range((self.version * 4) + 17):
            for y in range((self.version * 4) + 17):
                for n in range(8):
                    candidates[n][x][y] = code[x][y] if mask_patterns[n][x][y] == 0 else 1 if code[x][y] == 0 else 0
        
        # score each of these masking options
        scores = [0 for n in range(8)]
        for n in range(8):
            scores[n] += self.test_one(candidates[n])
            scores[n] += self.test_two(candidates[n])
            scores[n] += self.test_three(candidates[n])
            scores[n] += self.test_four(candidates[n])
        lowest_index = scores.index(min(scores))
        
        # create a QR code SVG image with the lowest scoring mask pattern
        format = self.FORMAT_INFORMATION[self.error_char][lowest_index]
        self.create_svg_code(candidates[lowest_index], 'code', format, self.version)

        
    def get_stream(self, version, mode_char, error_char, input):
        # get all of the data codewords
        data_codewords = self.generate_data_codewords(version, mode_char, 
            error_char, input)
        # depending on the version/error correction level of the QR 
        # code we may need to split the data and error codewords into 
        # a number of blocks
        stream = ''
        if(version == 3 and (error_char == 'Q' or error_char == 'H')):
            # we require more than one block
            # as we're only coding upto version 3 we will only need a maximum 
            # of two blocks. These two blocks of data are then interleaved.
            data_blocks = [[]] * self.TABLE_9[version][error_char]['BLOCKS']
            data_blocks[0] = data_codewords[:self.TABLE_9[version][error_char]['DATA']]
            data_blocks[1] = data_codewords[self.TABLE_9[version][error_char]['DATA']:]
            data_zip = [value for sub_list in [[data_blocks[0][i], data_blocks[1][i]] for i in range(len(data_blocks[0]))] for value in sub_list]
            # The same applies to the error correction codewords, these are 
            # interleaved and then the 'zipped' error correction codewords 
            # are appended to the 'zipped' data codewords.
            # When more than one block is used, the error correction codewords
            # are calculated on each data codeword block, therefore the 
            # generate error codewords method is called twice in this case. This 
            # not necessary for the data codewords, this is just called once, 
            # whatever number of blocks we're using.
            error_blocks = [[]] * self.TABLE_9[version][error_char]['BLOCKS']
            for i in range(2):
                error_blocks[i] = self.generate_error_codewords(version, error_char, data_blocks[i])
            error_zip = [value for sub_list in [[error_blocks[0][i], error_blocks[1][i]] for i in range(len(error_blocks[0]))] for value in sub_list]
            stream = ''.join([format(d, '08b') for d in data_zip]) + ''.join([format(d, '08b') for d in error_zip])
        else:
            error_codewords = self.generate_error_codewords(version, error_char, 
                data_codewords)
            data_codewords = [format(d, '08b') for d in data_codewords]
            error_codewords = [format(v, '08b') for v in error_codewords]
            stream = ''.join(data_codewords) + ''.join(error_codewords)
        # if a QR version greater than two is used we need to append 7 remainder bits
        # this changes depending on the version used but for version 2 and 3 we add 
        # seven remainder bits.
        if self.version > 1:
            stream += '0000000'
        return stream
        
        
    def generate_data_codewords(self, version, mode_char, error_char, input):
        # Add the mode indicator.
        stream = '0001' if mode_char == 'N' else '0010'
        # Add the character count indicator.
        stream += format(len(input),'09b' if mode_char == 'A' else '010b')
        # Begin encoding of data.
        if mode_char == 'A':
            stream += self.encode_alphanumeric(input)
        else:
            stream += self.encode_numeric(input)
        # Add up to four terminator zeros.
        reqd_bit_length = self.TABLE_7_9[version][error_char]['D'] * 8
        stream += '0000' if reqd_bit_length - len(stream) >= 4 else ('0' *
            (reqd_bit_length - len(stream)))
        # Make data stream length a multiple of eight.
        mod_8 = len(stream) % 8
        extra_zeros = 8 - mod_8 if mod_8 != 0 else 0 
        stream += '0' * extra_zeros
        # Add pad bytes to fill capacity.
        number_of_pad_bytes = int((reqd_bit_length - len(stream)) / 8) 
        for i in range(number_of_pad_bytes):
            stream += '11101100' if i % 2 == 0 else '00010001'
        # Return the data codewords as a series of 8 bit bytes
        return [int(stream[i:i+8], 2) for i in range(0, len(stream), 8)]
        
        
    def generate_error_codewords(self, version, error_char, message):
        to_int = [1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19,
        38, 76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 
        192, 157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 
        159, 35, 70, 140, 5, 10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111,
        222, 161, 95, 190, 97, 194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 
        60, 120, 240, 253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 
        163, 91, 182, 113, 226, 217, 175, 67, 134, 17, 34, 68, 136, 13, 26, 52,
        104, 208, 189, 103, 206, 129, 31, 62, 124, 248, 237, 199, 147, 59, 118,
        236, 197, 151, 51, 102, 204, 133, 23, 46, 92, 184, 109, 218, 169, 79, 
        158, 33, 66, 132, 21, 42, 84, 168, 77, 154, 41, 82, 164, 85, 170, 73, 
        146, 57, 114, 228, 213, 183, 115, 230, 209, 191, 99, 198, 145, 63, 126,
        252, 229, 215, 179, 123, 246, 241, 255, 227, 219, 171, 75, 150, 49, 98,
        196, 149, 55, 110, 220, 165, 87, 174, 65, 130, 25, 50, 100, 200, 141, 
        7, 14, 28, 56, 112, 224, 221, 167, 83, 166, 81, 162, 89, 178, 121, 242,
        249, 239, 195, 155, 43, 86, 172, 69, 138, 9, 18, 36, 72, 144, 61, 122,
        244, 245, 247, 243, 251, 235, 203, 139, 11, 22, 44, 88, 176, 125, 250,
        233, 207, 131, 27, 54, 108, 216, 173, 71, 142, 1]
        to_alpha = [None, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 
        199, 75, 4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8,
        76, 113, 5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18,
        130, 69, 29, 181, 194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77,
        228, 114, 166, 6, 191, 139, 98, 102, 221, 48, 253, 226, 152, 37, 179,
        16, 145, 34, 136, 54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19,
        92, 131, 56, 70, 64, 30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 40,
        84, 250, 133, 186, 61, 202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 
        229, 172, 115, 243, 167, 87, 7, 112, 192, 247, 140, 128, 99, 13, 103,
        74, 222, 237, 49, 197, 254, 24, 227, 165, 153, 119, 38, 184, 180, 124,
        17, 68, 146, 217, 35, 32, 137, 46, 55, 63, 209, 91, 149, 188, 207, 205,
        144, 135, 151, 178, 220, 252, 190, 97, 242, 86, 211, 171, 20, 42, 93,
        158, 132, 60, 57, 83, 71, 109, 65, 162, 31, 45, 67, 216, 183, 123, 164,
        118, 196, 23, 73, 236, 127, 12, 111, 246, 108, 161, 59, 82, 41, 157, 
        85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203, 89, 95, 176, 156, 
        169, 160, 81, 11, 245, 22, 235, 122, 117, 44, 215, 79, 174, 213, 233, 
        230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175]
        e_num = self.TABLE_9[version][error_char]['ERROR']
        generator = []
        if e_num == 7:
            generator = [0, 87, 229, 146, 149, 238, 102, 21]
        elif e_num == 10:
            generator = [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45]
        elif e_num == 13:
            generator = [0, 74, 152, 176, 100, 86, 100, 106, 104, 130, 
            218, 206, 140, 78]
        elif e_num == 15:
            generator = [0, 8, 183, 61, 91, 202, 37, 51, 58, 58, 237, 140, 
            124, 5, 99, 105]
        elif e_num == 16:
            generator = [0, 120, 104, 107, 109, 102, 161, 76, 3, 91, 191, 147, 
            169, 182, 194, 225, 120]
        elif e_num == 17:
            generator = [0, 43, 139, 206, 78, 43, 239, 123, 206, 214, 147, 24, 
            99, 150, 39, 243, 163, 136]
        elif e_num == 18:
            generator = [0, 215, 234, 158, 94, 184, 97, 118, 170, 79, 187, 152,
            148, 252, 179, 5, 98, 96, 153]
        elif e_num == 22:
            generator = [0, 210, 171, 247, 242, 93, 230, 14, 109, 221, 53, 200,
            74, 8, 172, 98, 80, 219, 134, 160, 105, 165, 231]
        elif e_num == 26:
            generator = [0, 173, 125, 158, 2, 103, 182, 118, 17, 145, 201, 111,
            28, 165, 53, 161, 21, 245, 142, 13, 102, 48, 227, 153, 145, 218, 70]
        elif e_num == 28:
            generator = [0, 168, 223, 200, 104, 224, 234, 108, 180, 110, 190, 
            195, 147, 205, 27, 232, 201, 21, 43, 245, 87, 42, 195, 212, 119, 
            242, 37, 9,123]
        elif e_num == 36:
            generator = [0, 200, 183, 98, 16, 172, 31, 246, 234, 60, 152, 115, 24,
            167, 152, 113, 248, 238, 107, 18, 63, 218, 37, 87, 210, 105, 177, 120,
            74, 121, 196, 117, 251,113, 233, 30, 120]
        elif e_num == 44:
            generator = [0, 190, 7, 61, 121, 71, 246, 69, 55, 168, 188, 89, 243, 
            191, 25, 72, 123, 9, 145, 14, 247, 1, 238, 44, 78, 143, 62, 224, 126, 
            118, 114, 68, 163, 52, 194, 217, 147, 204, 169, 37, 130, 113, 102, 73, 181]
        result_a = []
        result_b = []
        for i in range(1, len(message)+1, 1):
            # Lead exponent of message in first run and result of XOR in
            # subsequent runs. If the alpha exponent is None, set it to zero.
            # this means we'll just be using the generator polynomial directly.
            alpha = to_alpha[message[0]] if i == 1 else to_alpha[result_b[0]]
            alpha = alpha if alpha is not None else 0
            # Multiply lead term with generator.
            for exp in generator:
                plus = exp + alpha
                mod = plus if plus < 256 else plus % 255
                result_a.append(to_int[mod])   
            # Part is either message on first run, or result of xor in 
            # subsequent runs
            part = [v for v in message] if i == 1 else [v for v in result_b]
            # Equalise the length of arrays, then XOR.
            maxcount = max(len(result_a), len(part))
            result_a += [0] * ((maxcount - len(result_a)) if (maxcount - len(result_a)) > 0 else 0)
            part += [0] * ((maxcount - len(part)) if (maxcount - len(part)) > 0 else 0)
            xor = [result_a[i] ^ part[i] for i in range(len(result_a))]
            # Discard the first zero term.
            result_b = xor[1:]        
            # Reset the result of multiplying lead term with generator.
            result_a = []
        # Return the array of error correction integers
        return result_b

        
    def generate_blank_array(self, version):
        # Generates a blank 2d array, complete with finder patterns
        # alignment patterns, timer patterns and the black pixel.
        length = (version * 4) + 17
        array = [[0 for y in range(length)] for x in range(length)]
        black_indices = self.generate_finder_with_start(0, 0)
        black_indices += self.generate_finder_with_start(length - 7, 0)
        black_indices += self.generate_finder_with_start(0, length - 7)
        black_indices += self.generate_timers(length)
        if version > 1:
            black_indices += self.generate_alignment_with_start(length - 9,
                length - 9)
        black_indices += [[8, length - 8]]
        for pixel in black_indices:
            array[pixel[0]][pixel[1]] = 1
        return array
        
    
    def flip_array_diagonally(self, array):
        # Useful function for flipping the array if you wish to export the 
        # QR code to a CSV file for example.
        a = [[array[x][y] for y in range(len(array))] for x in 
            range(len(array))]
        n = len(a)
        for x in range(0, n):
            for y in range(x+1, n):
                a[x][y], a[y][x] = a[y][x], a[x][y]
        return a
        
    def generate_finder_with_start(self, x, y):
        return [[x, y], [x+1, y], [x+2, y], [x+3, y], [x+4, y], [x+5, y], 
        [x+6, y], [x, y+1], [x+6, y+1], [x, y+2], [x+2, y+2], [x+3, y+2], 
        [x+4, y+2], [x+6, y+2], [x, y+3], [x+2, y+3], [x+3, y+3], [x+4, y+3], 
        [x+6, y+3], [x, y+4], [x+2, y+4], [x+3, y+4], [x+4, y+4], [x+6, y+4], 
        [x, y+5], [x+6, y+5], [x, y+6], [x+1, y+6], [x+2, y+6], [x+3, y+6], 
        [x+4, y+6], [x+5, y+6], [x+6, y+6]]
    
    def generate_alignment_with_start(self, x, y):
        return [[x, y], [x+1, y], [x+2, y], [x+3, y], [x+4, y], [x, y+1], 
        [x+4, y+1], [x, y+2], [x+2, y+2], [x+4, y+2], [x, y+3], [x+4, y+3], 
        [x, y+4], [x+1, y+4], [x+2, y+4], [x+3, y+4], [x+4, y+4]]
    
    def generate_timers(self, length):
        indices = [[x, 6] for x in range(8, length - 8, 2)]
        indices += [[6, y] for y in range(8, length - 8, 2)]
        return indices
        
    def encode_alphanumeric(self, input):
        TABLE_5 = {
        '0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, 
        '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15, 'G':16, 
        'H':17, 'I':18, 'J':19, 'K':20, 'L':21, 'M':22, 'N':23, 'O':24, 'P':25,
        'Q':26, 'R':27, 'S':28, 'T':29, 'U':30, 'V':31, 'W':32, 'X':33, 'Y':34,
        'Z':35, ' ':36, '$':37, '%':38, '*':39, '+':40, '-':41, '.':42, '/':43,
        ':':44}
        # Split stream into pairs, get values, multiple first by 45 and add to 
        # second, convert to 11 bit stream.  If final 'pair' only consists of 
        # one value, convert this to a 6 bit stream.
        stream = ''
        for i in range(0, len(input), 2):
            pair = input[i : i + 2].upper()
            if len(pair) == 2:
                p1 = TABLE_5[pair[0]] * 45
                p2 = TABLE_5[pair[1]]
                stream += format(p1 + p2, '011b')
            else:
                p1 = TABLE_5[pair[0]]
                stream += format(p1, '06b')
        return stream
    
    
    def encode_numeric(self, input):
        stream = ''
        for i in range(0, len(input), 3):
            triple = input[i:i+3]
            if len(triple) == 3:
                stream += format(int(triple), '010b')
            elif len(triple) == 2:
                stream += format(int(triple), '07b')
            else:
                stream += format(int(triple), '04b')
        return stream
                
    def encode_byte(self, input):
        TABLE_6 = {' ':32,'!':33,'"':34,'#':35,'$':36,'%':37,'&':38,'(':40,')':41,'*':42,'+':43,',':44,'-':45,'.':46,'/':47,'0':48,'1':49,'2':50,'3':51,'4':52,'5':53,'6':54,'7':55,'8':56,'9':57,':':58,';':59,'<':60,'=':61,'>':62,'?':63,'@':64,'A':65,'B':66,'C':67,'D':68,'E':69,'F':70,'G':71,'H':72,'I':73,'J':74,'K':75,'L':76,'M':77,'N':78,'O':79,'P':80,'Q':81,'R':82,'S':83,'T':84,'U':85,'V':86,'W':87,'X':88,'Y':89,'Z':90,'[':91,'\\':92,']':93,'^':94,'_':95,'`':96,'a':97,'b':98,'c':99,'d':100,'e':101,'f':102,'g':103,'h':104,'i':105,'j':106,'k':107,'l':108,'m':109,'n':110,'o':111,'p':112,'q':113,'r':114,'s':115,'t':116,'u':117,'v':118,'w':119,'x':120,'y':121,'z':122,'{':123,'|':124,'}':125,'~':126,'£':163,'§':167,'±':177}
        stream = ''
        for i in range(len(input)):
            stream += format(TABLE_6[input[i]], '08b')
        return stream
        
    
    def create_svg_code(self, array, filename, format_string, version):
        svg = SVG()
        cell_size = 20
        svg_size = cell_size * (len(array) + 8)
        svg.prep_for_drawing(svg_size, svg_size)
        length = (4 * version) + 17
        # Bottom right format information
        br = [[x, 8] for x in range(length - 1, length - 9, -1)]
        br += [[8, y] for y in range(length - 7, length, 1)]
        for i in range(len(br)):
            x = br[i][0]
            y = br[i][1]
            if(format_string[i] == '1'):
                svg.add_coloured_rect(x*20, y*20, 'rgb(0, 0, 0);')
        # Top left format information.
        tl = [[8, y] for y in range(0,9)]
        tl += [[x, 8] for x in range(7,-1,-1)]
        c = 0
        for i in range(len(tl)):
            x = tl[i][0]
            y = tl[i][1]
            if not ((x == 6 and y == 8) or (x == 8 and y == 6)):
                if(format_string[c] == '1'):
                    svg.add_coloured_rect(x*20, y*20, 'rgb(0, 0, 0);')
                c+=1
        for x in range(len(array)):
            for y in range(len(array[x])):
                if(array[x][y]) == 1:
                    svg.add_rect(x*20, y*20)
        svg.save(filename + '.svg')
    
    def get_mask(self, version, n):
        # Generate the mask.
        length = (version * 4) + 17
        mask = [[self.get_mask_pixel(x, y, n) for y in range(length)] for x in range(length)]
        # Remove masking where it does not apply, including finder patterns,
        # timer strips, alignment patterns and format information and of course
        # the dark pixel.
        finder_start = (version * 4) + 9
        unmask_array = [[x, y] for x in range(9) for y in range(9)]
        unmask_array += [[x, y] for x in range(finder_start, length, 1) for y in range(9)]
        unmask_array += [[x, y] for x in range(9) for y in range(finder_start, length, 1)]
        unmask_array += [[6, y] for y in range(length)]
        unmask_array += [[x, 6] for x in range(length)]
        if version > 1:
            align_start = length - 9
            unmask_array += [[x, y] for x in range(align_start, align_start + 5, 1) for y in range(align_start, align_start + 5, 1)]
        for coordinate in unmask_array:
            mask[coordinate[0]][coordinate[1]] = 0
        # Returns a 2D masking pattern array.
        return mask
        
    def get_mask_pixel(self, x, y, n):
        if n == 0:
            return 1 if (x+y)%2 == 0 else 0
        elif n == 1:
            return 1 if x%2 == 0 else 0
        elif n == 2:
            return 1 if y%3 == 0 else 0
        elif n == 3:
            return 1 if (x+y)%3 == 0 else 0
        elif n == 4:
            return 1 if (math.floor(x/2.0) + math.floor(y/3.0))%2 == 0 else 0
        elif n == 5:
            return 1 if (x*y)%2+(x*y)%3 == 0 else 0
        elif n == 6:
            return 1 if ((x*y)%2+(x*y)%3)%2 == 0 else 0
        elif n == 7:
            return 1 if ((x+y)%2+(x*y)%3)%2 == 0 else 0
        else:
            return 0
        
    def test_one(self, a):
        current = None
        previous = None
        count = 0
        score = 0
        for x in range(len(a)): # columns
            for y in range(len(a)):
                current = a[x][y]
                if current is not previous and previous is not None:
                    if count >= 5:
                        score += (3 + (count - 5))
                    count = 1
                else:
                    count += 1
                previous = current
            count = 0
            previous = None
        count = 0
        current = None
        previous = None
        for y in range(len(a)): # rows
            for x in range(len(a)):
                current = a[x][y]
                if current is not previous and previous is not None:
                    if count >= 5:
                        score += (3 + (count - 5))
                    count = 1
                else:
                    count += 1
                previous = current
            count = 0
            previous = None        
        return score
        
    def test_two(self, a):
        penalty = 0
        for x in range(len(a)):
            for y in range(len(a[0])):
                penalty += self.block_search(a, [x, y], [1, 1])
        return penalty
        
    def block_search(self, a, start, dim):
        # prevent out of bounds, find what the max value may be.
        x_ok = True if (start[0] + dim[0] + 1) < len(a) else False
        y_ok = True if (start[1] + dim[1] + 1) < len(a[0]) else False
        check_for = 1 if a[start[0]][start[1]] == 0 else 1
        if x_ok and y_ok:
            testall = [a[x][y] for x in range(start[0], start[0] + dim[0] + 1, 1) for y in range(start[1], start[1] + dim[1] + 1)]
            if check_for not in testall:
                return self.block_search(a, start, [dim[0] + 1, dim[1] + 1])
        if x_ok:
            testx = [a[x][y] for x in range(start[0], start[0] + dim[0] + 1, 1) for y in range(start[1], start[1] + dim[1], 1)]
            if check_for not in testx:
                return self.block_search(a, start, [dim[0] + 1, dim[1]])
        if y_ok:
            testy = [a[x][y] for x in range(start[0], start[0] + dim[0], 1) for y in range(start[1], start[1] + dim[1] + 1, 1)]
            if check_for not in testy:
                return self.block_search(a, start, [dim[0], dim[1] + 1])
        return 3 * (dim[0] - 1) * (dim[1] -1)
       
    def test_three(self, a):
        condition_one = '00001011101'
        condition_two = '10111010000'
        for x in range(len(a)): # columns
            for y in range(len(a)-12):
                check_word = ''.join([str(a[x][j]) for j in range(y, y + 12, 1)])
                if check_word == condition_one or check_word == condition_two:
                    return 40
        for x in range(len(a)-12): # rows
            for y in range(len(a)):
                check_word = ''.join([str(a[i][y]) for i in range(x, x + 12, 1)])
                if check_word == condition_one or check_word == condition_two:
                    return 40
        return 0
        
    def test_four(self, a):
        black_pixels = 0
        for x in a:
            for y in x:
                if y == 1:
                    black_pixels += 1
        percent_black = (black_pixels / float(len(a) * len(a))) * 100
        lower_multiple = percent_black - (percent_black % 5)
        upper_multiple = percent_black - (percent_black % 5) + 5
        return min(abs(lower_multiple - 50) / 5.0, abs(upper_multiple - 50) / 5.0) * 10
    
QR('H', 'http://www.paul-reed.co.uk')

















