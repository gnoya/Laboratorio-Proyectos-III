close all
%%%Definición de parámetros%%%
La=1.76e-4;
Jm=2.1393e-5;
Ra=1.1724;
Bm=0.0115;
ki=0.2864;
kv=0.2864;
%%%Función de transferencia%%%

Num=[ki];
Den=[(La*Jm) ((Ra*Jm)+(Bm*La)) ((Ra*Bm)+(ki*kv))];
sys=tf(Num,Den);
step(2*sys)
figure
plot(t1,WnMot)
grid on;