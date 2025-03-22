window.addEventListener('load', function() {
    const loader = document.getElementById('loader');
    loader.classList.add('fade-out');
  
    // Give the CSS transition time to finish, then hide completely
    setTimeout(() => {
      loader.style.display = 'none';
    }, 1000); // match the .5s in your CSS transition
});