const sideMenu = document.querySelector("aside");
const profileBtn = document.querySelector("#profile-btn");
// const menuItems = document.querySelectorAll('.menu-item');
// const currentURL = window.location.href;

// menuItems.forEach(item => {
//   if (item.href === currentURL) {
//     item.classList.add('active');
//   }

//   item.addEventListener('click', (event) => {
//     event.preventDefault();
//     menuItems.forEach(item => item.classList.remove('active'));
//     item.classList.add('active');
//     window.location.href = item.href;
//   });
// });


profileBtn.onclick = function() {
    sideMenu.classList.toggle('active');
}
window.onscroll = () => {
    sideMenu.classList.remove('active');
    if(window.scrollY > 0){document.querySelector('header').classList.add('active');}
    else{document.querySelector('header').classList.remove('active');}
}