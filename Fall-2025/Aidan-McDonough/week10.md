# Design Log Week 10

## Status: 

I am not currently stuck or blocked.

## Work Completed

### Vertex Shader 

- Controller calls  kernal per vertex

- Instead of matrix multiplication for translation in 3D: 
    - input line to rotate around
    - normalize vertex to line
    - rotate about line via creation of rotation matrix then matrix multiplication
    - move vertex back to original 
- Pinhole camera model -> translation from 3D to 2D [CS334](https://cs.purdue.edu/cgvlab/courses/334/Fall_2025/Lectures/PHC.pdf)
    - input: float of horizontal field of view in degrees, int of width and height of image in 
    - P is the 3D point in the world space
    - C is the camera center(origin in our case)
    - a, b are horizontal and vertical 3D vectors of the image plane
    - c distance form top left of image plane to camera
    - Normalize 3D w.r.t camera:
        - $ \begin{bmatrix} u \\ v \\ l \end{bmatrix} * w = $ $\begin{bmatrix}
            a_x & b_x & c_x \\
            a_y & b_y & c_y \\
            a_z & b_z & c_z
            \end{bmatrix}^{-1}$ *  $\begin{bmatrix}
            P_x - C_x \\
            P_y - C_y \\
            P_z - C_z \end{bmatrix} $

        - $\begin{bmatrix} u \\ v \end{bmatrix}
        = \dfrac{1}{w}
        \begin{bmatrix} uw \\ vw \end{bmatrix}$
        - $ l = \dfrac{1}{w} $

### Next Steps:
 - Rework vertex kernel 
 - Connect final kernel output to openGL draw pixels to render image to screen
    - incorporate into main function
    - use for debug and confirm functionailty before on cpusim before functsim
 - Debug kernels to confirm correct operation 

