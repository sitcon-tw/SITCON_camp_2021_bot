import json
import random

point_codes_list = []
point_codes_10 = []
point_codes_20 = []
point_codes_30 = []

def generate(times, point_codes):
    for i in range(100):
        tmp_string = ""
        for j in range(10):
            tmp = random.randint(0, 61)
            if tmp < 10:
                tmp_string += chr(tmp+48)
            elif tmp < 36:
                tmp_string += chr(tmp+65-10)
            else:
                tmp_string += chr(tmp+97-36)
        point_codes.append(tmp_string)

generate(100, point_codes_10)
generate(100, point_codes_20)
generate(100, point_codes_30)

point_codes_list.append(point_codes_10)
point_codes_list.append(point_codes_20)
point_codes_list.append(point_codes_30)

with open('pointCode.json', mode='w', encoding='utf-8') as jfile:
    json.dump(point_codes_list, jfile)

