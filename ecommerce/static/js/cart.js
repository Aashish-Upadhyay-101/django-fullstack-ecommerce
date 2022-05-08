const updateBtn = document.getElementsByClassName("update-cart");

for (let i = 0; i < updateBtn.length; i++) {
  updateBtn[i].addEventListener("click", function (event) {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    console.log(`product_id: ${productId}\naction: ${action}`);

    console.log("USER", user);

    if (user === "AnonymousUser") {
      console.log(
        "User is not authenticated, please login to perform this action"
      );
    } else {
      console.log("sending data to the backend");
    }
  });
}
