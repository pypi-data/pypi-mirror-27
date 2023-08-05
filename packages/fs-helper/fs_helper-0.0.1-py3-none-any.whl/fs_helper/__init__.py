def lazy_filename(text, ext=''):
    """Return a filename string for the given text and optional extension (ext)

    - http://stackoverflow.com/a/7406369
    """
    # Strip out and replace some things in case text is a url
    text = text.split('://')[-1].strip('/').replace('/', '--')
    ext = '.{}'.format(ext) if ext else ''

    return "".join([
        c
        for c in text
        if c.isalpha() or c.isdigit() or c in (' ', '-', '_', '+', '.')
    ]).rstrip().replace(' ', '-') + ext
