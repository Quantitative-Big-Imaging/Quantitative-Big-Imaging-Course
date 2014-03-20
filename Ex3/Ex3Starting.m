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

%% Perform an open operation (hint use the bwmorph command in the image processing toolbox)

cleanImage = ???


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


%% Robust threshold selection

% the goal of this is to get the curve to be as flat as possible (insensitive to threshold value)
% by filtering and performing morphological operations well

% use the appropriate filter command for the image
filtImage = ??? 
threshValues=[min(filtImage(:)):max(filtImage(:))];
objectCount=zeros(1,length(threshValues));
objectVolume=zeros(1,length(threshValues));

for cStep=1:length(threshValues)
    threshImage=filtImage<threshValues(cStep);
    % perform appropriate cleaning operations
    cleanImage= ??? ;
    labelImage=bwlabel(cleanImage);
    volumeDistribution=hist(labelImage(labelImage>0),1:max(labelImage(:)));
    objectCount(cStep)=length(volumeDistribution);
    objectVolume(cStep)=mean(volumeDistribution);
end

subplot(2,1,1)
plot(threshValues,objectCount,'r.-')
xlabel('Threshold Value');
ylabel('Number of objects');

subplot(2,1,2)
semilogy(threshValues,objectVolume,'r.-')
xlabel('Threshold Value');
ylabel('Average Volume of objects')

