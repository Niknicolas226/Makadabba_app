const breakfastButton = document.getElementById("breakfast-button");
const lunchButton = document.getElementById("lunch-button");
const dinnerButton = document.getElementById("dinner-button");
const breakfastSection = document.getElementById("breakfast");
const lunchSection = document.getElementById("lunch");
const dinnerSection = document.getElementById("dinner");

breakfastButton.addEventListener("click", () => {
  breakfastSection.scrollIntoView({ behavior: "smooth" });
});


 
