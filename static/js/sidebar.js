'use strict'

let arrow = document.querySelectorAll(".arrow");

for (var i = 0; i < arrow.length; i++) {
    arrow[i].addEventListener("click", (e)=>{

        let arrowParent = e.target.parentElement.parentElement;
         arrowParent.classList.toggle("showMenu");
    });
}

let sidebar = document.querySelector("#sidebarMenu");

$('.side').on('click', function () {
        sidebar.classList.toggle("close");
    });
