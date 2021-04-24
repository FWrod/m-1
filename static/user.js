/* COPY PROFILE PAGE BUTTON VARIABLES */
    let copy_button = document.getElementById('copy-link-button');

/* QRCODE GENERATOR VARIABLES */
    let qrcode_button = document.getElementById("qrcode-button");

/* QRCODE MODAL VARIABLES */
    let close_modal = document.getElementById("close-modal");
    let modal = document.getElementById("modal");

/* COPY LINK FUNCTION */
    copy_button.addEventListener('click', () => {
        let element = document.createElement('input'),
        location = window.location.href;

        document.body.appendChild(element); 
        element.value = location;
        element.select();
        document.execCommand('copy');
        document.body.removeChild(element);

        copy_button.innerHTML = '<svg class="mr-1 fill-current text-white" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"><path d="M9 21.035l-9-8.638 2.791-2.87 6.156 5.874 12.21-12.436 2.843 2.817z"/></svg>' + 'Altlink Copied'; 
    });

/* MODAL FUNCTION */
    function modal_event(){
        if(modal.style.display === "block"){
            modal.style.display = "none";

        } else {
            modal.style.display = "block";
        };
    };

/* QRCODE MODAL EVENT */
    qrcode_button.addEventListener("click", () => {
        modal_event();
    });

    close_modal.addEventListener("click", () => {
        modal_event();
    });

    