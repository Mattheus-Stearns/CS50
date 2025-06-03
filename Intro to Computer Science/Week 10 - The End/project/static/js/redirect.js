console.log("Redirect script loaded.");
window.onload = function () {
    const redirectTarget = document.querySelector("[data-redirect-url]");
    if (redirectTarget) {
        const url = redirectTarget.dataset.redirectUrl;
        const back = redirectTarget.dataset.backUrl;
        if (url) window.open(url, "_blank");
        if (back) window.location.href = back;
    }
};