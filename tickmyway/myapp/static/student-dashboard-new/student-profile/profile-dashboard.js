
    const totalDays = 252; 
    const colors = ["antiqueWhite", "#d2a679", "#a0522d", "#8b4513"]; 
    const daysContainer = document.getElementById("days-container");

    for (let i = 0; i < totalDays; i++) {
        const dayDiv = document.createElement("div");


        const colorIndex = i % colors.length; 
        dayDiv.style.backgroundColor = colors[colorIndex];

        const dayNumber = (i % 4) + 1; 
        dayDiv.className = `active-day${dayNumber}`;

        daysContainer.appendChild(dayDiv);
    }

