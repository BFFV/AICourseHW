% Ejemplo 5x5

%fila(1..5).
%columna(1..5).
%color(verde, 3, 1).
%color(verde, 4, 1).
%color(azul, 5, 1).
%color(azul, 5, 3).
%color(blanco, 5, 4).
%color(blanco, 4, 5).
%color(amarillo, 3, 3).
%color(amarillo, 3, 4).
%color(morado, 3, 5).
%color(morado, 2, 4).

% Bonus 15x15

%fila(1..15).
%columna(1..15).
%color(blanco, 1, 4).
%color(blanco, 15, 10).
%color(verde_oscuro, 2, 8).
%color(verde_oscuro, 5, 2).
%color(cafe_claro, 1, 9).
%color(cafe_claro, 2, 10).
%color(rosado_claro, 1, 14).
%color(rosado_claro, 2, 9).
%color(morado, 1, 15).
%color(morado, 8, 9).
%color(azul_claro, 2, 7).
%color(azul_claro, 4, 3).
%color(naranjo, 3, 8).
%color(naranjo, 10, 13).
%color(celeste, 3, 14).
%color(celeste, 10, 5).
%color(rojo, 3, 15).
%color(rojo, 12, 15).
%color(cafe_oscuro, 5, 7).
%color(cafe_oscuro, 6, 5).
%color(rosado_oscuro, 5, 15).
%color(rosado_oscuro, 7, 15).
%color(turquesa, 6, 4).
%color(turquesa, 14, 14).
%color(azul, 7, 12).
%color(azul, 11, 13).
%color(amarillo, 8, 8).
%color(amarillo, 9, 7).
%color(verde, 9, 13).
%color(verde, 12, 14).
%color(gris, 12, 8).
%color(gris, 13, 3).

% Coordenadas adyacentes
adyacente(Y, X, B, A) :- fila(Y), columna(X), fila(B), columna(A), A == X, B == Y + 1.
adyacente(Y, X, B, A) :- fila(Y), columna(X), fila(B), columna(A), A == X, B == Y - 1.
adyacente(Y, X, B, A) :- fila(Y), columna(X), fila(B), columna(A), A == X + 1, B == Y.
adyacente(Y, X, B, A) :- fila(Y), columna(X), fila(B), columna(A), A == X - 1, B == Y.

% Colores
color_disponible(C) :- color(C, Y, X), fila(Y), columna(X).

% Se parte de sólo 1 de los puntos de partida por color (el otro pasa a ser la meta)
1{meta(C, Y, X): color(C, Y, X)}1 :- color_disponible(C).
partida(C, Y, X) :- color(C, Y, X), not meta(C, Y, X).

% Un camino no puede aparecer de la nada, debe estar conectado al resto
conectado(C, B, A) :- partida(C, B, A).
conectado(C, B, A) :- camino(C, Y, X, B, A), conectado(C, Y, X).

% Caminos (1 por casilla, excepto la meta de cada color)
1{camino(C, Y, X, B, A) : adyacente(Y, X, B, A)}1 :- conectado(C, Y, X), not meta(C, Y, X). 

% Se deben usar todas las casillas
pintada(Y, X) :- conectado(C, Y, X).
:- not pintada(Y, X), fila(Y), columna(X).

% No se pueden cruzar los caminos
:- conectado(C, Y, X), conectado(O, Y, X), C != O.

% No se puede formar un camino con un punto de partida o una meta de color distinto
:- camino(C, Y, X, B, A), color(O, B, A), not meta(C, B, A).

% No se puede retroceder
:- camino(C, Y, X, B, A), camino(C, B, A, Y, X).

#show camino/5.
