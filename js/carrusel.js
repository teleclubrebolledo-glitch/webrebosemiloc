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
    if (dest && secs[idx].contains(dest)) { if (dest.tagName === 'DETAILS') dest.open = true; dest.scrollIntoView(); } else window.scrollTo(0, 0);
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

  /* Dovelas: el arco del vídeo lleva un anillo de piedras con sus juntas (dibujo decorativo, se recalcula al cambiar el tamaño). */
  /* Fotos de «Fauna y flora» en las piedras del arco: de una en una; mientras se desvanece la de una piedra aparece otra foto en otra piedra, sin repetir hasta agotarlas todas. */
  var fotosPiedra = (function () {
    var lista = (document.querySelector('.marco-arco') || {}).getAttribute ? (document.querySelector('.marco-arco').getAttribute('data-fotos') || '').split('|').filter(Boolean) : [];
    var cola = [], actual = null, NS = 'http://www.w3.org/2000/svg', o = { geo: [], capa: null };
    function baraja() { cola = lista.slice(); for (var a = cola.length - 1; a > 0; a--) { var b = Math.floor(Math.random() * (a + 1)), t = cola[a]; cola[a] = cola[b]; cola[b] = t; } }
    function crea(piedra, url, visible) {
      var g = o.geo[piedra]; if (!g || !o.capa) return null;
      var im = document.createElementNS(NS, 'image');
      im.setAttribute('href', url); im.setAttribute('x', g.x); im.setAttribute('y', g.y); im.setAttribute('width', g.w); im.setAttribute('height', g.h);
      im.setAttribute('preserveAspectRatio', 'xMidYMid slice'); im.setAttribute('clip-path', 'url(#pf-' + piedra + ')');
      im.style.opacity = visible ? 1 : 0; im.style.transition = 'opacity 1.8s ease-in-out';
      o.capa.appendChild(im); return im;
    }
    o.repinta = function () { if (actual) actual.im = crea(actual.piedra, actual.url, true); };
    function paso() {
      if (!lista.length || !o.geo.length || !o.capa) return;
      if (!cola.length) baraja();
      var url = cola.pop(), piedra, tries = 0;
      do { piedra = Math.floor(Math.random() * o.geo.length); tries++; } while (actual && Math.abs(piedra - actual.piedra) < 2 && tries < 20);   /* otra piedra, no la de al lado */
      var nuevo = { piedra: piedra, url: url, im: crea(piedra, url, false) };
      if (!nuevo.im) return;
      var viejo = actual; actual = nuevo;
      requestAnimationFrame(function () { requestAnimationFrame(function () { if (nuevo.im) nuevo.im.style.opacity = 1; if (viejo && viejo.im) { var v = viejo.im; v.style.opacity = 0; setTimeout(function () { if (v.parentNode) v.parentNode.removeChild(v); }, 2000); viejo.im = null; } }); });
    }
    if (!reducido && lista.length) { setTimeout(paso, 1500); setInterval(function () { if (!document.hidden) paso(); }, 6000); }
    return o;
  })();

  function piedras() {
    var marco = document.querySelector('.marco-arco'), por = document.querySelector('.portada');
    if (!marco || !por) return;
    var NS = 'http://www.w3.org/2000/svg';
    var svg = marco.querySelector('.piedras');
    if (!svg) { svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'piedras'); svg.setAttribute('aria-hidden', 'true'); svg.setAttribute('focusable', 'false'); marco.insertBefore(svg, marco.firstChild); }
    var sonda = document.createElement('div'); sonda.style.cssText = 'position:absolute;visibility:hidden;height:var(--arco);width:1px'; marco.appendChild(sonda);
    var b = sonda.offsetHeight; sonda.style.height = 'var(--cap)'; var capAlto = sonda.offsetHeight; marco.removeChild(sonda);
    var m = marco.getBoundingClientRect(), r = por.getBoundingClientRect();
    var a = r.width / 2, cx = r.left - m.left + a, top = r.top - m.top, cy = top + b;
    var T = Math.min((marco.querySelector('.pilar') || marco).getBoundingClientRect().width, top);      /* grosor = ancho del capitel */
    var M = 160, P = [], O = [], L = [0], k, th, nx, ny, nn, i;
    for (k = 0; k <= M; k++) {                                   /* arco interior (elipse) y curva paralela a distancia T: el grosor no cambia en ningún punto */
      th = Math.PI * k / M;
      var x = cx - a * Math.cos(th), y = cy - b * Math.sin(th);
      nx = -Math.cos(th) / a; ny = -Math.sin(th) / b; nn = Math.hypot(nx, ny); nx /= nn; ny /= nn;
      P.push([x, y]); O.push([x + T * nx, y + T * ny]);
      L.push(k ? L[k - 1] + Math.hypot(x - P[k - 1][0], y - P[k - 1][1]) : 0);
    }
    L.shift();
    var N = Math.max(7, Math.round(L[M] / (T * 1.1))); if (N % 2 === 0) N++;       /* nº impar: la clave queda en el centro */
    var banda = 'M' + O.map(function (q) { return q[0].toFixed(1) + ' ' + q[1].toFixed(1); }).join('L') + 'L' + P.slice().reverse().map(function (q) { return q[0].toFixed(1) + ' ' + q[1].toFixed(1); }).join('L') + 'Z';
    var d = '', J = [0];
    for (i = 1; i < N; i++) {                                    /* juntas a intervalos iguales de arco: todas las piedras del mismo largo */
      var obj = L[M] * i / N; k = 1; while (k < M && L[k] < obj) k++;
      J.push(k); d += 'M' + P[k][0].toFixed(1) + ' ' + P[k][1].toFixed(1) + 'L' + O[k][0].toFixed(1) + ' ' + O[k][1].toFixed(1);
    }
    svg.setAttribute('width', m.width); svg.setAttribute('height', cy + 2); svg.setAttribute('viewBox', '0 0 ' + m.width + ' ' + (cy + 2));
    /* el anillo termina justo en la cara superior del capitel (ni un pixel por debajo): recorte horizontal a esa altura */
    svg.innerHTML = '<defs><clipPath id="piedras-corte"><rect x="0" y="0" width="' + m.width + '" height="' + (cy - capAlto) + '"/></clipPath></defs><g clip-path="url(#piedras-corte)">' +
      '<path d="' + banda + '" fill="#cbbd9b"/><g id="piedras-fotos"></g><path d="' + d + '" stroke="#8f836b" stroke-width="1.6" fill="none" stroke-linecap="round"/><path d="' + banda + '" fill="none" stroke="#8f836b" stroke-width="1.6" stroke-linejoin="round"/></g>';
    J.push(M);
    var defs = svg.querySelector('defs'), capa = svg.querySelector('#piedras-fotos'), geo = [];
    for (i = 0; i < N; i++) {                                    /* polígono de cada piedra: borde exterior de una junta a la siguiente y vuelta por el interior */
      var pts = [], xs = [], ys = [];
      for (k = J[i]; k <= J[i + 1]; k++) pts.push(O[k]);
      for (k = J[i + 1]; k >= J[i]; k--) pts.push(P[k]);
      pts.forEach(function (q) { xs.push(q[0]); ys.push(q[1]); });
      var cp = document.createElementNS(NS, 'clipPath'); cp.setAttribute('id', 'pf-' + i);
      var pg = document.createElementNS(NS, 'polygon'); pg.setAttribute('points', pts.map(function (q) { return q[0].toFixed(1) + ',' + q[1].toFixed(1); }).join(' ')); cp.appendChild(pg); defs.appendChild(cp);
      var x0 = Math.min.apply(null, xs), y0 = Math.min.apply(null, ys);
      geo.push({ x: x0, y: y0, w: Math.max.apply(null, xs) - x0, h: Math.max.apply(null, ys) - y0 });
    }
    fotosPiedra.geo = geo; fotosPiedra.capa = capa; fotosPiedra.repinta();
  }


  piedras();
  if (window.ResizeObserver) new ResizeObserver(piedras).observe(document.querySelector('.marco-arco')); else window.addEventListener('resize', piedras);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(piedras);

  /* Cintas negras bajo el vídeo (avisos: 7 s; huerta: 21 s): una entrada cada vez (quieta con «movimiento reducido»), se detiene al pasar el ratón o el foco, y con flechas. */
  [].forEach.call(document.querySelectorAll('.cinta'), function (cinta) {
    var its = [].slice.call(cinta.querySelectorAll('.cinta-item')), k = 0, t = null, dentro2 = false, ms = parseInt(cinta.getAttribute('data-ms') || '7000', 10);
    function ver(n) { its[k].classList.remove('activo'); k = (n + its.length) % its.length; its[k].classList.add('activo'); }
    function auto() { if (t) clearInterval(t); if (!reducido && !dentro2 && its.length > 1) t = setInterval(function () { ver(k + 1); }, ms); }
    [].forEach.call(cinta.querySelectorAll('.cinta-b'), function (b) { b.addEventListener('click', function () { ver(k + parseInt(b.getAttribute('data-d'), 10)); auto(); }); });
    cinta.addEventListener('mouseenter', function () { dentro2 = true; auto(); }); cinta.addEventListener('mouseleave', function () { dentro2 = false; auto(); });
    cinta.addEventListener('focusin', function () { dentro2 = true; auto(); }); cinta.addEventListener('focusout', function () { dentro2 = false; auto(); });
    auto();
  });

  var p = new URLSearchParams(location.search).get('i');
  if (p !== null && !isNaN(parseInt(p, 10))) i = parseInt(p, 10);
  etiqueta();
  ruta();
})();
