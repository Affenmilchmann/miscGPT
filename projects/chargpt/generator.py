from mingpt.model import GPT
from mingpt.bpe import BPETokenizer
import torch
from time import sleep
from projects.chargpt.chargpt import get_config
from projects.chargpt.chargpt import CharDataset

glob_cfg = get_config()
cfg = glob_cfg.model
cfg.vocab_size = 1132
cfg.block_size = 128

model = GPT(cfg)
model.load_state_dict(torch.load('out/chargpt/model.pt'))

with open('womanru.txt', 'r') as f:
    train_dataset = CharDataset(glob_cfg.data, f.read())

stoi = train_dataset.stoi
itos = train_dataset.itos

def generate(prompt='', steps=20, do_sample=True):
    x = torch.tensor([stoi[s] for s in prompt], dtype=torch.long)[None,...].to('cpu')

    # forward the model `steps` times to get samples, in a batch
    y = model.generate(x, max_new_tokens=steps, do_sample=do_sample, top_k=40)
    
    out = ''.join([itos[int(i)] for i in y[0]])
    return(out)
        

base = '[new]\n' + input(' >> ')
print()
steps = 1
#total = 50

print(base, end='', flush=True)

while True:
    #total -= steps
    base = generate(base, steps=steps)
    to_print = base[-steps:]
    print(to_print, end='', flush=True)
    if base.endswith('[new]'): break
    sleep(0.01)
print()

