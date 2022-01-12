clc
clear all
close all  % this section just clears any previous code and variables

f = [-1 -1];  %here we define the objective function (negitive values because we seek to maximise the value)
A = [10 100; -1 0; 0 -1; 1 0; 0 1];  %here we define our constraints (upper bound and lowerbound are included
b = [1000 0 0 50 7];                 %here due to compatibility with the provided plotregion command)

Aeq = [];  %no equality constraints required for this problem
beq = [];
lowerb = [0 0];   %included upper and lowerbound for linprog
upperb = [50 7];  

[val,fval] = linprog(f,A,b,Aeq,beq,lowerb,upperb); %linprog solver

figure(1)
lb = [0 0]; % define lower bounds (just for plot axis)
ub = [60 10]; % define upper bound (just for plot axis)
plotregion(-A,-b,lb,ub,'g',0.5) %from Matlab File Exchange provided as part of course
xlabel('x1: Supplier One QALY Centuries'), ylabel('x2: Supplier Two QALY Centuries') %label Axis
axis([lb(1) ub(1) lb(2) ub(2)]), grid %draw plot axis
hold on 

x = [0 100];    %draw constraint representing max budget
y = [10 0];
pl = line(x,y);
pl.Color = 'blue';
pl.LineStyle = '--';

x = [0 60];   %draw constraint representing max demand from supplier two
y = [7 7];
pl = line(x,y);
pl.Color = 'blue';
pl.LineStyle = '-.';

x = [50 50]; %draw constraint representing max demand from supplier one
y = [0 10];
pl = line(x,y);
pl.Color = 'blue';
pl.LineStyle = ':';

x = [0 55]; %draw objective function
y = [55 0];
pl = line(x,y);
pl.Color = 'red';
pl.LineStyle = '--';

%%% label the legend of the plot
lgd = legend('Feasible Region','Budget Constraint','Limit of x2','Limit of x1','Objective Function','Interpreter','latex');
title(lgd,'Legend')