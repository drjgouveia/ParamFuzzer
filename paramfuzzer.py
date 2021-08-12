import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Set input file", default=None)
parser.add_argument("-u", "--url", help="Input URL to FUZZ", type=str, default="")
args = parser.parse_args()

def param_extract(response, black_list="", placeholder="FUZZ"):
    '''
    Function to extract URLs with parameters (ignoring the black list extention)
    regexp : r'.*?:\/\/.*\?.*\=[^$]'

    '''

    parsed = list(set(re.findall(r'.*?:\/\/.*\?.*\=[^$]', response)))
    final_uris = []

    for i in parsed:
        delims = list()
        delims.append(i.find('='))

        while i.find("=", delims[len(delims) - 1] + 1) > -1:
            delims.append(i.find("=", delims[len(delims) - 1] + 1))

        if len(black_list) > 0:
            words_re = re.compile("|".join(black_list))
            if not words_re.search(i):
                for delim in delims:
                    final_uris.append((i[:delim + 1] + placeholder))
        else:
            for delim in delims:
                final_uris.append((i[:delim + 1] + placeholder))

    # for i in final_uris:
    #     k = [ele for ele in black_list if(ele in i)]

    return list(set(final_uris))


if __name__ == '__main__':
    if args.input is not None:
        with open(args.input, "r") as r:
            for line in r.readlines():
                for url in param_extract(line):
                    print(url)


    else:
        for url in param_extract(args.url):
            print(url)
