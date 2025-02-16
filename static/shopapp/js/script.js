// document.addEventListener("DOMContentLoaded", function () {
//     var container = document.querySelector('.popup-container');
//     var popupButtons = document.querySelectorAll('.open-popup');
//     for (let i = 0; i < popupButtons.length; i++) {
//         popupButtons[i].addEventListener('click', function () {
//             container.style.display = 'flex';
//         })
//     }
//     container.addEventListener('click', function (event) {
//         if (event.target === container) {
//             container.style.display = 'none';
//         }
//     });
// });


// document.addEventListener('DOMContentLoaded', function () {
//     document.getElementById('loginForm').onclick = function () {
//         window.location.href = "shop/products";
//     }
// });
//
// document.addEventListener('DOMContentLoaded', function () {
//     document.getElementById('logoutButton').onclick = function () {
//         window.location.href = "shop/products";
//     }
// });

document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const loginPopup = document.getElementById('loginPopup'); // Получаем элемент всплывающего окна

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Предотвращаем стандартное поведение формы

            const formData = new FormData(loginForm); // Собираем данные формы

            fetch(loginForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Указываем, что это AJAX-запрос
                }
            })
                .then(response => response.json())
                // {
                //     if (response.ok) {
                //         return response.json(); // Предполагаем, что сервер возвращает JSON
                //     }
                //     throw new Error('Network response was not ok.');
                // })
                .then(data => {
                    // Обработка успешного ответа
                    if (data.success) {
                        loginPopup.style.display = 'none'
                        window.location.href = data.redirect_url; // Перенаправляем на указанную страницу
                    } else {
                        alert(data.message); // Показываем сообщение об ошибке
                    }
                })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });
        });
    }

    const logoutButton = document.getElementById('logoutButton');

    if (logoutButton) {
        logoutButton.addEventListener('click', function (event) {
            event.preventDefault(); // Предотвращаем стандартное поведение кнопки

            const confirmation = confirm("Вы уверены, что хотите выйти?");
            if (confirmation) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = logoutButton.form.action; // Получаем URL из формы

                const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);

                const nextInput = document.createElement('input');
                nextInput.type = 'hidden';
                nextInput.name = 'next';
                nextInput.value = logoutButton.form.querySelector('input[name="next"]').value; // Получаем значение из формы
                form.appendChild(nextInput);

                document.body.appendChild(form);
                form.submit(); // Отправляем форму
            }
        });
    }

    // Закрытие всплывающего окна при клике вне его
    window.addEventListener('click', function (event) {
        if (event.target === loginPopup) { // Проверяем, был ли клик по контейнеру
            loginPopup.style.display = 'none'; // Закрываем окно
        }
    });
});
