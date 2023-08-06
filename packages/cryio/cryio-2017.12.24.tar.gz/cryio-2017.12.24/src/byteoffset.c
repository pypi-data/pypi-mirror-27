#include <stdlib.h>
#include <stdint.h>
#include "cryio.h"
#include "byteoffset.h"


static cbfdata *alloc_cbf(int dim1, int dim2) {
    cbfdata *cbf;

    cbf = (cbfdata *)malloc(sizeof(cbfdata));
    if (cbf == NULL)
        return NULL;

    cbf->dim1 = (Py_ssize_t)dim1;
    cbf->dim2 = (Py_ssize_t)dim2;
    cbf->n_pixels = cbf->dim1 * cbf->dim2;
    cbf->buf_size = cbf->n_pixels * sizeof(int32_t);
    cbf->shape[0] = cbf->dim1;
    cbf->shape[1] = cbf->dim2;
    cbf->strides[0] = cbf->dim2 * sizeof(int32_t);
    cbf->strides[1] = sizeof(int32_t);
    cbf->mem = malloc(cbf->buf_size);
    if (cbf->mem == NULL) {
        _destroy_cbf(cbf);
        return NULL;
    }
    return cbf;

}


cbfdata *_decode_byte_offset(int dim1, int dim2, char *buf)
{
    int8_t delta8;
    int16_t delta16;
    int32_t pixel, *array;
    Py_ssize_t i;
    cbfdata *out;

    out = alloc_cbf(dim1, dim2);
    if (out == NULL)
        return NULL;

    pixel = 0;
    array = (int32_t *)out->mem;
    for (i=0; i<out->n_pixels; ++i) {
        delta8 = *(int8_t *)buf;
        buf += sizeof(int8_t);
        if ((delta8 & 0xff) == 0x80) {
            delta16 = *(int16_t *)buf;
            buf += sizeof(int16_t);
            if ((delta16 & 0xffff) == 0x8000) {
                pixel += *(int32_t *)buf;
                buf += sizeof(int32_t);
            } else {
                pixel += delta16;
            }
        } else {
            pixel += delta8;
        }
        *array++ = pixel;
    }
    return out;
}


cbfpacked *_encode_byte_offset(Py_buffer *buf) {
    Py_ssize_t i;
    int32_t diff, nval, cval, adiff, *array;
    memptr t;
    cbfpacked *cbf;

    cbf = malloc(sizeof(cbfpacked) + buf->len);
    if (cbf == NULL)
        return NULL;
    cbf->data = (int8_t *)(cbf + 1);
    cval = 0;
    array = (int32_t *)buf->buf;
    t._8 = cbf->data;
    for (i=0; i<buf->shape[0]*buf->shape[1]; ++i) {
        nval = *array++;
        diff = nval - cval;
        adiff = abs(diff);
        if (adiff < 0x80) {
            *t._8++ = (int8_t)diff;
        } else {
            *t._8++ = 0x80;
            if (adiff < 0x8000) {
                *t._16++ = (int16_t)diff;
            } else {
                *t._16++ = 0x8000;
                *t._32++ = diff;
            }
        }
        cval = nval;
    }
    cbf->data_size = (Py_ssize_t)(t._8 - cbf->data);
    return cbf;
}


void destroy_cbfpacked(cbfpacked *cbfp) {
    if (cbfp != NULL)
        free(cbfp);
}


void _destroy_cbf(cbfdata *cbf) {
    if (cbf != NULL) {
        if (cbf->mem != NULL) {
            free(cbf->mem);
        }
        free(cbf);
    }
}
