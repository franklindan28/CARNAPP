const text = [
  "More than 30 Massuer Near You",
  "Activating The Senses",
  "Less stress, More Facials",
  "Relaxation + Enjoyment",
  "What Are You Waiting For?",
];
let count = 0;
let index = 0;
let currentText = "";
let letter = "";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

(async function type() {
  if (count === text.length) {
    count = 0;
  }
  currentText = text[count];
  letter = currentText.slice(0, ++index);

  document.querySelector(".typing").textContent = letter;
  if (letter.length === currentText.length) {
    await sleep(1500);

    while (letter.length != 0) {
      letter = currentText.slice(0, --index);

      document.querySelector(".typing").textContent = letter;

      await sleep(25);
    }

    //reset
    count++;
    index = 0;
    await sleep(500);
  }

  setTimeout(type, 75);
})();

window.addEventListener("scroll", function () {
  var header = this.document.querySelector("header");
  header.classList.toggle("sticky", window.scrollY > 0);
});
