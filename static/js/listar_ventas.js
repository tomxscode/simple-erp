function infoVenta(idVenta) {
  Swal.fire({
    title: "Acciones",
    text: "¿Qué acción desea realizar? Recuerde que los cambios son irreversibles",
    // 2 botones: Eliminar y Editar
    showDenyButton: true,
    showCancelButton: true,
    confirmButtonText: "Editar",
    denyButtonText: "Eliminar",
    cancelButtonText: "Cancelar"
  }).then((result) => {
    if (result.isConfirmed) {
      console.log('editar')
    } else if (result.isDenied) {
      fetch(`/api/ventas`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id: idVenta
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          Swal.fire({
            title: "Venta eliminada",
            text: data.message,
            icon: "success"
          }).then(() => {
            location.reload();
          })
        } else {
          Swal.fire({
            title: "Error al eliminar la venta",
            text: data.message,
            icon: "error"
          })
        }
      })
    }
  })
}