// Get the login form element from the DOM
const loginForm = document.getElementById("Admin-form");

// Add an event listener to the form for when it is submitted
loginForm.addEventListener("submit", (event) => {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the input values from the form
    const OrganisationID = document.getElementById("OrganisationID").value;
    const password = document.getElementById("password").value;

    // Define the data to be sent to the backend
    const data = { OrganisationID: OrganisationID, password: password };
    

    // Send a POST request to the backend with the data
    fetch("/api/login", {
        method: "POST",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
    })
        .then((response) => response.json())
        .then((response) => {
            if (response.ok) {
              // Redirect to new page if response is successful
              window.location.href = "./registration.html";
            } else {
              // Handle error if response is not successful
              throw new Error("Error fetching login details");
            }
          })
        .then((data) => {
            console.log(data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
function redirectToNewPage() {
    window.location.href = "./registration.html"
}

