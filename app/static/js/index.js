(function () {
    const $totalPrice = document.querySelector('#total-price');

    // Estado de la aplicacion
    const state = {
        products: API.getProducts(),
        selectedProduct: null,
        quantity: 0,
        order: API.getOrder()
    }
     
    const refs = {}
    /**
     * Actualiza el valor del precio total
     **/
    function updateTotalPrice() {
        const totalPrice = state.selectedProduct.price * state.quantity;
        $totalPrice.innerHTML = `Precio total: $ ${totalPrice}`
    }

     /**
     * Agrega un producto a una orden
     *
     **/
    function onAddProduct() {
        if(state.quantity >= 1){                //Si es una cantidad válida, acepta los valores y los carga
            API.addProduct(1, state.selectedProduct, state.quantity)
            .then(function (r) {
                if (r.error) {
                    console.error(r.error);
                } else {
                    API.getOrder().then(function (data) {
                        refs.table.update(data);
                    });

                    refs.modal.close();
                }
            });
        }else{                                  //Si es nulo o negativo, muestra mensaje de error
            alert("Error. No puede ingresarse una cantidad negativa o nula.");
        }
}

    /**
     * Inicializa la aplicacion
     **/
    function init() {
        Modal.init({
            el: '#modal',
            products: API.getProducts(),
            onProductSelect: function (selectedProduct) {
                state.selectedProduct = selectedProduct;
                updateTotalPrice();
            },
            onChangeQunatity: function (quantity) {
                state.quantity = quantity;
                updateTotalPrice();
            }
        });

        // Inicializamos la tabla
        Table.init({
            el: '#orders',
            data: API.getOrder()
        });
    }

    init();
})()

