%% Initialize everything and load image
close all;
clear;

% Download image from ImageJ sample site
cellImage=imread('http://imagej.nih.gov/ij/images/Cell_Colony.jpg');
% it loads as an unsigned integer which is messy, convert it to double
cellImage=double(cellImage);

%% Show a preview of the image and histogram
subplot(2,1,1)
imagesc(cellImage);
colormap('gray');
title('Preview of Cell Image')
axis equal

subplot(2,1,2)
hist(cellImage(:),255);
title('Histogram of Cell Image')
pause(1); % wait a second before continuing 

%% Choose a threshold
subplot(2,1,1)
imagesc(cellImage<120)
colormap('default');
title('120 threshold')
subplot(2,1,2)
imagesc(cellImage<200)
title('200 threshold')

threshImage=cellImage<120;

%% Label and count the objects
labelImage=bwlabel(threshImage);
subplot(2,1,1)
imagesc(labelImage)
title('Labeled Image')
subplot(2,1,2)
hist(labelImage(labelImage>0),1:max(labelImage(:)))
title('Histogram of Labeled Image')
pause(1)

%% Calculate the average volume

volumeDistribution=hist(labelImage(labelImage>0),1:max(labelImage(:)));
disp(['Number of Cells:' num2str(length(volumeDistribution)) ', Average Volume:' num2str(mean(volumeDistribution))])    
