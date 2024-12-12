const totalDays = 252; 
const colors = ["#a8d5e2", "#6495ed", "#4682b4", "#0f3552"]; // Light blue to dark blue
const activityLevels = [
    "User was not active",
    "User logged in once",
    "User logged in twice",
    "User logged in more than twice"
];
const daysContainer = document.getElementById("days-container");

// Generate list of dates for the last 252 days
const today = new Date();
const dates = Array.from({ length: totalDays }, (_, i) => {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    return date.toISOString().split('T')[0]; // Format: YYYY-MM-DD
}).reverse(); // Reverse to display oldest first

// Create a hash function for deterministic randomization
function hashCode(str) {
    return str.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
}

// Create day blocks
for (let i = 0; i < totalDays; i++) {
    const dayDiv = document.createElement("div");

    // Use the hash of the date to pick a random color index
    const colorIndex = hashCode(dates[i]) % colors.length;

    dayDiv.className = "day";
    dayDiv.style.backgroundColor = colors[colorIndex];
    dayDiv.style.position = "relative";

    // Tooltip for activity status
    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    tooltip.textContent = `${dates[i]}: ${activityLevels[colorIndex]}`;
    tooltip.style.position = "absolute";
    tooltip.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
    tooltip.style.color = "white";
    tooltip.style.padding = "5px";
    tooltip.style.borderRadius = "5px";
    tooltip.style.fontSize = "12px";
    tooltip.style.whiteSpace = "nowrap";
    tooltip.style.visibility = "hidden"; // Hide tooltip by default
    tooltip.style.bottom = "110%"; // Show above the box
    tooltip.style.left = "50%";
    tooltip.style.transform = "translateX(-50%)";

    dayDiv.appendChild(tooltip);

    // Show tooltip on hover
    dayDiv.addEventListener("mouseenter", () => {
        tooltip.style.visibility = "visible";
    });

    // Hide tooltip when not hovering
    dayDiv.addEventListener("mouseleave", () => {
        tooltip.style.visibility = "hidden";
    });

    daysContainer.appendChild(dayDiv);
}
