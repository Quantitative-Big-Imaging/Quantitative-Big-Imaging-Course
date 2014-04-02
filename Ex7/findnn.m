% calculate nearest neighbor
function [nndist,nntheta] = findnn(xcol,ycol)
colIndex=1:length(xcol)
nndist=zeros(1,length(xcol));
nntheta=zeros(1,length(xcol));
for i=colIndex
    curX=xcol(i);
    curY=ycol(i);
    [mindist,minind]=min(sqrt((xcol(find(colIndex~=i))-curX).^2+(ycol(find(colIndex~=i))-curY).^2));
    
    if(minind>=i) 
        % since we remove the i-th element before computing
        minind=minind+1;
    end
    nndist(i)=mindist;
    nntheta(i)=atan2(ycol(minind)-curY,xcol(minind)-curX);
end

    