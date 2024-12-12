const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});
// JavaScript for the instructor and student sign-in selection
document.getElementById('instructor-btn').addEventListener('click', function () {
  console.log('You selected to sign in as Instructor');
});

document.getElementById('student-btn').addEventListener('click', function () {
  console.log('You selected to sign in as Student');
});

// JavaScript for the instructor and student sign-up selection
document.getElementById('instructor-signup-btn').addEventListener('click', function () {
  console.log('You selected to sign up as Instructor');
});

document.getElementById('student-signup-btn').addEventListener('click', function () {
  console.log('You selected to sign up as Student');
});

