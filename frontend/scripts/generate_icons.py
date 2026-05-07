import sys
from PIL import Image

try:
    img = Image.open('public/printerify.png')
    
    def make_square(im, size):
        im.thumbnail((size, size), Image.Resampling.LANCZOS)
        bg = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        bg.paste(im, ((size - im.width) // 2, (size - im.height) // 2))
        return bg

    make_square(img, 192).save('public/pwa-192x192.png')
    make_square(img, 512).save('public/pwa-512x512.png')
    
    def make_apple_icon(im, size):
        im.thumbnail((size, size), Image.Resampling.LANCZOS)
        bg = Image.new('RGB', (size, size), (255, 255, 255))
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            alpha = im.convert('RGBA').split()[3]
            bg.paste(im, ((size - im.width) // 2, (size - im.height) // 2), mask=alpha)
        else:
            bg.paste(im, ((size - im.width) // 2, (size - im.height) // 2))
        return bg

    make_apple_icon(img, 180).save('public/apple-touch-icon-180x180.png')
    print("Icons generated successfully.")
except Exception as e:
    print(f"Error: {e}")
