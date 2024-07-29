import re
import filetype

def validate_calle(calle):
    if calle is None:
        return False
    valid = len(calle) <= 80
    return valid

def validate_tipo(tipo):
    if tipo is None:
        return False
    return True

def validate_cantidad(cantidad):
    if cantidad is None:
        return False
    valid = len(cantidad) <= 10
    return valid

def validate_descripcion(descripcion):
    if descripcion is None:
        return True
    valid = len(descripcion) <= 80
    return valid

def validate_descripcion2(descripcion):
    if descripcion is None:
        return False
    valid = len(descripcion) <= 250
    return valid

def validate_condiciones(condiciones):
    if condiciones is None:
        return True
    valid = len(condiciones) <= 80
    return valid

def validate_img(img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png"}
    # check if a file was submitted
    if img is None:
        return False

    # check if the browser submitted an empty file
    if img.filename == "":
        return False
    
    # check file extension
    ftype_guess = filetype.guess(img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validate_name(name):
    if name is None:
        return False
    valid = len(name) <= 80 and len(name) >= 3
    return valid

def validate_email(email):
    if email is None:
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone_number(phone_number):
    if phone_number is None:
        return True
    pattern = r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    return re.match(pattern, phone_number) is not None

def validate_date(date):
    if date is None:
        return False
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(pattern, date) is not None

def validate_donation_form(calle, tipo, cantidad, descripcion, condiciones, img, name, email, phone_number, date):

    if validate_calle(calle) is False:
        return False

    if validate_tipo(tipo) is False:
        return False

    if validate_cantidad(cantidad) is False:
        return False
    
    if validate_descripcion(descripcion) is False:
        return False
    
    if validate_condiciones(condiciones) is False:
        return False

    if validate_img(img) is False:
        return False

    if validate_name(name) is False:
        return False

    if validate_email(email) is False:
        return False
    
    if validate_phone_number(phone_number) is False:
        return False
    
    if validate_date(date) is False:
        return False

    return True


def validate_pedido_form(tipo, descripcion, cantidad, name, email, phone_number):
    if validate_tipo(tipo) is False:
        return False

    if validate_cantidad(cantidad) is False:
        return False
    
    if validate_descripcion2(descripcion) is False:
        return False

    if validate_name(name) is False:
        return False

    if validate_email(email) is False:
        return False
    
    if validate_phone_number(phone_number) is False:
        return False
    
    return True
