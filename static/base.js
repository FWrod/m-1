let loading = document.getElementById("loading");
let menu_button = document.getElementById("menu-button");
let div_menu = document.getElementById("div-menu");
let hamburguer_button = document.getElementById("hamburguer-button");
let close_button = document.getElementById("close-button");

window.onload = function(){ 
    loading.style.display = "none";
}
                
function display_event(){
    if(div_menu.style.display === "flex"){
        div_menu.style.display = "none";
        close_button.style.display = "none";
        hamburguer_button.style.display = "inherit";
    } else {
        div_menu.style.display = "flex";
        close_button.style.display = "flex";
        hamburguer_button.style.display = "none";
    };
};

menu_button.addEventListener("click", () => {
    display_event();
});