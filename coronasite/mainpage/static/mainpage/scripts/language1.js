let btnText1 = document.querySelector('#englishbutton');
let btnHtml1 = document.querySelector('#russianbutton');
let content1 = document.querySelector('#coronavirus_statistics');
let paragraph_1 = document.querySelector('#corona_cases');
let paragraph_2 = document.querySelector('#deaths_cases');
let paragraph_3 = document.querySelector('#recovered_cases');

btnText1.addEventListener('click', () => {
    paragraph_1.innerText = 'Coronavirus cases:';
    paragraph_2.innerText = 'Deaths:';
    paragraph_3.innerText = 'Recovered:';
});

btnHtml1.addEventListener('click', () => {
    paragraph_1.innerText = 'Случаи коронавируса:';
    paragraph_2.innerText = 'Смерти:';
    paragraph_3.innerText = 'Выздоровевшие:'
});
