import json
from cw_tokenize import cw_tokenize

parse_map = {
    'game_files/00_astral_rifts':               'cw_json/astral-rift.json',
    ('game_files/astral_rifts_0_events.txt',
     'game_files/astral_rifts_1_events.txt',
     'game_files/astral_rifts_2_events.txt',
     'game_files/astral_rifts_3_events.txt'): 'cw_json/astral-events-0.json'
}

def dict_merge(a: dict, b: dict):
    for key in b:
        if key in a:
            if isinstance(a[key], list) and isinstance(b[key], list):
                a[key] = [*a[key], *b[key]]
            else:
                a[key] = [a[key], b[key]]
            continue
        a[key] = b[key]

print('Parsing Files:')
for src, dst in parse_map.items():
    if isinstance(src, tuple):
        print(f'\tGroup:')
        output = {}
        for fp in src:
            print(f'\t\t{fp:<40}' if fp != src[-1] else f'\t\t{fp:<40}\t->\t\t{dst}')
            dict_merge(output, cw_tokenize(fp))
    else:
        print(f'\t{src:<40}\t\t->\t\t{dst}')
        output = cw_tokenize(src)
    with open(dst, 'w+') as f:
        f.write(json.dumps(output, indent=4))
