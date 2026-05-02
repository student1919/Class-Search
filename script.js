document.querySelectorAll("input[type='range']").forEach(slider => {
  const outputId = slider.id.replace("Slider", "Val");
  const output = document.getElementById(outputId);


  // set initial value
  output.textContent = slider.value;

  // update on move
  slider.addEventListener("input", () => {
    output.textContent = slider.value;
  });
});


const majors = [
  "Computer Science",
  "Business Administration",
  "Biology",
  "Psychology",
  "Mechanical Engineering",
  "Economics",
  "Political Science",
  "English",
  "Mathematics",
  "Chemistry"
];

const majorDropdown = document.getElementById("major");

majors.forEach(major => {
  const option = document.createElement("option");
  option.textContent = major;
  option.value = major.toLowerCase().replace(/ /g, "_"); // for example: "computer_science"
  majorDropdown.appendChild(option);
});

async function getRecommendations() {
  // 1. Get user input
  const major = document.getElementById("major").value;
  const interests = document.getElementById("interests").value;
  const courses = document.getElementById("courses").value;

  const resultsDiv = document.getElementById("results");

  const sliders = {
  language: document.getElementById("langSlider").value,
  arts: document.getElementById("artSlider").value,
  humanities: document.getElementById("humSlider").value,
  social_science: document.getElementById("socSlider").value,
  natural_science: document.getElementById("natSlider").value,
  stem: document.getElementById("stemSlider").value
};

  // 2. Show loading message
  resultsDiv.innerHTML = "<p>Loading recommendations...</p>";

  const userData = {
    major: major,
    interests: interests,
    courses: courses,
    preferences: sliders
  };

  try {
    // 3. Send to backend (Flask, etc.)
    const response = await fetch("http://localhost:5000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(userData)
    });

    const data = await response.json();

    // 4. Display results
    resultsDiv.innerHTML = "<h3>Recommended Courses:</h3>";

    data.courses.forEach(course => {
      const div = document.createElement("div");
      div.className = "course";

      div.innerHTML = `
        <b>${course.name}</b><br>
        Score: ${course.score}
      `;

      resultsDiv.appendChild(div);
    });

  } catch (error) {
    // 5. Handle errors
    resultsDiv.innerHTML = "<p style='color:red;'>Error connecting to server.</p>";
    console.error(error);
  }
}