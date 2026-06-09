document.addEventListener("DOMContentLoaded", () => {

    const phoneInputs = document.querySelectorAll(".phone-mask");


    phoneInputs.forEach((input) => {

        input.addEventListener("input", (event) => {

            let value = event.target.value;

            value = value.replace(/\D/g, "");


            if (value.length > 11) {
                value = value.slice(0, 11);
            }


            if (value.length > 10) {

                value = value.replace(
                    /^(\d{2})(\d{5})(\d{4}).*/,
                    "($1) $2-$3"
                );

            } else if (value.length > 6) {

                value = value.replace(
                    /^(\d{2})(\d{4})(\d{0,4}).*/,
                    "($1) $2-$3"
                );

            } else if (value.length > 2) {

                value = value.replace(
                    /^(\d{2})(\d{0,5})/,
                    "($1) $2"
                );

            } else {

                value = value.replace(
                    /^(\d*)/,
                    "($1"
                );
            }

            event.target.value = value;

        });

    });

});

const deleteButtons = document.querySelectorAll(
    ".open-delete-modal"
);


const deleteForm = document.getElementById(
    "deleteForm"
);


const deleteClientName = document.getElementById(
    "deleteClientName"
);


deleteButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const clientId = button.dataset.clientId;

        const clientName = button.dataset.clientName;


        deleteClientName.textContent = clientName;


        deleteForm.action = `/clients/${clientId}/delete`;

    });

});
