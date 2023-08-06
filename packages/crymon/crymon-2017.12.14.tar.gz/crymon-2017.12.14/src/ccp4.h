#ifndef CRYMON_CCP4_H_   /* Include guard */
#define CRYMON_CCP4_H_

#include <stdlib.h>
#include <stdint.h>

enum int_type {
    volume,
    layer
};

typedef struct {
    float distance;
    float wavelength;
    float alpha;
    float beta;
    float xc;
    float yc;
    float ub[3 * 3];
    float d1;
    float d2;
    float d3;
    float cell_a;
    float cell_b;
    float cell_c;
    float cell_alpha;
    float cell_beta;
    float cell_gamma;
    float b2;
    float omega0;
    float theta0;
    float kappa0;
    float phi0;
    float pixel;
    int inhor;
    int inver;
} parfile;

typedef struct {
    float b[3][3];
    float cell[3][3];
    float ub[3][3];
    float u[3][3];
    float g[3][3];
    float uu[3][3];
} cell_matrices;

typedef struct {
    /* The description of the ccp4 header is given here:
     * http://www.ccp4.ac.uk/html/maplib.html#description
     */
    int32_t nc;
    int32_t nr;
    int32_t ns;
    int32_t mode;
    int32_t ncstart;
    int32_t nrstart;
    int32_t nsstart;
    int32_t nx;
    int32_t ny;
    int32_t nz;
    float xlen;
    float ylen;
    float zlen;
    float alpha;
    float beta;
    float gamma;
    int32_t mapc;
    int32_t mapr;
    int32_t maps;
    int32_t zeros[237];
} ccp4header;

typedef struct {
    float h;
    float k;
    float l;
} t_hkl;

typedef struct {
    t_hkl p0;
    t_hkl p1;
    t_hkl pc;
    float thickness;
    float qmax;
    float dQ;
    int downsample;
    int x;
    int y;
    int z;
    int lorentz;
    int scale;
    int n_voxels;
} t_slice;

typedef struct {
    parfile *par;
    cell_matrices *mtx;
    int s_array;
    int s_buf;
    int s_output;
    float *lorentz;
    float *kxA;
    float *kyA;
    float *kzA;
    float *voxval;
    int *voxcount;
    float *voxels;
    int s_voxels;
    ccp4header *ccp4_hdr;
    int map_calculated;
    t_slice *slice;
    enum int_type type;
} geometry;

void ccp4_destroy(geometry *geo);
void ccp4_add_array(geometry *geo, float *array, float angle, float osc);
void ccp4_map(geometry *geo);
int ccp4_init_par(geometry *geo);
geometry *ccp4_init_geo(enum int_type type, t_slice *slice);

#endif /* CRYMON_CCP4_H_ */
