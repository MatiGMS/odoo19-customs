document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('.ws_info_input');
    
    inputs.forEach(input => {
        // 'change' dispara al quitar el foco de un input de texto, o al marcar un checkbox
        input.addEventListener('change', function (e) {
            const fieldName = e.target.name;
            // Si es checkbox capturamos su estado (true/false), sino su valor en texto
            const fieldValue = e.target.type === 'checkbox' ? e.target.checked : e.target.value;

            fetch('/shop/cart/update_ws_info', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    params: {
                        field_name: fieldName,
                        field_value: fieldValue
                    }
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.result && data.result.status === 'success') {
                    console.log(`Guardado exitoso: ${data.result.field}`);
                }
            })
            .catch(error => console.error('Error guardando dato de vendedor:', error));
        });
    });
});