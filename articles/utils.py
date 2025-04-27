def normalize_text(text):
    if not text:
        return ""
    text = text.lower() 
    replacements = {
        'ú': 'u', 
        'ǵ': 'g',
        'ó': 'o',
        'á': 'a',
        'ń': 'n',
        'ı': 'i',
    }
    for src, dest in replacements.items():
        text = text.replace(src, dest)

    return text