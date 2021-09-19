let btnText = document.querySelector('#englishbutton');
let btnHtml = document.querySelector('#russianbutton');
let content = document.querySelector('#english_text');
let paragraph1 = document.querySelector('#name');
let paragraph2 = document.querySelector('#dangerous');
let paragraph3 = document.querySelector('#first_part');
let paragraph4 = document.querySelector('#second_part');
let paragraph5 = document.querySelector('#third_part');
let paragraph6 = document.querySelector('#fourth_part');
let paragraph7 = document.querySelector('#stat');
let paragraph8 = document.querySelector('#news');
let paragraph9 = document.querySelector('#points');


btnText.addEventListener('click', () => {
    paragraph1.innerText = 'Coronavirus infection (COVID-19)';
    paragraph2.innerText = 'The most dangerous strains';
    paragraph3.innerText = '– is an infectious disease caused by the SARS-CoV-2 virus.';
    paragraph4.innerText = 'of this disease are Cluster 5, Alpha, Beta, Gamma, Line B.1.525 and Delta.';
    paragraph5.innerText = 'The video shows a computer-simulated penetration of coronavirus into a human body.';
    paragraph6.innerText = 'Resources with useful information on the coronavirus: ';
    paragraph7.innerText = 'Statistics';
    paragraph8.innerText = 'UN Coronavirus News';
    paragraph9.innerText = 'Vaccination points in Belarus ';
});

btnHtml.addEventListener('click', () => {
    paragraph1.innerText = 'Коронавирусная инфекция (COVID-19)';
    paragraph2.innerText = 'Самыми опасными штаммами';
    paragraph3.innerText = '– это инфекционное заболевание, вызванное вирусом SARS-CoV-2.';
    paragraph4.innerText = 'этой болезни являются - Кластер 5, Альфа, Бета, Гамма, Линия B.1.525 и Дельта.';
    paragraph5.innerText = 'Видео показывает смоделированное на компьютере проникновение коронавируса в тело человека.';
    paragraph6.innerText = 'Ресурсы, с полезной информацией по коронавирусу:';
    paragraph7.innerText = 'Статистика';
    paragraph8.innerText = 'Новости по коронавирусу от ООН';
    paragraph9.innerText = 'Пункты вакцинации в Беларуси';
});
