from bdfparser import Font

font = Font('unlearne.bdf')
print(f"This font's global size is "
      f"{font.headers['fbbx']} x {font.headers['fbby']} (pixel), "
      f"it contains {len(font)} glyphs.")

a = input()


def reverse_slicing(s):
    return s[::-1]


a_new = reverse_slicing(a)

phrase = font.draw(a_new, direction='rl').glow()
print(phrase)

from PIL import Image

im_ac = Image.frombytes('RGBA',
                        (phrase.width(), phrase.height()),
                        phrase.tobytes('RGBA'))
im_ac.save("ac.png", "PNG")


