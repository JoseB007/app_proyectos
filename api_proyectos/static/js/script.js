function validarCampos() {
    var name = document.getElementById("nombre_proyecto").value;

    if (name.trim() === "") {
        alert("Por favor, escribe un nombre de proyecto");
        return false; // Devuelve false para evitar enviar el formulario
    }

    return true;
}

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth'
    });
    calendar.render();
  });

