% image_generator
% cell_count is the number of cells in each image
% illumination level is the brightness of the source
% noise_level is the strength of the noise signal (normally distributed
% gaussian the standard deviation is specificed)

function out_im = image_generator(cell_count,noise_level,illum_level)
% default settings
im_size=[512,512];
cell_rad=10; % cell radius
cell_abs=0.02; % absorption coefficient
% coordinate system
[xx,yy]=meshgrid(1:im_size(1),1:im_size(2));

% create source
source_im=illum_level.*(1+noise_level*randn(im_size));

% create list of cells
cell_pos=rand(cell_count,2);
cell_pos(:,1)=cell_pos(:,1)*im_size(1);
cell_pos(:,2)=cell_pos(:,2)*im_size(2);
% create cell thickness map
cell_thickness=zeros(im_size);
for cur_cell = 1:cell_count
    cur_cell_thickness=real(sqrt(cell_rad.^2-(xx-cell_pos(cur_cell,1)).^2-(yy-cell_pos(cur_cell,2)).^2));
    cell_thickness = cell_thickness + cur_cell_thickness;
end

out_im=uint8(255*source_im .* exp(- cell_abs*cell_thickness));


