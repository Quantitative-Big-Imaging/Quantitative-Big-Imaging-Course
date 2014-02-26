function [ss,info]=ssim(A,B,window,C)

if nargin<3
    window=[3 3];
end

if nargin<4
    C=[0 0 0];
end

Kr=ones(window(1),1);
Kc=ones(1,window(2));

mA=filter2(Kc,filter2(Kr,A)); % compute the neigborhood sum
s2A=filter2(Kc,filter2(Kr,A.^2)); % compute the squared neigborhood sum

mB=filter2(Kc,filter2(Kr,B)); % compute the neigborhood sum
s2B=filter2(Kc,filter2(Kr,B.^2)); % compute the squared neigborhood sum

M=prod(window(1:2));
info.mA=mA/M;
info.mB=mB/M;

cAB=filter2(Kc,filter2(Kr,(A-info.mA).*(B-info.mB)))/M;


info.sA=sqrt(1/(M-1)*(s2A-1/M*mA.^2)); % Use the sums to compute the local standard deviaton
info.sB=sqrt(1/(M-1)*(s2B-1/M*mB.^2)); % Use the sums to compute the local standard deviaton

info.l=(2*info.mA.*info.mB+C(1))./(info.mA.^2+info.mB.^2+C(1));
info.s=(2*info.sA.*info.sB+C(2))./(info.sA.^2+info.sB.^2+C(2));
info.c=((cAB+C(3))./(info.sA.*info.sB+C(3)))
info.ssid=info.l .* info.s .* info.c;

ss=mean(info.ssid(:));