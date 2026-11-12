document.getElementById('year').textContent=new Date().getFullYear();
const navbtn=document.getElementById('navbtn'),nav=document.getElementById('nav');
navbtn.addEventListener('click',()=>nav.classList.toggle('open'));
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>nav.classList.remove('open')));