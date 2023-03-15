from json import load
from collections import defaultdict

stot = defaultdict(lambda: "unknown_token")

with open('stot.json', 'r', encoding='utf-8') as f:
    stot.update(load(f))

def decode(text: str) -> str:
    return ' '.join([stot[x] for x in text if x in stot])

if __name__ == "__main__":
    print(decode('晛蠓⑐𔑭𙐷Ž𑤶𕆌贼檡𑧿𑖻𕃨𔑭𚮮靘贼蠓𛑚𘎊𐁻﫴𓜩𕃨⯑꩟𒖼𕒋ࢅ𓭹贼蠓晛蠓۵𗝯ｗ𗸝ೢ𓩨ꮬﱛ𐜕檡圎𙸦ॣ𘙢𕶲𕃨獺𕃨➠篈𚣉𐁻𕃨𘴼𕌽綧𑴴𙴩⎎𒚑쁊۵蠓𛉖Ž㈺㣸贼⩽𑫯﫴𚧛𕃨𑫯𘟮늞𑤶껵凓𖚴贼𙟍靘𓶏㢑𙸦喃𒨅靘贼𗣏蠓'))
