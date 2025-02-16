document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('backToProfileBtn').addEventListener('click', function () {
        const pk = this.getAttribute("data-pk");
        const url = `/accounts/about-me/${pk}/`;
        window.location.href = url;  // Перенаправляем на сформированный URL
    });
});