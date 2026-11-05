/* Tiempo en la cabecera: estado de ahora y «prev. mañana», con iconos minimalistas. Lee tiempo/tiempo.json (misma web; lo actualiza un programa en el servidor).
   Sin cookies, sin almacenamiento, sin contactar con terceros. Si no hay datos, no muestra nada. */
(function () {
  'use strict';
  var nube = '<path d="M6.5 18a4 4 0 0 1-.4-7.98A5.5 5.5 0 0 1 16.8 8.8 4.6 4.6 0 0 1 17 18Z"/>';
  var sol = '<circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.3M12 19.2v2.3M2.5 12h2.3M19.2 12h2.3M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M18.7 5.3l-1.6 1.6M6.9 17.1l-1.6 1.6"/>';
  var luna = '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.4 6.4 0 0 0 10.5 10.5Z"/>';
  function desplaza(s, x, y) { return '<g transform="translate(' + x + ' ' + y + ')">' + s + '</g>'; }
  function icono(codigo, dia) {
    var i, t;
    if (codigo === 0) { i = dia ? sol : luna; t = dia ? 'Despejado' : 'Despejado'; }
    else if (codigo === 1) { i = dia ? sol : luna; t = 'Poco nuboso'; }
    else if (codigo === 2) { i = '<g transform="translate(-3 -3) scale(.66)">' + (dia ? sol : luna) + '</g>' + desplaza('<g transform="scale(.85)" fill="var(--papel)">' + nube + '</g>', 3, 5); t = 'Parcialmente nuboso'; }
    else if (codigo === 3) { i = nube; t = 'Cubierto'; }
    else if (codigo === 45 || codigo === 48) { i = '<path d="M4 8h16M3 12h18M5 16h14M8 20h8"/>'; t = 'Niebla'; }
    else if ((codigo >= 51 && codigo <= 67) || (codigo >= 80 && codigo <= 82)) { i = desplaza(nube, 0, -3) + '<path d="M8 19l-1 2.6M12 19l-1 2.6M16 19l-1 2.6"/>'; t = codigo >= 80 ? 'Chubascos' : (codigo < 61 ? 'Llovizna' : 'Lluvia'); }
    else if ((codigo >= 71 && codigo <= 77) || codigo === 85 || codigo === 86) { i = desplaza(nube, 0, -3) + '<path d="M8 20h.01M12 21h.01M16 20h.01M10 23h.01M14 23h.01" stroke-width="3"/>'; t = 'Nieve'; }
    else if (codigo >= 95) { i = desplaza(nube, 0, -3) + '<path d="M12.5 15.5l-2.6 4h3.2l-2.2 4"/>'; t = 'Tormenta'; }
    else { i = nube; t = 'Variable'; }
    return { svg: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + i + '</svg>', texto: t };
  }
  var a = document.querySelector('.t-ahora'), m = document.querySelector('.t-manana');
  if (!a || !m) return;
  fetch('tiempo/tiempo.json', { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : Promise.reject(); }).then(function (d) {
    var h = icono(d.ahora.codigo, d.ahora.dia), n = icono(d.manana.codigo, true);
    a.innerHTML = '<span class="ico">' + h.svg + '</span><span class="gr">' + d.ahora.temp + '°</span>';
    a.setAttribute('title', 'Ahora en Rebolledo: ' + h.texto + ', ' + d.ahora.temp + ' grados'); a.setAttribute('aria-label', a.getAttribute('title'));
    m.innerHTML = '<span class="pre">prev. mañana</span><span class="ico">' + n.svg + '</span><span class="gr">' + d.manana.tmin + '°/' + d.manana.tmax + '°</span>';
    m.setAttribute('title', 'Previsión de mañana: ' + n.texto + ', mínima ' + d.manana.tmin + ' y máxima ' + d.manana.tmax + ' grados, lluvia ' + d.manana.lluvia + ' %'); m.setAttribute('aria-label', m.getAttribute('title'));
    a.hidden = false; m.hidden = false;
  }).catch(function () { /* sin datos: no se muestra nada */ });
})();
