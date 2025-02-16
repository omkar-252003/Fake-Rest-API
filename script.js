const API_AIRLINES = "https://api.instantwebtools.net/v1/airlines";
const API_PASSENGERS = "https://api.instantwebtools.net/v1/passenger";

// Fetch airlines and populate dropdown
async function fetchAirlines() {
    try {
        const res = await fetch(API_AIRLINES);
        const airlines = await res.json();

        const airlineDropdown = document.getElementById("airline");
        const filterDropdown = document.getElementById("filter-airline");

        airlines.forEach(airline => {
            const option = document.createElement("option");
            option.value = airline._id;
            option.textContent = airline.name;

            airlineDropdown.appendChild(option);
            filterDropdown.appendChild(option.cloneNode(true));
        });

        // Add manually required airlines
        const fixedAirlines = ["Haulmer", "American", "Sri Lankan"];
        fixedAirlines.forEach(name => {
            const opt = document.createElement("option");
            opt.textContent = name;
            filterDropdown.appendChild(opt);
        });
    } catch (error) {
        console.error("Error fetching airlines:", error);
    }
}

// Fetch and display passengers
async function fetchPassengers() {
    try {
        const res = await fetch(`${API_PASSENGERS}?size=100`);
        const data = await res.json();
        let passengers = data.data;

        // Apply filters
        const selectedAirline = document.getElementById("filter-airline").value;
        const minTrips = document.getElementById("filter-trips").value;

        passengers = passengers.filter(passenger => {
            let airlineMatch = !selectedAirline || passenger.airline[0]?.name.includes(selectedAirline);
            let tripsMatch = !minTrips || passenger.trips >= parseInt(minTrips);
            return airlineMatch && tripsMatch;
        });

        displayPassengers(passengers);
    } catch (error) {
        console.error("Error fetching passengers:", error);
    }
}

// Display passengers in table
function displayPassengers(passengers) {
    const table = document.getElementById("passenger-table");
    table.innerHTML = "";

    passengers.forEach(passenger => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${passenger.name}</td>
            <td>${passenger.trips}</td>
            <td>${passenger.airline[0]?.name || "N/A"}</td>
            <td>
                <button class="edit-btn" onclick="editPassenger('${passenger._id}', '${passenger.name}', ${passenger.trips})">Edit</button>
                <button class="delete-btn" onclick="deletePassenger('${passenger._id}')">Delete</button>
            </td>
        `;
        table.appendChild(row);
    });
}

// Add new passenger
async function addPassenger() {
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value;
    const airline = document.getElementById("airline").value;

    if (!name.match(/^[a-zA-Z ]+$/)) {
        alert("Name must contain only letters!");
        return;
    }
    if (age <= 0 || isNaN(age)) {
        alert("Age must be a positive number!");
        return;
    }

    const newPassenger = { name, trips: Math.floor(Math.random() * 100), airline };

    try {
        const res = await fetch(API_PASSENGERS, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newPassenger)
        });

        if (!res.ok) throw new Error("Failed to add passenger");

        alert("Passenger added successfully!");
        fetchPassengers();
    } catch (error) {
        console.error("Error adding passenger:", error);
    }
}

// Delete passenger (Fixed)
async function deletePassenger(id) {
    try {
        const res = await fetch(`${API_PASSENGERS}/${id}`, { method: "DELETE" });

        if (!res.ok) {
            alert("Failed to delete passenger!");
            return;
        }

        alert("Passenger deleted successfully!");
        fetchPassengers();
    } catch (error) {
        console.error("Error deleting passenger:", error);
    }
}

// Edit passenger inline
function editPassenger(id, currentName, trips) {
    const newName = prompt("Enter new name:", currentName);
    if (!newName || !newName.match(/^[a-zA-Z ]+$/)) {
        alert("Invalid name input!");
        return;
    }

    const updatedPassenger = { name: newName, trips };

    fetch(`${API_PASSENGERS}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedPassenger)
    })
        .then(res => {
            if (!res.ok) throw new Error("Failed to update passenger");
            alert("Passenger updated!");
            fetchPassengers();
        })
        .catch(error => console.error("Error updating passenger:", error));
}

// Initial Load
fetchAirlines();
fetchPassengers();
