const password = document.getElementById('password');
const confirm = document.getElementById('password-confirm');
const form = document.querySelector('form');

const checkPasswordsEquality = () => {
  if (password.value == confirm.value) {
    confirm.setCustomValidity('');
  }
  else {
    confirm.setCustomValidity('Пароли не совпадают');
  }
}

password.addEventListener('input', checkPasswordsEquality);
confirm.addEventListener('input', checkPasswordsEquality);

form.addEventListener('submit', (e) => {
  console.log('triegger')
  checkPasswordsEquality();
  if (!form.checkValidity()) {
    e.preventDefault();
  }
});