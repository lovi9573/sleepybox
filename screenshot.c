
#include <stdio.h>
#include <Xlib.h>
#include <Imlib2.h>





void getScreenShot(){
	Imlib_Image im;
	Display *disp = NULL;
	Screen *scr = NULL;
	Window root;
	Visual *vis = NULL;
	Colormap cm;
	int depth;
	printf("a\n");
	fflush(stdout);
	disp = XOpenDisplay(NULL);  //NULL here opens the display in environment var DISPLAY
	printf("b%x\n",disp);
	fflush(stdout);
	scr = ScreenOfDisplay(disp,DefaultScreen(disp));
	printf("c%x\n",scr);
	fflush(stdout);
	int scrnum = XScreenNumberOfScreen(scr);
	printf("d-%d\n",scrnum);
	fflush(stdout);
    vis = DefaultVisual(disp, scrnum);
    depth = DefaultDepth(disp,scrnum);
    cm = DefaultColormap(disp, scrnum);
	root = RootWindow(disp, scrnum);
	printf("d%x\n",&root);
	fflush(stdout);
	imlib_context_set_display(disp);
	imlib_context_set_visual(vis);
	imlib_context_set_colormap(cm);
	imlib_context_set_color_modifier(NULL);
	imlib_context_set_operation(IMLIB_OP_COPY);
	imlib_context_set_drawable(root);
	printf("e\n");
	fflush(stdout);
	im  = imlib_create_image_from_drawable(0,0,0,scr->width,scr->height,1);
	printf("f%x\n",im);
	fflush(stdout);
	imlib_context_set_image(im);
	//imlib_image_set_format('jpg');
	//imlib_save_image_with_error_return(im,)

}
//Get this im image into python....

int main(int argc, char* argv[]){
	printf("a-");
	//Imlib_Image im;
	getScreenShot();
	printf("w: %d, h: %d\n",imlib_image_get_width(), imlib_image_get_height());
	printf("%d",imlib_image_get_data());
}
