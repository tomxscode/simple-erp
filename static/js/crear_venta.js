fetch(`${SITIO}/api/empresa`, {
  method: 'GET'
})
  .then(response => response.json())
  .then(data => {
    let opcionesEmpresas = data.map(empresa => ({
      id: empresa.rut,
      text: `${empresa.nombre} | ${empresa.rut}`
    }));

    $(document).ready(function () {
      $('.select2').select2({
        data: opcionesEmpresas,
        placeholder: 'Selecciona una empresa',
        allowClear: true,
      });

      $('#empresa_mandante_select').on('change', function () {
        var seleccion = $(this).val();
        $('input[name="empresa_mandante"]').val(seleccion);
      });

      $('#empresa_venta_select').on('change', function () {
        var seleccion = $(this).val();
        $('input[name="empresa_venta"]').val(seleccion);
      });
    });
  })
  .catch(error => console.error(error));