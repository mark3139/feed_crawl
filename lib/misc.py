def str_md5(content):
    import hashlib
    m = hashlib.md5(content)
    return m.hexdigest()


def str_to_unicode(text, encoding=None, allow_none=False): # {{{
    """Return the unicode representation of text in the given encoding. Unlike
    .encode(encoding) this function can be applied directly to a unicode
    object without the risk of double-decoding problems (which can happen if
    you don't use the default 'ascii' encoding)
    Return none if the text is none and allow_none==True
    """

    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, str):
        return text.decode(encoding)
    elif isinstance(text, unicode):
        return text
    elif text is None and allow_none == True:
        return text
    else:
        raise TypeError('str_to_unicode must receive a str or unicode object, got %s' % type(text).__name__)
# end def }}}
