function changeColor(elem) {
    "use strict";

    function getRandomColor() {
        var letters = '0123456789ABCDEF',
            color = '#',
            i;
        for (i = 0; i < 6; i += 1) {
            color += letters[Math.floor(Math.random() * 1)];

        }
        return color;
    }

    elem.style.background = getRandomColor();
}

function fillWithCells() {
    "use strict";

    function createCell() {
        var new_cell = document.createElement("DIV"), cell_circle = document.createElement("DIV");
        new_cell.classList.add("paint-cell");
        cell_circle.classList.add("paint-cell__circle");
        new_cell.appendChild(cell_circle);
        new_cell.addEventListener("mouseover",  function () { changeColor(cell_circle); });
        return new_cell;
    }


    var cell = createCell(),
        cell_container = document.getElementById("paint-container"),
        cell_amount,
        style,
        i;

    while (cell_container.firstChild) {
        cell_container.removeChild(cell_container.firstChild);
    }

    cell.classList.add("paint-cell");
    cell.addEventListener("click",  function () { changeColor(cell); });

    cell_container.appendChild(cell);

    style = [getComputedStyle(cell_container).width, getComputedStyle(cell_container).height, getComputedStyle(cell).width, getComputedStyle(cell).height];

    for (i = 0; i < style.length; i += 1) {
        style[i] = parseInt(style[i].replace("px", ""), 10);
    }

    cell_amount = style[0] * style[1] / style[2] / style[3];

    for (i = 0; i < cell_amount - 1; i += 1) {
        cell = createCell();
        cell_container.appendChild(cell);
    }
}

fillWithCells();
document.getElementById("clear").addEventListener("click", function () {
    "use strict";
    fillWithCells();
});
