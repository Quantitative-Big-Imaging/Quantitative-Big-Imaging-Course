% Ex1.1
%% Load images

a=double(imread('data/scroll.tif'));
b=double(imread('data/wood.tif'));
c=double(imread('data/asphalt_gray.tif'));

%% Show images

figure(1)
% show the images with subplot and imagesc

%% compute SNR 
% Identify the region and extract a sub image
subA1=a(x1:x2,y1:y2);
snrA1=mean(subA1(:))/std(subA1(:)) % compute the snr

% Find a second region in a

% Repeat the procedure with images b and c


%% Load phantom images
% Exercise 1.2
d=double(mean(imread('data/testpattern.png'),3));

%% Create noisy image
figure(2)
ax2(1)=subplot(2,5,1); imagesc(d),axis image, title('Original')

scale = ??? ;
d_snr100=d+scale*randn(size(d));
ax2(6)=subplot(2,5,6); imagesc(d_snr100), axis image; title('SNR 100')

scale = ??? ;
d_snr10=d+scale*randn(size(d));
ax2(7)=subplot(2,5,7); imagesc(d_snr10), axis image; title('SNR 10')

scale = ??? ;
d_snr5=d+scale*randn(size(d));
ax2(8)=subplot(2,5,8); imagesc(d_snr5), axis image; title('SNR 5')

scale = ??? ;
d_snr2=d+scale*randn(size(d));
ax2(9)=subplot(2,5,9); imagesc(d_snr2), axis image; title('SNR 2')

scale = ??? ;
d_snr1=d+scale*randn(size(d));
ax2(10)=subplot(2,5,10); imagesc(d_snr1), axis image; title('SNR 1')

linkaxes(ax2)


%% Filter the images
% Exercise 2.1 Uniform

figure(3)

% Size of the filter window
N=[3 5 7];

% 
for i=1:3
    n=N(i);
    h= ??? ; % Define the filter kernel 
   ax3(1+(i-1)*5)=subplot(3,5,1+(i-1)*5); imagesc(filter2(h,d_snr100)), axis image, title(['SNR 100, Box ' num2str(n) 'x' num2str(n)]) 
   ax3(2+(i-1)*5)=subplot(3,5,2+(i-1)*5); imagesc(filter2(h,d_snr10)), axis image, title(['SNR 10, Box ' num2str(n) 'x' num2str(n)]) 
   ax3(3+(i-1)*5)=subplot(3,5,3+(i-1)*5); imagesc(filter2(h,d_snr5)), axis image, title(['SNR 5, Box ' num2str(n) 'x' num2str(n)]) 
   ax3(4+(i-1)*5)=subplot(3,5,4+(i-1)*5); imagesc(filter2(h,d_snr2)), axis image, title(['SNR 2, Box ' num2str(n) 'x' num2str(n)]) 
   ax3(5+(i-1)*5)=subplot(3,5,5+(i-1)*5); imagesc(filter2(h,d_snr1)), axis image, title(['SNR 1, Box ' num2str(n) 'x' num2str(n)]) 
end

linkaxes(ax3)

%% Exercise 2.1 Median

figure(4)

% Size of the filter window
N=[3 5 7];

for i=1:3
    n=N(i);
    fd = ??? ; % define the filter parameter
   ax4(1+(i-1)*5)=subplot(3,5,1+(i-1)*5); imagesc(medfilt2(d_snr100,fd)), axis image, title(['SNR 100, Box ' num2str(n) 'x' num2str(n)]) 
   ax4(2+(i-1)*5)=subplot(3,5,2+(i-1)*5); imagesc(medfilt2(d_snr10,fd)), axis image, title(['SNR 10, Box ' num2str(n) 'x' num2str(n)]) 
   ax4(3+(i-1)*5)=subplot(3,5,3+(i-1)*5); imagesc(medfilt2(d_snr5,fd)), axis image, title(['SNR 5, Box ' num2str(n) 'x' num2str(n)]) 
   ax4(4+(i-1)*5)=subplot(3,5,4+(i-1)*5); imagesc(medfilt2(d_snr2, fd)), axis image, title(['SNR 2, Box ' num2str(n) 'x' num2str(n)]) 
   ax4(5+(i-1)*5)=subplot(3,5,5+(i-1)*5); imagesc(medfilt2(d_snr1, fd)), axis image, title(['SNR 1, Box ' num2str(n) 'x' num2str(n)]) 
end

linkaxes(ax4)

%% Exercise 3.1

% Select different number of levels and wavelet types (eg coif, sym, db)
wname = 'sym6'; lev =2;

% Select different noise images or even experiment images
[c,s] = wavedec2(d_snr10,lev,wname);

% Estimate the noise standard deviation from the
% detail coefficients at level 1.
det1 = detcoef2('compact',c,s,1);
sigma = median(abs(det1))/0.6745;

% Use wbmpen for selecting global threshold  
% for image de-noising.
alpha = 1.2;
thr = wbmpen(c,1,sigma,alpha);

% Use wdencmp for de-noising the image using the above
% thresholds with soft thresholding and approximation kept.
keepapp = 1;
% Select threshold type 'h' or 's'
tt='s';
xd = wdencmp('gbl',c,s,wname,lev,thr,tt,keepapp);

figure(5)

ax5(1)=subplot(1,2,1); imagesc(d_snr10), axis image, title('Original')
ax5(2)=subplot(1,2,2); imagesc(xd), axis image, title(['Wavelet filtered with ' num2str(lev) ' levels of ' wname ])

linkaxes(ax5);

%% Exercise 3.2 Diffusion filter

addpath 'diffusion/'

% Tune the filter parameters for the three experiment images
lambda=1000;
sigma=1;
m=8;
stepsize=0.25;
steps=10;
y=nldif(a,lambda,sigma,m,stepsize,steps);

figure(6)

ax6(1)=subplot(1,2,1); imagesc(a), axis image, title('Original')
ax6(2)=subplot(1,2,2); imagesc(y), axis image, title('Nonlin diffusion')

linkaxes(ax5);

%% Exercise 4 Test run

% in separate file exercise4.m