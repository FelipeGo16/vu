let zoom = 100;

function zoomIn(){

    zoom += 10;

    document.body.style.zoom = zoom + "%";
}

function zoomOut(){

    zoom -= 10;

    document.body.style.zoom = zoom + "%";
}