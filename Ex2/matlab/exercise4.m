%% Setup

addpath 'diffusion/'
addpath 'metrics/'

clear all;

%% Create test images

a=double(mean(imread('data/testpattern.png'),3));

% define scales to obtain SNR 1,2,5,10,20,50,100

SNR = [1 2 5 10 20 50 100];
scales = SNR * scale;

Ntests = 10;

%% Test run for filter 1

mse1(length(scales),Ntests)=0;
ssim1(length(scales), Ntests)=0;

for i=1:length(scales)
    
    for j=1:Ntests
        x=your_filter1(a+scale(i)*randn(size(a))); % replace 'your_filter' with the chosen filter and its parameters
        mse1(i,j)=mse(a,x);
        ssim1(i,j)=ssim(a,x);
    end
    
    % Add some lines here to display the latest image in a subplot,prepared
    % for link axes
end

loglog(SNR,mean(mse1,2)); % Add annotations for the plot and axes
semilogx(SNR,mean(ssim1,2));


%% Test run for filter 2

% repeat the code from filter 1 
