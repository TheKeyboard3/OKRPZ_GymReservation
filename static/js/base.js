document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('profile-form')

    if (form) {
        form.addEventListener('submit', function (event) {
            var inputText = document.getElementById('id_username').value
            var containsCyrillic = /[а-яА-ЯЁёґҐіІїЇєЄ]/.test(inputText)

            if (containsCyrillic) {
                event.preventDefault() // Відміна надсилання форми
                alert('Текст містить кириличні символи. Будь ласка, введіть текст латиницею.')
            }
        })
    }
})

function toggleComments(link, commentId) {
    var target = document.getElementById('reply-comment-' + commentId)

    if (link.getAttribute('data-loaded') === 'true') {
        if (target.style.display === 'none') {
            target.style.display = 'block'
        } else {
            target.style.display = 'none'
        }
    } else {
        // Якщо коментарі ще не завантажені, виконуємо запит через HTMX
        htmx.trigger(link, 'click')
        link.setAttribute('data-loaded', 'true')
    }
}
