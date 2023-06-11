def paragraphize(text, n=5, delimiter='\n'):
    sentences = text.split('. ')
    assert len(sentences) >= n

    i = n
    blocks = []
    while i < len(sentences):
        block = '. '.join(sentences[i:i+n])
        block += f'.{delimiter}'
        blocks.append(block)
        i += n

    blocks[-1] = blocks[-1][:-1]
    return ''.join(blocks)
