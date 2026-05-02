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
  "Economics",
  "Political Science",
  "Psychology",
  "Engineering",
  "Biology",
  "History",
  "English",
  "Mathematics",
  "Neuroscience",
  "Chemical Engineering",
  "Mechanical Engineering",
  "Biomedical Engineering",
  "Statistics",
  "Philosophy",
  "Anthropology",
  "Sociology",
  "Art History",
  "Creative Writing",
  "Film & Media Studies"
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

  const resultsDiv = document.getElementById("results");

  const sliders = {
  language: document.getElementById("langSlider").value,
  arts: document.getElementById("artSlider").value,
  humanities: document.getElementById("humSlider").value,
  social_science: document.getElementById("socSlider").value,
  natural_science: document.getElementById("natSlider").value,
  stem: document.getElementById("stemSlider").value
};


  if (!major) {
    resultsDiv.innerHTML = "<p style='color:red;'>Please select a major.</p>";
    return;
  }

  // 2. Show loading message
  resultsDiv.innerHTML = "<p>Loading recommendations...</p>";

  const userData = {
    major: major,
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

      const title = document.createElement("b");
      title.textContent = course.name;

      const score = document.createElement("div");
      score.textContent = "Score: " + course.score;

      div.appendChild(title);
      div.appendChild(score);

      resultsDiv.appendChild(div);
    });

  } catch (error) {
    // 5. Handle errors
    resultsDiv.innerHTML = "<p style='color:red;'>Error connecting to server.</p>";
    console.error(error);
  }
}