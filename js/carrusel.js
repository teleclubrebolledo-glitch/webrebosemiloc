/* Carrusel de secciones de Rebolledo de la Torre. Script PROPIO y mínimo: sin cookies, sin almacenamiento local, sin terceros, sin analítica.
   Sin este script la página funciona igual, con todas las secciones una debajo de otra.
   - Cada diapositiva muestra UNA subsección de una sección; cada vez que la sección vuelve a salir, enseña la siguiente (y al acabar, empieza otra vez).
   - Flechas, teclado, pausa; los enlaces de abajo abren la sección entera (pantalla completa, sin las demás). */
(function () {
  'use strict';
  var raiz = document.documentElement;
  var almacen = document.getElementById('almacen');
  var caja = document.querySelector('.caja'), diap = document.querySelector('.diap'), carrusel = document.getElementById('carrusel');
  if (!almacen || !caja || !diap) return;
  raiz.classList.add('js');

  var secs = [].slice.call(almacen.querySelectorAll(':scope > .sec'));
  var tabs = [].slice.call(document.querySelectorAll('.tabs a, .navtop > a[data-sec], .navtop summary[data-sec]'));
  var N = secs.length;
  var cartas = secs.map(function (s) { return [].slice.call(s.querySelectorAll('.rejilla > article')); });
  var reducido = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var pausaBtn = document.querySelector('.pausa');
  var i = 0, reproduce = !reducido, timer = null, dentro = false, actual = null;
  var DURACION = 12000;

  function mod(a, n) { return ((a % n) + n) % n; }

  function devolver() {
    if (actual) { actual.hueco.replaceWith(actual.carta); actual = null; }
  }

  function subrayar(s) {
    var id = s === null ? 'inicio' : secs[s].id;
    tabs.forEach(function (a) { if (a.getAttribute('data-sec') === id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
  }

  function mostrar(n) {
    devolver();
    i = n;
    var s = mod(n, N), lista = cartas[s], k = mod(Math.floor(n / N), lista.length);
    var carta = lista[k], hueco = document.createElement('div');
    hueco.hidden = true; carta.replaceWith(hueco);
    actual = { carta: carta, hueco: hueco };
    var sec = secs[s];
    diap.textContent = '';
    var tit = document.createElement('div'); tit.className = 'titulo';
    var h = document.createElement('h2'); h.textContent = sec.getAttribute('data-nombre'); tit.appendChild(h);
    var lead = document.createElement('p'); lead.className = 'lead'; lead.textContent = sec.getAttribute('data-lead');
    var cuenta = document.createElement('p'); cuenta.className = 'cuenta';
    cuenta.textContent = 'Tarjeta ' + (k + 1) + ' de ' + lista.length + ' · ';
    var ver = document.createElement('a'); ver.href = '#' + sec.id; ver.textContent = 'Abrir la sección completa →'; cuenta.appendChild(ver);
    var envol = document.createElement('div'); envol.className = 'enc';
    envol.appendChild(tit); envol.appendChild(lead); envol.appendChild(carta); envol.appendChild(cuenta);
    diap.appendChild(envol);
    caja.setAttribute('data-par', sec.classList.contains('b2') ? '2' : (sec.classList.contains('b1') ? '1' : '0'));
    diap.classList.remove('entra'); void diap.offsetWidth; diap.classList.add('entra');
    subrayar(s);
  }

  function parar() { if (timer) { clearInterval(timer); timer = null; } }
  function arrancar() {
    parar();
    if (reproduce && !dentro && !document.hidden && !raiz.getAttribute('data-vista')) timer = setInterval(function () { mostrar(i + 1); }, DURACION);
  }
  function etiqueta() {
    if (!pausaBtn) return;
    pausaBtn.textContent = reproduce ? '⏸ Pausar' : '▶ Reproducir';
    pausaBtn.setAttribute('aria-pressed', reproduce ? 'false' : 'true');
    diap.setAttribute('aria-live', reproduce ? 'off' : 'polite');
  }

  function vistaCarrusel(desdeSeccion) {
    raiz.removeAttribute('data-vista');
    secs.forEach(function (s) { s.classList.remove('activa'); });
    mostrar(i);
    arrancar();
    if (desdeSeccion) window.scrollTo(0, 0);
  }

  function vistaSeccion(idx, ancla) {
    parar(); devolver();
    raiz.setAttribute('data-vista', 'seccion');
    secs.forEach(function (s, k) { s.classList.toggle('activa', k === idx); });
    subrayar(idx);
    var dest = ancla && document.getElementById(ancla);
    if (dest && secs[idx].contains(dest)) dest.scrollIntoView(); else window.scrollTo(0, 0);
  }

  function ruta() {
    var id = decodeURIComponent((location.hash || '').slice(1));
    var idx = -1;
    secs.forEach(function (s, k) { if (id === s.id || id.indexOf(s.id + '-') === 0) idx = k; });
    if (idx >= 0) vistaSeccion(idx, id);
    else vistaCarrusel(raiz.getAttribute('data-vista') === 'seccion');
  }

  [].forEach.call(document.querySelectorAll('.flecha'), function (b) {
    b.addEventListener('click', function () { mostrar(i + parseInt(b.getAttribute('data-dir'), 10)); arrancar(); });
  });
  if (pausaBtn) pausaBtn.addEventListener('click', function () { reproduce = !reproduce; etiqueta(); arrancar(); });
  if (carrusel) {
    carrusel.addEventListener('mouseenter', function () { dentro = true; parar(); });
    carrusel.addEventListener('mouseleave', function () { dentro = false; arrancar(); });
    carrusel.addEventListener('focusin', function () { dentro = true; parar(); });
    carrusel.addEventListener('focusout', function () { dentro = false; arrancar(); });
    carrusel.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { mostrar(i - 1); arrancar(); e.preventDefault(); }
      if (e.key === 'ArrowRight') { mostrar(i + 1); arrancar(); e.preventDefault(); }
    });
  }
  /* Móvil: se pasa arrastrando el dedo hacia los lados (el gesto vertical sigue siendo desplazar la página). */
  var x0 = null, y0 = 0;
  caja.addEventListener('touchstart', function (e) {
    if (e.touches.length !== 1) { x0 = null; return; }
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
  }, { passive: true });
  caja.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var t = e.changedTouches[0], dx = t.clientX - x0, dy = t.clientY - y0; x0 = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > 1.5 * Math.abs(dy)) { mostrar(i + (dx < 0 ? 1 : -1)); arrancar(); }
  }, { passive: true });
  caja.addEventListener('touchcancel', function () { x0 = null; }, { passive: true });
  document.addEventListener('visibilitychange', arrancar);
  function cierraMenus() { [].forEach.call(document.querySelectorAll('.navtop details[open]'), function (d) { d.removeAttribute('open'); }); }
  window.addEventListener('hashchange', function () { cierraMenus(); ruta(); });
  document.addEventListener('click', function (e) { if (!e.target.closest || !e.target.closest('.navtop')) cierraMenus(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') cierraMenus(); });

  var p = new URLSearchParams(location.search).get('i');
  if (p !== null && !isNaN(parseInt(p, 10))) i = parseInt(p, 10);
  etiqueta();
  ruta();
})();
