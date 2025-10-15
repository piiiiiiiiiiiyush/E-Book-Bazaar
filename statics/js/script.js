// Search Filter Script
const searchInput = document.querySelector(".search-box");
const books = document.querySelectorAll(".book-card");

if (searchInput && books.length > 0) {
  searchInput.addEventListener("keyup", function () {
    let filter = searchInput.value.toLowerCase();
    let anyVisible = false;

    books.forEach(book => {
      let title = book.querySelector("h3").textContent.toLowerCase();
      let author = book.querySelector("p").textContent.toLowerCase();

      if (title.includes(filter) || author.includes(filter)) {
        book.style.display = "block";
        anyVisible = true;
      } else {
        book.style.display = "none";
      }
    });

    // Show "No results" message
    if (!anyVisible) {
      if (!document.getElementById("noResults")) {
        let msg = document.createElement("p");
        msg.id = "noResults";
        msg.textContent = "No matching books found.";
        msg.style.textAlign = "center";
        msg.style.color = "red";
        msg.style.marginTop = "20px";
        document.querySelector(".books").appendChild(msg);
      }
    } else {
      let msg = document.getElementById("noResults");
      if (msg) msg.remove();
    }
  });
}