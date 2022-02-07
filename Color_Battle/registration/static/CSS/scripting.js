if(!localStorage.theme) localStorage.theme - "light"
document.body.className = localStorage.theme

toggleThemeBtn.onclick = () => {
    document.body.classList.toggle("dark")
    localStorage.theme = document.body.className || "light"
}

toggleThemePurple.onclick = () => {
    document.body.classList.toggle("purple")
    localStorage.theme = document.body.className || "light"
}

function soundClick() {
  var audio = new Audio(); // Создаём новый элемент Audio
  audio.src = 'http://127.0.0.1:8000/static/CSS/out.mp3' ; // Указываем путь к звуку "клика"
  audio.autoplay = true; // Автоматически запускаем
}

