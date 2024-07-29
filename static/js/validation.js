const validateCalle = (calle) => {
  if (!calle) return false;
  // length validation
  let lengthValid = calle.length <= 80;

  return lengthValid;
};

const validateTipo = (tipo) => {
  if (!tipo) return false;
  else return true;
};

const validateCantidad = (cantidad) => {
  if (!cantidad) return false;
  // length validation
  let lengthValid = cantidad.length <= 10;

  return lengthValid;
};

const validateDate = (date) => {
  const inputDate = new Date(date);
  const currentDate = new Date();
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  const isValidDate = regex.test(date);
  const isAfterCurrentDate = inputDate >= currentDate;
  return isValidDate && isAfterCurrentDate;
}

const validateDescripcion = (descripcion) => {
  if (descripcion){
    // length validation
    let lengthValid = descripcion.length <= 80;
    return lengthValid;
  }
  else{
    return true
  }
};

const validateCondiciones = (condiciones) => {
  if (condiciones){
    // length validation
    let lengthValid = condiciones.length <= 80;
    return lengthValid;
  }
  else{
    return true
  }
};

const validateFiles = (files) => {
  if (!files) return false;

  // number of files validation
  let lengthValid = 1 <= files.length && files.length <= 3;

  // file type validation
  let typeValid = true;

  for (const file of files) {
    // file.type should be "image/<foo>" or "application/pdf"
    let fileFamily = file.type.split("/")[0];
    typeValid &&= fileFamily == "image" || file.type == "application/pdf";
  }

  // return logic AND of validations.
  return lengthValid && typeValid;
};

const validateNombre = (nombre) => {
  if (!nombre) return false;
  // length validation
  let minLengthValid = nombre.length >= 3;
  let maxLengthValid = nombre.length <= 80;

  return minLengthValid && maxLengthValid;
};

const validateEmail = (email) => {
  if (!email) return false;
  // length validation
  let lengthValid = email.length >= 15;

  // format validation
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  // return logic AND of validations.
  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (phoneNumber) {
    // length validation
    let lengthValid = phoneNumber.length >= 8;
  
    // format validation
    let re = /^[0-9]+$/;
    let formatValid = re.test(phoneNumber);
  
    // return logic AND of validations.
    return lengthValid && formatValid;
  }
  else{
    return true
  }
};

function showSuccessMessage() {
  document.getElementById('agregar-donacion').reset(); 
  document.getElementById("ty_msg").removeAttribute('hidden'); // Muestra el mensaje de éxito
}

const validateForm = () => {
  // get elements from DOM by using form's name.
  let myForm = document.forms["agregar-donacion"];
  let calle = myForm["calle-numero"].value;
  let tipo = myForm["tipo"].value;
  let cantidad = myForm["cantidad"].value;
  let date = myForm["fecha-disponibilidad"].value;
  let descripcion = myForm["descripcion"].value;
  let condiciones = myForm["condiciones"].value;
  let files = myForm["files"].files;
  let nombre = myForm["nombre"].value;
  let email = myForm["email"].value;
  let phoneNumber = myForm["telefono"].value;
  
  
  // validation auxiliary variables and function.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  // validation logic
  if (!validateCalle(calle)) {
    setInvalidInput("Calle y número");
  }
  if (!validateTipo(tipo)) {
    setInvalidInput("Tipo");
  }
  if (!validateCantidad(cantidad)) {
    setInvalidInput("Cantidad");
  }
  if (!validateDate(date)) {
    setInvalidInput("Fecha");
  }
  if (!validateDescripcion(descripcion)) {
    setInvalidInput("Descripcion");
  }
  if (!validateCondiciones(condiciones)) {
    setInvalidInput("Condiciones");
  }
  if (!validateFiles(files)) {
    setInvalidInput("Foto(s)");
  }
  if (!validateNombre(nombre)) {
    setInvalidInput("Nombre");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email");
  }
  if (!validatePhoneNumber(phoneNumber)) {
    setInvalidInput("Teléfono");
  }
  

  // finally display validation
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");
  let confirm1 = document.getElementById("confirm1");
  let confirm2 = document.getElementById("confirm2");
  let confirm3 = document.getElementById("confirm3");
  let submitFinal = document.getElementById("submit-btn2");

  if (!isValid) {
    validationListElem.textContent = "";
    // add invalid elements to val-list element.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // set val-msg
    validationMessageElem.innerText = "Los siguientes campos son invalidos:";

    // make validation prompt visible
    validationBox.hidden = false;
    window.scrollTo(0, 0);

  } else {
    validationBox.hidden = true;
    confirm1.hidden = false;
    confirm2.hidden = false;
    confirm3.hidden = false;
    submitFinal.hidden = false;
    submitFinal.addEventListener("click", function() {
      myForm.submit();  
    });
  }
};

let submitBtn = document.getElementById("submit-btn1");
submitBtn.addEventListener("click", validateForm);

document.addEventListener("DOMContentLoaded", function() {
  let backToIndexBtn = document.getElementById("back-to-inicio-btn");
  backToIndexBtn.addEventListener("click", function() {
    window.location.href = indexUrl;
  });
});