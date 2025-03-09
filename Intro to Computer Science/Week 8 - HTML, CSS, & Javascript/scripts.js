document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function(event) {
    alert('hello, ' + document.querySelector('#name').value);
    event.preventDefault();
    });
});
