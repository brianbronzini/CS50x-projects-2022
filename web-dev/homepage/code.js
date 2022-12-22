document.addEventListener('DOMContentLoaded', function() {
  let btn = document.querySelector('#js-btn')
  let message = document.getElementById('secretText');

  btn.addEventListener('click', function() {
    message.innerHTML = "You have found the secret text!";
  });
});