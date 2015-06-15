
#include <stdio.h>
#include <Xlib.h>
#include <Imlib2.h>
#include <stdlib.h>
#include <unistd.h>




static DATA32 *diff_data = NULL;
static Imlib_Image im_old = NULL;
static Imlib_Image im_new = NULL;

Imlib_Image im;
Display *disp = NULL;
Screen *scr = NULL;
Window root;
Visual *vis = NULL;
Colormap cm;
int depth;

static void rotateOutOldImage(){
	if(im_old){
		imlib_context_set_image(im_old);
		imlib_free_image();
	}
	im_old = im_new;
	im_new = NULL;
}


void init(){
	disp = XOpenDisplay(NULL);  //NULL here opens the display in environment var DISPLAY
	scr = ScreenOfDisplay(disp,DefaultScreen(disp));
	int scrnum = XScreenNumberOfScreen(scr);
    vis = DefaultVisual(disp, scrnum);
    depth = DefaultDepth(disp,scrnum);
    cm = DefaultColormap(disp, scrnum);
	root = RootWindow(disp, scrnum);
}

static Imlib_Image getScreenShot(){
	imlib_context_set_display(disp);
	imlib_context_set_visual(vis);
	imlib_context_set_colormap(cm);
	imlib_context_set_color_modifier(NULL);
	imlib_context_set_operation(IMLIB_OP_COPY);
	imlib_context_set_drawable(root);
	return imlib_create_image_from_drawable(0,0,0,scr->width,scr->height,1);
	//imlib_image_set_format('jpg');
	//imlib_save_image_with_error_return(im,)

}
//Get this im image into python....

static void makeDiffImage(){
	if(!im_old){
		im_old = getScreenShot();
	}
	imlib_context_set_image(im_old);
	im_new = getScreenShot();
	imlib_context_set_operation(IMLIB_OP_SUBTRACT);
	imlib_blend_image_onto_image(	im_new,0,
									0,0,imlib_image_get_width(),imlib_image_get_height(),
									0,0,imlib_image_get_width(),imlib_image_get_height());
}

DATA32 *getDiffImageData(){
	makeDiffImage();
	imlib_context_set_image(im_old);
	int n = imlib_image_get_width()* imlib_image_get_height();
	DATA32 *old_diff = imlib_image_get_data(); //32 bits per pixel ARGB format.
	if(diff_data){
		free(diff_data);
	}
	diff_data = (DATA32*)malloc(sizeof(DATA32)*n);
	int i;
	for(i = 0; i < n; i++){
		diff_data[i] = old_diff[i];
	}
	rotateOutOldImage();
	return diff_data;
}


float getPixelDiff(){
	makeDiffImage();
	imlib_context_set_image(im_old);
#ifdef DEBUG
	imlib_save_image("diffimage");
#endif
	int n = imlib_image_get_width()* imlib_image_get_height();
	DATA32 *dat_diff = imlib_image_get_data(); //32 bits per pixel ARGB format.
	int i;
	int diff = 0;
	for(i=0; i < n; i++){
		diff = diff + abs(dat_diff[i] & 0x000000FF); //Blue Channel
		diff = diff + abs( (dat_diff[i] >> 8) & 0x000000FF); //Green Channel
		diff = diff + abs( (dat_diff[i] >> 16) & 0x000000FF); //Red Channel
	}
	rotateOutOldImage();
	return ((float)diff)/((float)(n*255*3));
}


