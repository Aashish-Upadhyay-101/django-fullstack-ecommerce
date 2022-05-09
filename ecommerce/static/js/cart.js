const updateBtn = document.getElementsByClassName("update-cart");

for (let i = 0; i < updateBtn.length; i++) {
  updateBtn[i].addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    console.log(`product_id: ${productId}\naction: ${action}`);

    console.log("USER", user);

    if (user === "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      console.log("sending data to the backend");
      updateUserOrder(productId, action);
    }
  });
}

function addCookieItem(productId, action) {
  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productId]["quantity"] -= 1;

    if (cart[productId]["quantity"] <= 0) {
      delete cart[productId];
    }
  }

  console.log("Cart", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";

  location.reload();
}

function updateUserOrder(productId, action) {
  url = "/update-item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      product_id: productId,
      action: action,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      location.reload();
    });
}
