document.addEventListener("DOMContentLoaded", () => {

  const form = document.querySelector(".login-form");
  if (!form) return;

  document.querySelector(".login-form").addEventListener("submit", async (e) => {
    e.preventDefault(); 
  
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const passwordError = document.querySelector(".wrong-password");
  
    try {
      const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
  
      if (!res.ok) {
        const error = await res.json();

        console.log(error.detail || "Login failed");
        console.log(res);
        console.log(error.detail, typeof error.detail)
        console.log(error.detail[0].type);
        if (error.detail == "Invalid credentials") {
          passwordError.textContent = "Неправильный логин/пароль";
        }
        else if (error.detail[0].type == "value_error") {
          console.log("Wrong data format");
          passwordError.textContent = "Введите данные в правильном формате";
        }
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
});
