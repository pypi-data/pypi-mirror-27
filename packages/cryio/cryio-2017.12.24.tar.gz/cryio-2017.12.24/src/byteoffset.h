#ifndef CRYIO_BYTEOFFSET_H_   /* Include guard */
#define CRYIO_BYTEOFFSET_H_

#include <stdlib.h>
#include <stdint.h>
#include <Python.h>

typedef struct {
    void *mem;
    Py_ssize_t dim1;
    Py_ssize_t dim2;
    Py_ssize_t n_pixels;
    Py_ssize_t buf_size;
    Py_ssize_t shape[2];
    Py_ssize_t strides[2];
} cbfdata;

typedef struct {
    int8_t *data;
    Py_ssize_t data_size;
} cbfpacked;

cbfdata* _decode_byte_offset(int dim1, int dim2, char* buf);
cbfpacked *_encode_byte_offset(Py_buffer *buf);
void destroy_cbfpacked(cbfpacked *cbfp);
void _destroy_cbf(cbfdata *cbf);

#endif  // CRYIO_BYTEOFFSET_H_
