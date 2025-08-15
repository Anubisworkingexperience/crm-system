document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector('.register-form');
  if (!form) return;

  document.querySelector('.register-form').addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log('file loaded');
  
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    try {
      const res = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
  
      if (!res.ok) {
        const error = await res.json();
        console.log(error.detail || "Registration failed");
        return;
      }
  
      const data = await res.json();
      localStorage.setItem("token", data.access_token);
  
      // redirect
      window.location.href = "../pages/dashboard.html";
    } catch (err) {
      console.error(err);
      console.log("Network error");
    }
  });
});

