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
