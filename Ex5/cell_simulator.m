% cell_simulator
% Author: Kevin Mader (kevinmader@gmail.com)
%   
% Cell simulator generates a given number of cells with a given radius 
% Usage:
%   [outImage,out_pos,out_shape,out_theta] = cell_simulator(100,10,5,0,1);
%       Outputs the image, the list of positions, the shape, and the orientations
%       For 100 cells, with average semiaxis length of 10 and standard deviation of 5
%       with 0 noise and a 100% illumination
% Parameters:
%   cell_count is the number of cells in each image
%   cell_radius is the mean semiaxis length for the ellipse
%   cell_radius_std is the standard deviation of the semiaxis length
%   noise_level is the strength of the noise signal (normally distributed
%   gaussian the standard deviation is specificed)
%   illumination level is the brightness of the source


function [out_im,cell_pos,cell_shape,cell_theta] = cell_simulator(cell_count,cell_radius,cell_radius_std,noise_level,illum_level)
% default settings
im_size=[512,512];
cell_abs=0.02; % absorption coefficient
% coordinate system
[xx,yy]=meshgrid(1:im_size(1),1:im_size(2));

% create source with a fixed illumination scaled by a random value at each point
source_im=normrnd(illum_level,noise_level,im_size(1),im_size(2));

% create list of cells

% first the positions
cell_pos=rand(cell_count,2);
cell_pos(:,1)=cell_pos(:,1)*im_size(1);
cell_pos(:,2)=cell_pos(:,2)*im_size(2);

% now the shape
cell_shape=normrnd(cell_radius,cell_radius_std,cell_count,2);
% reorder to the first length is always the longest
cell_shape=[max(cell_shape,[],2),min(cell_shape,[],2)];

% now the orientation
cell_theta=2*pi*rand(cell_count,1);

% create cell thickness map
cell_thickness=zeros(im_size);
for cur_cell = 1:cell_count
    % calculate cell coordinates (center of volume at 0)
    cur_cell_x=(xx-cell_pos(cur_cell,1));
    cur_cell_y=(yy-cell_pos(cur_cell,2));
    % rotate these axes to rotate the cell (see coordinate system rotation)
    cur_cell_x_rot=cos(cell_theta(cur_cell))*cur_cell_x-sin(cell_theta(cur_cell))*cur_cell_y;
    cur_cell_y_rot=sin(cell_theta(cur_cell))*cur_cell_x+cos(cell_theta(cur_cell))*cur_cell_y;
    % calculate the thickness in the new coordinates
    cur_cell_thickness=real(sqrt(1-(cur_cell_x_rot/cell_shape(cur_cell,1)).^2-(cur_cell_y_rot/cell_shape(cur_cell,2)).^2));
    % add to the existing image
    cell_thickness = cell_thickness + cur_cell_thickness;
end

out_im=uint8(255*source_im .* exp(- cell_abs*cell_thickness));


