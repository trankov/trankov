# Convert line-breaked text to paragraphs.

import re



COMMON_FLAGS = re.IGNORECASE|re.MULTILINE # = 10


def unbreak(n):
    """Removes non-paragraph line breaks"""
    
    return re.sub(pattern = r'([^.!?])($\n)',
            repl = r'\g<1> ', 
            string = n, count = 0, 
            flags = COMMON_FLAGS)


def typographer(n):
    """Replace ... to … , -- to — (emdash), " -" in line beginning to "— " (emdash and space) """
    
    repl_set = (
        (r'--', r'—'),
        (r'^-\s', r'^— '),
        (r'(\.{3})([\s\n\r])', r'…\g<2>'),
    )   
    for x in repl_set:
        n = re.sub(x[0], x[1], n, 0, COMMON_FLAGS)
    
    return n


def qouter(n):
    """Set « » instead of " " """
    
    lquote_match = r'([\s^])"'
    rquote_match = r'"([.,!?:;…\n\s\r$])'
    n = re.sub(rquote_match, r'»\g<1>', n, 0, COMMON_FLAGS)
    n = re.sub(lquote_match, r'\g<1>«', n, 0, COMMON_FLAGS)
    return n


def total_prettify(n):
    """Step-by-step convertion"""
    
    return unbreak(
        typographer(
            qouter(n)
        )
    )



if __name__ == '__main__':
    n = '''
"Победоносцев".
Написать эти тринадцать букв,
сливающихся в сочетание, столь роковое и
несчастное для русского народа, очень легко... Но
-- дальше-то что же? Когда я взялся сделать
характеристику г. Победоносцева в его
политической, общественной и литературной
деятельности, -- задача представлялась мне весьма
простою. 
'''
    print (total_prettify(n))
    
