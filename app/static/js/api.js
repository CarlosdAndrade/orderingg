const API = (function () {
    /**
     * Obtiene una orden desde el backend
     *
     * @param {Number} orderId id de la orden
     */
    function getOrder(orderId) {
        return fetch('/order/1')
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Obtiene todos los productos desde el backend
     *
     */
    function getProducts() {
        return fetch('/product')
            .then(function toJson(r) {
                return r.json();
            });
    }

        function deleteProduct(orderId, productId) { /*Funcion que elimina producto de la DB*/
        return fetch(`/order/${ orderId }/product/${ productId }`,
            {
                method: 'DELETE'
            }
        )
        
        console.log('borro')
    }

    /**
     * Agrega un producto a una orden
     **/
    function addProduct(orderId, product, quantity) {
        const data = JSON.stringify({ quantity: quantity, product: product })

        return fetch(`/order/${ orderId }/product`,
            {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: data
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }



    return {
        getOrder,
        getProducts,
        addProduct,
        deleteProduct
    }
})()