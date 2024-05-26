// Toggle password visibility
function togglePasswordVisibility() {
  const passwordInput = document.getElementById('password');
  const eyeIcon = document.querySelector('.eye-icon');

  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    eyeIcon.classList.remove('fa-eye-slash');
    eyeIcon.classList.add('fa-eye');
  } else {
    passwordInput.type = 'password';
    eyeIcon.classList.remove('fa-eye');
    eyeIcon.classList.add('fa-eye-slash');
  }
}

// Changing Greetings
function changeGreeting(userType) {
  const greeting = document.getElementById('greeting');
  const slider = document.querySelector('.user-type .slider');
  const userTypeField = document.getElementById('user_type');
  const studentButton = document.querySelector('.user-type button:first-child');
  const teacherButton = document.querySelector('.user-type button:last-child');

  if (userType === 'student') {
    greeting.textContent = 'Hello Student!';
    slider.classList.remove('teacher');
    slider.classList.add('student');
    userTypeField.value = 'student';
    // studentButton.classList.add('active');
    
  } else if (userType === 'teacher') {
    greeting.textContent = 'Hello Teacher!';
    slider.classList.remove('student');
    slider.classList.add('teacher');
    userTypeField.value = 'teacher';
    // studentButton.classList.remove('active');
    // teacherButton.classList.add('active');
  }
}