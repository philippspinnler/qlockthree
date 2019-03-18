def intro():
    owner = os.environ.get('QLOCKTHREE_OWNER')
    if not owner:
        return

    if owner == 'mayca':
        word = word_mayca
    elif owner == 'ken':
        word = word_ken

    for idx in range(len(word)):
        pixels.clear()
        for idx2 in range(0, idx + 1):
            pixels.set_pixel(word[idx2], get_color())
        pixels.show()
        time.sleep(1)
    time.sleep(4)