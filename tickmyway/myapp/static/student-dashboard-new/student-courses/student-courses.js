document.querySelector(".upload-btn").addEventListener("click", () => {
    document.getElementById("file-upload").click();
});


document.getElementById("file-upload").addEventListener("change", (event) => {
    const file = event.target.files[0]; 
    
    if (file) {
        const notesUploaded = document.querySelector(".notes-uploaded");
        const fileDiv = document.createElement("div");
        fileDiv.className = "file-item";


        const uploadDate = new Date();
        const formattedDate = uploadDate.toLocaleString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        });


        fileDiv.innerHTML = `
            <span class="file-name">${file.name}</span>
            <span class="file-date">Uploaded on: ${formattedDate}</span>
            <button class="delete-btn">Delete</button>
        `;

        notesUploaded.appendChild(fileDiv);


        fileDiv.querySelector(".delete-btn").addEventListener("click", () => {
            fileDiv.remove();
        });
    }
});
