const API_URL = "http://localhost:8000"; // api gateway link
const token = localStorage.getItem("token");

if (!token) {
  window.location.href = "./login.html";
}

document.querySelector(".logout-button").addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "./login.html";
});

async function fetchCustomers() {
  const res = await fetch(`${API_URL}/customers`, {
    headers: { Authorization: `Bearer ${token}` }
  });

  if (!res.ok) {
    alert("Ошибка при загрузке клиентов");
    return;
  }

  const data = await res.json();
  renderCustomers(data.customers);
}

function renderCustomers(customers) {
  const clientList = document.querySelector(".clients");
  clientList.innerHTML = "";

  customers.forEach(c => {
    const client = document.createElement("div");
    client.className = "customer-card";

    const customerEmail = document.createElement('h3');
    customerEmail.textContent = c.email.toString() || "";
    client.appendChild(customerEmail);

    const createdAt = document.createElement('p');
    createdAt.textContent = `Создан: ${new Date(c.created_at).toLocaleString()}` || "";
    client.appendChild(createdAt);

        // Show orders button
        const ordersBtn = document.createElement("button");
        ordersBtn.textContent = "Заказы";
        ordersBtn.addEventListener("click", () => showOrders(c.id));
        client.appendChild(ordersBtn);
    
        // Create order button
        const createBtn = document.createElement("button");
        createBtn.textContent = "Создать заказ";
        createBtn.addEventListener("click", () => createOrder(c.id));
        client.appendChild(createBtn);
    
        // Edit button
        const editBtn = document.createElement("button");
        editBtn.textContent = "Изменить";
        editBtn.addEventListener("click", () => editCustomer(c.id, c.name, c.email));
        client.appendChild(editBtn);
    
        // Delete button
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Удалить";
        deleteBtn.addEventListener("click", () => deleteCustomer(c.id));
        client.appendChild(deleteBtn);
    
        // Orders container
        const ordersDiv = document.createElement("div");
        ordersDiv.id = `orders-${c.id}`;
        ordersDiv.className = "orders";
        client.appendChild(ordersDiv);
        
        clientList.appendChild(client);
  });
}

// Create customer
document.querySelector(".create-customer").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;

  const res = await fetch(`${API_URL}/customers`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ name, email })
  });

  if (res.ok) {
    fetchCustomers();
    e.target.reset();
  } else {
    alert("Ошибка при добавлении клиента");
  }
});

// Edit customer
async function editCustomer(id, oldName, oldEmail) {
  const name = prompt("Имя:", oldName);
  const email = prompt("Email:", oldEmail);
  if (!name || !email) return;

  const res = await fetch(`${API_URL}/customers/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ name, email })
  });

  if (res.ok) fetchCustomers();
}

// Delete customer
async function deleteCustomer(id) {
  if (!confirm("Удалить клиента?")) return;

  const res = await fetch(`${API_URL}/customers/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` }
  });

  if (res.ok) fetchCustomers();
}

// Show orders for a customer
async function showOrders(customerId) {
  const res = await fetch(`${API_URL}/orders?customer_id=${customerId}`, {
    headers: { Authorization: `Bearer ${token}` }
  });

  if (!res.ok) {
    alert("Ошибка при загрузке заказов");
    return;
  }

  const data = await res.json();
  const ordersDiv = document.getElementById(`orders-${customerId}`);
  ordersDiv.innerHTML = data.orders.map(o => `
    <div class="order">
      <p>${o.product_name} — ${o.price}₽ (${new Date(o.created_at).toLocaleString()})</p>
    </div>
  `).join("");
}

// Create order for a customer
async function createOrder(customerId) {
  const product = prompt("Название товара:");
  const price = parseFloat(prompt("Цена:"));
  if (!product || isNaN(price)) return;

  const res = await fetch(`${API_URL}/orders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ customer_id: customerId, product_name: product, price })
  });

  if (res.ok) {
    showOrders(customerId);
  } else {
    alert("Ошибка при создании заказа");
  }
}

// Initial load
fetchCustomers();
