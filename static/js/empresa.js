function infoEmpresa(id) {
  // Mostrar SweetAlert de carga
  Swal.fire({
      title: 'Cargando información...',
      allowOutsideClick: false,
      onBeforeOpen: () => {
          Swal.showLoading();
      },
  });

  // Hacer la solicitud fetch para obtener la información de la empresa
  fetch(`/api/empresa/${id}`)
      .then(response => response.json())
      .then(data => {
          // Cerrar SweetAlert de carga
          Swal.close();

          // Mostrar SweetAlert con la información obtenida
          Swal.fire({
              title: 'Información de la empresa',
              html: `Nombre: ${data.nombre}<br>Dirección: ${data.direccion}<br>Email: ${data.email}`,
              icon: 'info',
          });
      })
      .catch(error => {
          // Manejar errores
          Swal.close();
          Swal.fire({
              title: 'Error al cargar la información',
              text: 'Hubo un problema al obtener la información de la empresa.',
              icon: 'error',
          });
      });
}