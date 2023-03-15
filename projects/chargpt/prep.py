from collections import defaultdict
from tqdm import tqdm
from json import load, dump
import re

def add_to_name(file_name: str, str_to_add: str) -> str:
    return file_name.replace('.', f'_{str_to_add}.')

d = defaultdict(int)

file_name = "wr.txt"
clean_file_name = add_to_name(file_name, 'clean')
encoded_file_name = add_to_name(file_name, 'dataset')


def clear_line(text: str) -> str:
    text = text.lower()
    text = text.replace('[/quote]', '')
    text = re.sub(r'[a-z]', '', text)
    text = re.sub(r'([^а-я])', r' \g<1> ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clear_file():
    freq_threshhold = 5

    with open(file_name, 'r', encoding='utf-8') as f:
        freq = defaultdict(int)
        with open(clean_file_name, 'w', encoding='utf-8') as f_clean:
            for l in tqdm(f, desc='Cleaning'):
                clean = clear_line(l)
                f_clean.write(f"{clean}\n")
                for t in clean.split():
                    freq[t] += 1
        with open(f'freq.json', 'w', encoding='utf-8') as f_freq:
            freq = { k: v for k, v in sorted(freq.items(), reverse=True, key=lambda x: x[1]) }
            dump(freq, f_freq, indent=2, ensure_ascii=False)

    # freq filtering
    with open(clean_file_name, 'r', encoding='utf-8') as f_clean:
        flines = f_clean.readlines()
    with open(clean_file_name, 'w', encoding='utf-8') as f_clean:
        for l in tqdm(flines, desc='Freq filtering'):
            do_write = True
            for w in l.split():
                if freq[w] < freq_threshhold:
                    do_write = False
                    break
            if do_write:
                f_clean.write(l)

    # removing empty comments
    print("Removing empty comments")
    with open(clean_file_name, 'r', encoding='utf-8') as f_clean:
        full_text = f_clean.read()
    with open(clean_file_name, 'w', encoding='utf-8') as f_clean:
        f_clean.write(re.sub(r'(\[ \]\n){2,}', '[ ]\n', full_text))

def form_dicts():
    valid_utf8 = []
    for i in range(0x0, 0x10FFFF):
        try:
            utf8_char = chr(i).encode("utf-8")
            valid_utf8.append(utf8_char.decode("utf-8"))
        except UnicodeEncodeError:
            pass

    print(f"{len(valid_utf8)} valid characters generated")

    with open(clean_file_name, 'r', encoding='utf-8') as f:
        lexicon = set(f.read().split())
        lexicon.add('\n')
    ttos = { t:s for s,t in zip(valid_utf8, lexicon) }
    stot = { s:t for s,t in zip(valid_utf8, lexicon) }

    print(len(lexicon), ' unique tokens')

    with open(f'ttos.json', 'w', encoding='utf-8') as f:
        dump(ttos, f, indent=2, ensure_ascii=False)
    with open(f'stot.json', 'w', encoding='utf-8') as f:
        dump(stot, f, indent=2, ensure_ascii=False)

    return ttos, stot

def encode_dataset():
    with open('ttos.json', 'r', encoding='utf-8') as f:
        ttos = load(f)

    with open(clean_file_name, 'r', encoding='utf-8') as f:
        with open(encoded_file_name, 'w', encoding='utf-8') as f_encoded:
            for line in tqdm(f, desc='Encoding'):
                f_encoded.write(''.join([ttos[x] for x in line.split()]) + ttos['\n'])


clear_file()
form_dicts()
encode_dataset()

#print([ itos[x] for x in range(20) ])
#print(len(stoi.items()), len(itos.items()))
