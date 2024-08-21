
//Este código implementa un flujo de pago básico, que implica la recopilación de datos del cliente, la creación de un intento de pago en el servidor y la confirmación del pago con Stripe en el lado del cliente.

//Se crea una instancia de Stripe utilizando la clave pública (STRIPE_PUBLISHABLE_KEY) proporcionada por Stripe.
var stripe = Stripe(STRIPE_PUBLISHABLE_KEY);


var elem = document.getElementById('submit');
//Obtención del Cliente Secret:
//Se obtiene el Cliente Secret necesario para confirmar el pago. Este valor se genera en el servidor 
//y se almacena en el atributo data-secret
clientsecret = elem.getAttribute('data-secret');

//Configuración de Stripe Elements:
//Se configuran los elementos de Stripe (en este caso, un elemento de tarjeta de crédito) 
//el elemento se incluye en el contenedor con id card-element.
var elements = stripe.elements();
var style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};


var card = elements.create("card", { style: style });
card.mount("#card-element");

//Gestión de Cambios en la Tarjeta:
//Se añade un escuchador de eventos para detectar cambios en el elemento de la tarjeta.
// Si hay errores, se muestran mensajes de error.
card.on('change', function(event) {
var displayError = document.getElementById('card-errors')
if (event.error) {
  displayError.textContent = event.error.message;
  $('#card-errors').addClass('alert alert-info');
} else {
  displayError.textContent = '';
  $('#card-errors').removeClass('alert alert-info');
}
});

var form = document.getElementById('payment-form');

///Envío del Formulario:
//Se añade un escuchador de eventos al formulario 
//para interceptar el envío del formulario estándar y realizar acciones personalizadas.
form.addEventListener('submit', function(ev) {
ev.preventDefault();

////Preparación de Datos del Cliente:
//Se recopilan datos adicionales del formulario y se agregan al objeto FormData.
//Se incluye el Cliente Secret, el token CSRF y la acción que se realizará.
var custName = document.getElementById("id_full_name").value;
var custAdd = document.getElementById("id_address1").value;
var custAdd2 = document.getElementById("id_address2").value;
var custEmail = document.getElementById("id_email").value;
var custContact = document.getElementById("id_contact_no").value;


var formData = new FormData(form);

formData.append('order_key', clientsecret);
formData.append('csrfmiddlewaretoken', CSRF_TOKEN);
formData.append('action', 'post');

////Envío de la Solicitud AJAX:
//Se realiza una solicitud AJAX al servidor (http://127.0.0.1:8000/orders/add/) con los datos del formulario y el Cliente Secret. El servidor debe procesar esta solicitud para crear un intento de pago.

  $.ajax({
    type: "POST",
    url: 'http://127.0.0.1:8000/orders/add/',
    data: formData,
    contentType: false,
    processData: false,
    success: function (json) {
      //Procesamiento del Pago con Stripe:
      //Si la solicitud al servidor tiene éxito, se confirma el pago utilizando stripe.confirmCardPayment. 
      //Se incluye la información de la tarjeta y los detalles del cliente. Si el pago es exitoso, 
      //se redirige al usuario a la página de confirmación (http://127.0.0.1:8000/payment/orderplaced/).
      console.log(json.success)

      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address:{
                line1:custAdd,
                line2:custAdd2, 
            },
            name: custName,
            email: custEmail,
            phone: custContact
          },
        }

      }).then(function(result) {
        //Manejo de Errores:
        //Se manejan posibles errores durante el proceso de pago y se muestran mensajes de error en la consola.
        if (result.error) {

          console.log('payment error')
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
          // Existe el riesgo de que el cliente cierre la ventana antes de la devolución de llamada
          // ejecución. Configure un webhook o complemento para escuchar el
          // evento Payment_intent.succeeded que maneja cualquier negocio crítico
           // acciones pospago.
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
          }
        }
      });

    },
    error: function (xhr, errmsg, err) {},
  });



});