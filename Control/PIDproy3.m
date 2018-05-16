close all
%% Definición de parámetros
%%%Motor Rojo
La1=1.76e-4;
Jm1=2.1393e-5;
Ra1=1.1724;
Bm1=0.0202;
ki1=0.2864;
kv1=0.2864;
%%%Motor Verde
La2=1.49e-4;
Jm2=2.1393e-5;
Ra2=1.1458;
Bm2=0.0158;
ki2=0.2778;
kv2=0.2778;

%% Función de transferencia
%%%Funcion Motor Rojo
Num1=[ki1];
Den1=[(La1*Jm1) ((Ra1*Jm1)+(Bm1*La1)) ((Ra1*Bm1)+(ki1*kv1))];
sys1=tf(Num1,Den1)
sys1rl=feedback(sys1,1)

% graficamos la respuesta con 2 voltios
figure
step(2*sys1)
grid on
title('Respuesta ante una señal escalón - motor rojo')
figure
bode(2*sys1)
grid on
title('Diagrama de bode - motor rojo')

% chequeamos la estabilidad del sistema retroalimentado
figure
rlocus(sys1rl)
grid on
title('Lugar Geometrico de las raices - motor rojo')

%%%Función Motor verde
Num2=[ki2];
Den2=[(La2*Jm2) ((Ra2*Jm2)+(Bm2*La2)) ((Ra2*Bm2)+(ki2*kv2))];
sys2=tf(Num2,Den2)
sys2rl=feedback(sys2,1)

figure
step(2*sys2)
grid on
title('Respuesta ante una señal escalón - motor verde')

figure
bode(2*sys2)
grid on
title('Diagrama de bode - motor verde')

figure
rlocus(sys2rl)
grid on
title('Lugar Geometrico de las raices - motor verde')

%% Simulacion de los motores (correr simulink)
% figure
% plot(t1,WnMot)
% grid on;


% figure
% plot(t1,WnMot)
% grid on;

%% Controlador PID


%%%Motor rojo




%%%Motor verde


