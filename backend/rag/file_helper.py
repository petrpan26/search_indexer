from fastapi import HTTPException
import os
import fitz
import docx

FITZ_SUPPORTED_TYPE = ['pdf', 'xps', 'epub', 'mobi', 'fb2', 'cbz', 'svg']
DOCX_SUPPORTED_TYPE = ['docx']
PYTHON_SUPPORTED_TYPE = ['txt']

def read_with_fitz(filepath: str) -> str:
    try:
        with fitz.open(filepath) as doc:  # open document
            text = '\n'.join([page.get_text() for page in doc])
            return text
    except Exception as e:
        raise HTTPException(status_code=415, detail=f'File open fail with exception : {e}')

def read_with_docx(filepath: str) -> str:
    try:
        doc = docx.Document(filepath)
        allText = []
        for docpara in doc.paragraphs:
            allText.append(docpara.text)
        return '\n'.join([page.get_text() for page in doc])
    except Exception as e:
        raise HTTPException(status_code=415, detail=f'File open fail with exception : {e}')
    
def read_with_python(filepath: str) -> str:
    try:
        with open(filepath, 'r') as f:
            return '\n'.join(f.readlines())
    except Exception as e:
        raise HTTPException(status_code=415, detail=f'File open fail with exception : {e}')

def read_document_from_file(filepath: str) -> str:
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail='Internal error')
    
    extension = filepath.split('.')[-1]

    if extension in FITZ_SUPPORTED_TYPE:
        return read_with_fitz(filepath)
    if extension in DOCX_SUPPORTED_TYPE:
        return read_with_docx(filepath)
    if extension in PYTHON_SUPPORTED_TYPE:
        return read_with_python(filepath)
    
    raise HTTPException(status_code=415, detail='Document type not supported')