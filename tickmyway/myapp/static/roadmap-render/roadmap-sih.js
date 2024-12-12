const steps = {
    1: [
        "Understanding Variables and Data Types:        In Python, variables are used to store data values. The data types in Python include integers, floats, strings, and booleans. Each data type serves a different purpose and helps store information in a particular format. Python is dynamically typed, meaning you dont need to explicitly declare the data type of a variable.",
        "Basic Operators in Python:        Python supports various operators for performing mathematical, logical, and comparison operations. For example, arithmetic operators like +, -, *, and / are used for performing basic arithmetic, while comparison operators like ==, >, <, and != are used for making comparisons.",
        "Control Flow in Python:        Python provides conditional statements like if, elif, and else to control the flow of execution. These statements allow you to execute certain blocks of code based on specific conditions, enabling the creation of complex logic in programs.",
        "Functions in Python:Functions in Python allow you to encapsulate a block of reusable code. You can define functions using the def keyword and pass arguments to them. Functions help make code more modular and organized."
    ],
    2: [
        "Lists in Python:        Lists are one of the most commonly used data structures in Python. They are mutable, meaning elements can be added, removed, or changed. Lists are defined using square brackets, and the elements inside can be of any data type, including other lists.",
        "Tuples in Python:        Tuples are similar to lists but with one key difference: they are immutable. Once a tuple is created, its elements cannot be changed. Tuples are defined using parentheses and are often used for storing data that should not be modified.",
        "List Operations :Python provides several operations and methods for working with lists, such as adding elements with append(), removing elements with remove(), and slicing lists to access a portion of the data. Lists can also be nested to create more complex data structures.",
        "Tuple Operations:        While tuples do not support modification, they can still be used with various operations like concatenation and repetition. You can also access individual elements in a tuple using indexing, just like in lists."
    ],
    3: [
        "Step 3 Description 1",
        "Step 3 Description 2",
        "Step 3 Description 3",
        "Step 3 Description 4"
    ],
    4: [
        "Step 4 Description 1",
        "Step 4 Description 2",
        "Step 4 Description 3",
        "Step 4 Description 4"
    ],
    5:[
        "Step 5 Description 1",
        "Step 5 Description 2",
        "Step 5 Description 3",
        "Step 5 Description 4"
    ],
    6:[
        "Step 6 Description 1",
        "Step 6 Description 2",
        "Step 6 Description 3",
        "Step 6 Description 4"
    ],
    7:[
        "Step 7 Description 1",
        "Step 7 Description 2",
        "Step 7 Description 3",
        "Step 7 Description 4"
    ],
    8:[
        "Step 8 Description 1",
        "Step 8 Description 2",
        "Step 8 Description 3",
        "Step 8 Description 4"
    ],
    9:[
        "Step 9 Description 1",
        "Step 9 Description 2",
        "Step 9 Description 3",
        "Step 9 Description 4"
    ],
    10:[
        "Step 10 Description 1",
        "Step 10 Description 2",
        "Step 10 Description 3",
        "Step 10 Description 4"
    ]


    // Add descriptions for steps 3 to 10 similarly
};

const quizData = {
    1: [
        { question: "WHAT IS THE CORRECT WAY TO DEFINE A VARIABLE IN PYTHON", options: ["int x = 10", "x = 10", "10 = x", "var x = 10"], correct: "x = 10" },
        { question: "WHICH OPERATOR IS USED FOR DIVISION IN PYTHON", options: ["*", "/", "//", "%"], correct: "/" },
        { question: "WHAT DOES THE IF STATEMENT DO IN PYTHON", options: ["It repeats a block of code untill a conditoin is false", "It executes a block of code only if a condition is true.", "It executes a block of code only if a condition is true.", "It handles exceptions in the code."], correct: " It executes a block of code only if a condition is true." },
        { question: "Which of the following is the correct syntax for defining a function in Python?", options: ["function myFunc():", "def myFunc():", "func myFunc():", "function def myFunc():"], correct: "def myFunc():" },
    ],
    2: [
        { question: "Question 1 for Step 2?", options: ["A", "B", "C", "D"], correct: "C" }
    ]
    // Add quiz data for other steps
};

let currentStep = 1;
let currentDescription = 0;

function showStep(step) {
    currentStep = step;
    currentDescription = 0;
    updateInfoPane();
    highlightCurrentStep();
}

function updateInfoPane() {
    const infoPane = document.querySelector('.info-pane');
    infoPane.innerHTML = `
    <div class="discription">
        <div class="description-title"><p> Description ${currentDescription + 1}</p></div>
        <div class="discription-pop">
            <div class="description-content"> <p> ${steps[currentStep][currentDescription]}  </p> </div>
        </div>
        <div class="navigation-buttons">
            ${currentDescription > 0 ? '<button onclick="prevDescription()">Back</button>' : ''}
            ${currentDescription < steps[currentStep].length - 1 ? '<button onclick="nextDescription()">Next</button>' : '<button onclick="showQuiz()">Quiz</button>'}
        </div>
    </div>
    `;
}

function nextDescription() {
    currentDescription++;
    updateInfoPane();
}

function prevDescription() {
    currentDescription--;
    updateInfoPane();
}

function showQuiz() {
    const quiz = quizData[currentStep];
    if (!quiz) return;

    const infoPane = document.querySelector('.info-pane');
    const quizHTML = quiz.map((q, index) => `
        <div class="quiz-question">
            <p>${q.question}</p>
            ${q.options.map(option => `
                <label>
                    <input type="radio" name="q${index}" value="${option}"> ${option}
                </label>
            `).join('')}
        </div>
    `).join('');

    infoPane.innerHTML = `
        <div class="description-title">Quiz for Step ${currentStep}</div>
        ${quizHTML}
        <button class="submitting" onclick="submitQuiz()">Submit</button>
    `;
}

function submitQuiz() {
    const quiz = quizData[currentStep];
    let score = 0;

    // Check answers and calculate the score
    quiz.forEach((q, index) => {
        const selected = document.querySelector(`input[name="q${index}"]:checked`);
        if (selected && selected.value === q.correct) {
            score++;
        }
    });

    // Show score in an alert
    alert(`Your score is ${score}/${quiz.length}`);

    // If score is less than 2, do not proceed to the next step
    if (score < 2) {
        alert("Your score is too low to proceed. Please try again.");
    } else {
        completeStep();
    }
}


function completeStep() {
    const currentStepElement = document.querySelector(`.roadmap-item:nth-child(${currentStep * 2 - 1})`);

    // Mark the current step as completed with specific styles
    currentStepElement.classList.add('completed');
    currentStepElement.style.backgroundColor = 'black';
    currentStepElement.style.color = 'white';

    // Only move to the next step if the score was sufficient
    if (currentStep <= 10 && document.querySelector(`.roadmap-item:nth-child(${currentStep * 2 - 1})`).classList.contains('completed')) {
        currentStep++;
        showStep(currentStep);
    } else {
        document.querySelector('.info-pane').innerHTML = '<div>All steps completed!</div>';
    }
}

function highlightCurrentStep() {
    const steps = document.querySelectorAll('.roadmap-item');
    steps.forEach((item, index) => {
        // Reset styles for non-completed, non-active steps
        if (!item.classList.contains('completed')) {
            item.classList.remove('active');
            item.style.backgroundColor = ''; // Reset background
            item.style.color = ''; // Reset text color
        }

        // Apply active styles to the current step
        if (index === currentStep - 1 && !item.classList.contains('completed')) {
            item.classList.add('active');
            item.style.backgroundColor = '#8b4513'; // Green background
            item.style.color = 'antiquewhite'; // Antique white text
        }

        // Add a click event listener to each step
        item.onclick = () => {
            const stepNumber = index + 1; // Determine step from index
            showStep(stepNumber);
        };
    });
}

// Add to roadmap-sih.js
document.getElementById('file-upload').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name;
    if (fileName) {
        e.target.nextElementSibling.textContent = fileName;
    }
});

// Initialize the first step as active
highlightCurrentStep();
showStep(1);
