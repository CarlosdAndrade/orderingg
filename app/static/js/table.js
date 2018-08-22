

/*
     * Inicializa la tabla.
     *
     * @param {Object} config configuracion de la tabla
     *  Es un objecto con los siguientes atributos:
     *
     *  - `el` selector css que indica donde se va a renderizar la tabla
     *  - `data` Objecto con los datos de la tabla.
     */
function init(config) {       /**12:10  warning solo dice que define una variable q no se usa */
    const $el = document.querySelector(config.el);
    let data = config.data;

    // Si es una promise nos pasaron datos desde una api
    // cuando la promise se resuelve, renderizamos nuevamente
    // la tabla
    if (config.data instanceof Promise) {
        config.data.then(function (data) {
            render($el, data);
        });
    } else {
        data = {};
    }

    render($el, data);

    return {
        update: render.bind(null, $el)
    };
}

/**
     * Renderiza la tabla en `$el`;
     *
     * @param {HTMLElement} $el elemento donde se va a renderizar la tabla
     * @param {Object} data datos de la tabla
     */
function render($el, data) {
    $el.innerHTML = template(data);
}
/** LA MAYORIA DE LOS ERRORES EN ESTA TABLA FUERON DE SANGRIA */