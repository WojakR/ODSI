// Podglad tekstu z fragmentu adresu (po znaku #).
// textContent wstawia dane doslownie jako tekst, wiec HTML z ladunku nie jest interpretowany.
document.getElementById("podglad").textContent = decodeURIComponent(location.hash.slice(1));
