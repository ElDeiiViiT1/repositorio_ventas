document.getElementById("informeForm").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const data = {
      nombre: document.getElementById("nombre").value,
      mes: document.getElementById("mes").value,
      participacion: document.getElementById("participacion").checked,
      cursos: document.getElementById("cursos").value,
      horas: document.getElementById("horas").value,
      comentarios: document.getElementById("comentarios").value
    };
  
    const response = await fetch('/enviar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
  
    if (response.ok) {
      alert("¡Informe enviado exitosamente!");
    } else {
      alert("Hubo un error al enviar el informe.");
    }
  });