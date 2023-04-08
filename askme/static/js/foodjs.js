const FcharField = document.getElementById('food_place_id');
const FsubmitButton = document.getElementById('food_submit_button');
// const FerrorMessage = document.getElementById('error_message');

FsubmitButton.disabled = true;

FcharField.addEventListener('input', () => {
  if (FcharField.checkValidity()) {
    FsubmitButton.disabled = false;
  } else {
    FsubmitButton.disabled = true;
  }
});



function typeWriter(text, i, fnCallback) {
    if (i < text.length) {
      document.getElementById("make-food-visible").innerHTML += text.charAt(i);
      i++;
      setTimeout(function() {
        typeWriter(text, i, fnCallback)
      }, 100);
    } else if (typeof fnCallback == "function") {
      setTimeout(fnCallback, 700);
    }
  }

function startFoodTyping() {
    var text = "Building Food Recommendation... may take upto 10sec";
    typeWriter(text, 0, function() {
      console.log("Text has been typed out!");
    });
}