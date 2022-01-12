clear all
close all
clc       % this section just clears any previous code and variables

% This defines our objective function which is the sum of all of our
% variables (negitive due to it being a maximisation problem)
fun = @(x)(-x(1) - x(2) - x(3));

%The start point from which our algorithm begins it's analysis
x0 = [0 0 0];

%no linear constraints in this case
A = [];
b = [];
Aeq = [];
beq = [];

%lower bound of the variables as defined by policy makers.
lb = [0 2 10];

%upper bound of the variables as defined by the limits of necessity
ub = [50 7 100];

%defines the non linear constraint
nonlcon = @nonlinearfunction;

%the parameters and syntax of the fmincon function
options = optimoptions('fmincon','Display','iter','Algorithm','sqp');
[x,fval] = fmincon(fun,x0,A,b,Aeq,beq,lb,ub,nonlcon);

%defines the function used for the budget constraint with the discount
function [c,ceq]=nonlinearfunction(x);
    c = (10*x(1) + 100*x(2) + 20*x(3))^0.95 - 1000;
    ceq = [];
end

