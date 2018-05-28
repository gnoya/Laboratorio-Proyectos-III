%Clearing variables in memory and Matlab command screen
close all;
clc;
%Dimensions of the simulation grid in x (xdim) and y (ydim) directions
xdim=50;
ydim=50;
i=1:1:xdim;
j=2:1:ydim;
%Initializing previous (V_prev) and present (V_now) voltage matrices
V_now=5*zeros(xdim,ydim);
V_prev=5*zeros(xdim,ydim);
V_now(1,j)=0;
V_now(50,j)=0;
V_now(i,1)=0;
V_now(i,50)=0;
%Initializing boundary conditions only for V_now
%boundaries are going to remain at zero volts
V_now(25,25)=10;
V_now(30,30)=10;
V_now(20,20)=-10;
V_now(10,10)=-10;
%Iteration counter
iter=0;
%error
error=max(max(abs(abs(V_now)-abs(V_prev))));

%Iteration loop
while(error>0.01)%Run this until convergence
    
    iter=iter+1; % Iteration counter increment
    
    % Updating present iteration using 4 point Central diffrence form
    % of Laplace equation obtained using Finite Difference method
    for i=2:1:xdim-1
        for j=2:1:ydim-1
            if ((i==25) && (j==25)) || ((i==30) && (j==30))
                V_now(25,25)=10;
                V_now(30,30)=10;
            elseif ((i==10) && (j==10)) || ((i==20) && (j==20))
                 V_now(10,10)=-10;
                 V_now(20,20)=-10;
            else
                V_now(i,j)=(V_now(i-1,j)+V_now(i+1,j)+V_now(i,j-1)+V_now(i,j+1))/4;
            end    
            
        end
    end
    error=max(max(abs(V_now-V_prev))); % Calculate the maximum error between previous and current iteration at all points
    V_prev=V_now; % Updating previous iteration matrix to the last iteration performed
    
    %Movie type colour scaled image plot to see how solution progresses
    imagesc(V_now);colorbar;
    title(['Potential distrubution on a ',int2str(xdim),' x ',int2str(ydim),' grid at iteration no ',int2str(iter)],'Color','k');
    getframe;
end

%Plot the electric field distribution
figure;
[X,Y]=meshgrid(1:1:50);
[ex,ey]=gradient(V_now);
contour(X,Y,V_now);
hold on
quiver(X,Y,ex,ey,2); %Quiver command creates a plot, E=-grad(V), hence the negative sign
colormap hsv
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% END OF PROGRAM
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%