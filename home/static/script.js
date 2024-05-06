document.getElementById("breakfastBtn").addEventListener("click", function() {
    showMenu("breakfastMenu");
  });
  
  document.getElementById("lunchBtn").addEventListener("click", function() {
    showMenu("lunchMenu");
  });
  
  document.getElementById("dinnerBtn").addEventListener("click", function() {
    showMenu("dinnerMenu");
  });
  
  function showMenu(menuId) {
    var menus = document.querySelectorAll("#menu div");
    for (var i = 0; i < menus.length; i++) {
      menus[i].classList.remove("visible");
    }
    
    document.getElementById(menuId).classList.add("visible");
  }
  
  function addToCart(productId) {
    fetch(`/add-to-cart/${productId}/`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            // Handle success or show appropriate message
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error or show appropriate message
        });
}
