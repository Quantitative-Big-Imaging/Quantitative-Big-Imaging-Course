function m=mse(x,y)
%
% m=mse(x,y)
% Computes the mean squared difference between two matrices x and y
%
% Author: Anders Kaestner, Paul Scherrer Institut
%
d=x(:)-y(:);

m=a(:)'*a(:)/length(d);