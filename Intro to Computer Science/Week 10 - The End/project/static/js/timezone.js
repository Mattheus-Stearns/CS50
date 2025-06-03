// static/js/timezone.js
document.addEventListener("DOMContentLoaded", function () {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const tzInput = document.getElementById("timezone");
    if (tzInput) {
        tzInput.value = tz;
    }
});