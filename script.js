async function getRecommendations() {
  // 1. Get user input
  const major = document.getElementById("major").value;
  const interests = document.getElementById("interests").value;
  const courses = document.getElementById("courses").value;

  const resultsDiv = document.getElementById("results");

  // 2. Show loading message
  resultsDiv.innerHTML = "<p>Loading recommendations...</p>";

  const userData = {
    major: major,
    interests: interests,
    courses: courses
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