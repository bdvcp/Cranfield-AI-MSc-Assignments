clear all
close all
clc       % this section just clears any previous code and variables

f = [-1 -1 -0.1]; %here we define the objective function (negitive values because we seek to maximise the value)

A = [10 100 3.5]; %here we define our constraint
b = [1001];
Aeq = [];   %no equality constraint for this problem
beq = [];
intcon = 3;   %this value is the variable which is integer only

lb = [0 0 0];   %lower bound for variables
ub = [50 7 37];  %upper bound for variables

% intlinprog command to find answer where val are the optimum values for
% the decision variables.
[val,fval]=intlinprog(f,intcon,A,b,Aeq,beq,lb,ub);