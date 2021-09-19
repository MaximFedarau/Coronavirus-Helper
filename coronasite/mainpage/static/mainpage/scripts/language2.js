let btnText2 = document.querySelector('#englishbutton');
let btnHtml2 = document.querySelector('#russianbutton');
let content2 = document.querySelector('#telegram_bot');
let p1 = document.querySelector('#warning');
let p2 = document.querySelector('#warning_on_english');
let p3 = document.querySelector('#telegram');
let p4 = document.querySelector('#contacts');
let p5 = document.querySelector('#d_first_part');
let p6 = document.querySelector('#d_second_part');
let p7 = document.querySelector('#updates_main_title');

btnText2.addEventListener('click', () => {
    p1.innerText = '[WARNING!]';
    p2.innerText = 'This project is only in BETA version. If you have any advices or problems with our services or you want to join our team, then please contacts with us as fast as you can!'
    p3.innerText = 'Telegram Bot';
    p4.innerText =  'Contacts';
    p5.innerText = 'Our Telegram-bot allows people to quickly find out the latest and reliable information about the coronavirus.';
    p6.innerText = 'Help yourself and your relatives as the speed of obtaining reliable data is more import tant then ever!';
    p7.innerText = 'Coronavirus-Helper Bot latest update:';
});

btnHtml2.addEventListener('click', () => {
    p1.innerText = '[ВНИМАНИЕ!]';
    p2.innerText = 'Этот проект находится только в БЕТА версии. Если у вас есть какие-либо предложения или проблемы или вы хотите присоединиться к нашей команде, то свяжитесь с нами.'
    p3.innerText = 'Телеграм Бот';
    p4.innerText =  'Контакты';
    p5.innerText= 'Наш Телеграм-бот позволяет людям быстро находить актуальную и достоверную информацию о коронавирусе.';
    p6.innerText = 'Помогите себе и родственникам, так как скорость получения правдивой информации важна как никогда!';
    p7.innerText = 'Последнее обновление Coronavirus-Helper Бота: ';
});
