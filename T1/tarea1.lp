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
%color(blanco, 15, 10).
%color(blanco, 1, 4).
%color(naranjo, 10, 13).
%color(naranjo, 3, 8).
%color(amarillo, 9, 7).
%color(amarillo, 8, 8).
%color(verde_claro, 9, 13).
%color(verde_claro, 12, 14).
%color(verde_oscuro, 5, 2).
%color(verde_oscuro, 2, 8).
%color(azul_claro, 4, 3).
%color(azul_claro, 2, 7).
%color(azul_oscuro, 7, 12).
%color(azul_oscuro, 11, 13).
%color(gris_claro, 1, 9).
%color(gris_claro, 2, 10).
%color(gris_oscuro, 13, 3).
%color(gris_oscuro, 12, 8).
%color(purpura_suave, 2, 9).
%color(purpura_suave, 1, 14).
%color(purpura_fuerte, 5, 15).
%color(purpura_fuerte, 7, 15).
%color(morado, 8, 9).
%color(morado, 1, 15).
%color(rojo, 3, 15).
%color(rojo, 12, 15).
%color(burdeo, 6, 5).
%color(burdeo, 5, 7).
%color(celeste_claro, 10, 5).
%color(celeste_claro, 3, 14).
%color(celeste_oscuro, 6, 4).
%color(celeste_oscuro, 14, 14).

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

% Caminos (1 por casilla, excepto la meta de cada color)
1{camino(C, Y, X, B, A) : adyacente(Y, X, B, A)}1 :- partida(C, Y, X).
1{camino(C, K, J, B, A) : adyacente(K, J, B, A)}1 :- camino(C, Y, X, K, J), not meta(C, K, J).
:- camino(C, Y, X, B, A), meta(C, Y, X).

% Un camino no puede aparecer de la nada, debe estar conectado al resto
conectado(C, B, A) :- partida(C, B, A).
conectado(C, B, A) :- camino(C, Y, X, B, A), conectado(C, Y, X).
:- camino(C, B, A, Y, X), not conectado(C, B, A).

% Se deben usar todas las casillas
pintada(Y, X) :- conectado(C, Y, X).
:- not pintada(Y, X), fila(Y), columna(X).

% No se pueden cruzar los caminos
:- camino(C, Y, X, B, A), camino(O, K, J, B, A), X != J.
:- camino(C, Y, X, B, A), camino(O, K, J, B, A), Y != K.

% No se puede formar un camino con un punto de partida o una meta de color distinto
:- camino(C, Y, X, B, A), color(O, B, A), not meta(C, B, A).

% No se puede retroceder
:- camino(C, Y, X, B, A), camino(C, B, A, Y, X).

% No se puede formar un camino directo entre la partida y la meta de un color
:- camino(C, Y, X, B, A), partida(C, Y, X), meta(C, B, A).

#show camino/5.
