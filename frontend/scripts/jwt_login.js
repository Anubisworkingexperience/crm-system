document.querySelector(".login-form").addEventListener("submit", async (e) => {
  e.preventDefault(); 

  const login = document.getElementById("login").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    if (!res.ok) {
      const error = await res.json();
      console.log(error.detail || "Login failed");
      return;
    }

    const data = await res.json();
    localStorage.setItem("token", data.access_token);

    // redirects
    window.location.href = "../pages/dashboard.html";
  } catch (err) {
    console.error(err);
    console.log("Network error");
  }
});