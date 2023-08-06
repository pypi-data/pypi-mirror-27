/*
 * Different data format io routines
 */

#include <Python.h>
#include "byteoffset.h"
#include "agi_bitfield.h"
#include "mar345.h"


typedef struct {
    PyObject_HEAD
    cbfdata *cbf;
} _cbf_decode;


static int
_cbf_decode_init(_cbf_decode *self, PyObject *args) {
    int dim1, dim2;
    PyObject *bytes;
    Py_buffer cbf_buf;
    cbfdata *cbf;

    if (!PyArg_ParseTuple(args, "iiO", &dim1, &dim2, &bytes))
        return -1;

    _destroy_cbf(self->cbf);
    PyObject_GetBuffer(bytes, &cbf_buf, PyBUF_C_CONTIGUOUS);
    Py_BEGIN_ALLOW_THREADS
    cbf = _decode_byte_offset(dim1, dim2, (char *)cbf_buf.buf);
    Py_END_ALLOW_THREADS
    if (cbf == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory for CBF decompression");
        return -1;
    }
    PyBuffer_Release(&cbf_buf);
    self->cbf = cbf;
    return 0;
}


static void
_cbf_decode_dealloc(_cbf_decode *self) {
    _destroy_cbf(self->cbf);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static int
_cbf_decode_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    _cbf_decode *self = (_cbf_decode *)obj;
    view->obj = (PyObject *)self;
    view->buf = (void *)self->cbf->mem;
    view->len = self->cbf->buf_size;
    view->readonly = 0;
    view->itemsize = sizeof(int32_t);
    view->format = "i";
    view->ndim = 2;
    view->shape = self->cbf->shape;
    view->strides = self->cbf->strides;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);
    return 0;
}


static PyBufferProcs _cbf_decode_as_buffer = {
  (getbufferproc)_cbf_decode_getbuffer,
  (releasebufferproc)0,
};


static PyTypeObject _cbf_decode_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_cryio._cbf_decode",             /* tp_name */
    sizeof(_cbf_decode),              /* tp_basicsize */
    0,                                /* tp_itemsize */
    (destructor)_cbf_decode_dealloc,  /* tp_dealloc */
    0,                                /* tp_print */
    0,                                /* tp_getattr */
    0,                                /* tp_setattr */
    0,                                /* tp_reserved */
    0,                                /* tp_repr */
    0,                                /* tp_as_number */
    0,                                /* tp_as_sequence */
    0,                                /* tp_as_mapping */
    0,                                /* tp_hash  */
    0,                                /* tp_call */
    0,                                /* tp_str */
    0,                                /* tp_getattro */
    0,                                /* tp_setattro */
    &_cbf_decode_as_buffer,           /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,               /* tp_flags */
    "_cbf_decode object",             /* tp_doc */
    0,                                /* tp_traverse */
    0,                                /* tp_clear */
    0,                                /* tp_richcompare */
    0,                                /* tp_weaklistoffset */
    0,                                /* tp_iter */
    0,                                /* tp_iternext */
    0,                                /* tp_methods */
    0,                                /* tp_members */
    0,                                /* tp_getset */
    0,                                /* tp_base */
    0,                                /* tp_dict */
    0,                                /* tp_descr_get */
    0,                                /* tp_descr_set */
    0,                                /* tp_dictoffset */
    (initproc)_cbf_decode_init,       /* tp_init */
};


typedef struct {
    PyObject_HEAD
    cbfpacked *bytes;
} _cbf_encode;


static int
_cbf_encode_init(_cbf_encode *self, PyObject *args) {
    PyObject *np_array;
    Py_buffer array;
    cbfpacked *bytes;

    if (!PyArg_ParseTuple(args, "O", &np_array))
        return -1;
    destroy_cbfpacked(self->bytes);
    PyObject_GetBuffer(np_array, &array, PyBUF_C_CONTIGUOUS);
    Py_BEGIN_ALLOW_THREADS
    bytes = _encode_byte_offset(&array);
    Py_END_ALLOW_THREADS
    if (bytes == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory for CBF compression");
        return -1;
    }
    PyBuffer_Release(&array);
    self->bytes = bytes;
    return 0;
}


static void
_cbf_encode_dealloc(_cbf_encode *self) {
    destroy_cbfpacked(self->bytes);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static int
_cbf_encode_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    _cbf_encode *self = (_cbf_encode *)obj;
    view->obj = (PyObject *)self;
    view->buf = (void *)self->bytes->data;
    view->len = self->bytes->data_size;
    view->readonly = 1;
    view->itemsize = sizeof(int8_t);
    view->format = "c";
    view->ndim = 0;
    view->shape = NULL;
    view->strides = NULL;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);
    return 0;
}


static PyBufferProcs _cbf_encode_as_buffer = {
  (getbufferproc)_cbf_encode_getbuffer,
  (releasebufferproc)0,
};


static PyTypeObject _cbf_encode_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_cryio._cbf_encode",             /* tp_name */
    sizeof(_cbf_encode),              /* tp_basicsize */
    0,                                /* tp_itemsize */
    (destructor)_cbf_encode_dealloc,  /* tp_dealloc */
    0,                                /* tp_print */
    0,                                /* tp_getattr */
    0,                                /* tp_setattr */
    0,                                /* tp_reserved */
    0,                                /* tp_repr */
    0,                                /* tp_as_number */
    0,                                /* tp_as_sequence */
    0,                                /* tp_as_mapping */
    0,                                /* tp_hash  */
    0,                                /* tp_call */
    0,                                /* tp_str */
    0,                                /* tp_getattro */
    0,                                /* tp_setattro */
    &_cbf_encode_as_buffer,           /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,               /* tp_flags */
    "_cbf_encode object",             /* tp_doc */
    0,                                /* tp_traverse */
    0,                                /* tp_clear */
    0,                                /* tp_richcompare */
    0,                                /* tp_weaklistoffset */
    0,                                /* tp_iter */
    0,                                /* tp_iternext */
    0,                                /* tp_methods */
    0,                                /* tp_members */
    0,                                /* tp_getset */
    0,                                /* tp_base */
    0,                                /* tp_dict */
    0,                                /* tp_descr_get */
    0,                                /* tp_descr_set */
    0,                                /* tp_dictoffset */
    (initproc)_cbf_encode_init,       /* tp_init */
};


typedef struct {
    PyObject_HEAD
    espdata *esp;
} _esp_encode;


static int
_esp_encode_init(_esp_encode *self, PyObject *args) {
    PyObject *np_array;
    Py_buffer array;
    espdata *esp;

    if (!PyArg_ParseTuple(args, "O", &np_array))
        return -1;
    _destroy_esp(self->esp);
    PyObject_GetBuffer(np_array, &array, PyBUF_C_CONTIGUOUS);
    if (array.shape[0] != array.shape[1] || (array.shape[0] % 4) != 0) {
        PyErr_SetString(PyExc_TypeError, "The dimensions of the esperanto image are wrong.");
        return -1;
    }
    Py_BEGIN_ALLOW_THREADS
    esp = encode_agi_bitfield(&array);
    Py_END_ALLOW_THREADS
    if (esp == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory for Esperanto compression");
        return -1;
    }
    PyBuffer_Release(&array);
    self->esp = esp;
    return 0;
}


static void
_esp_encode_dealloc(_esp_encode *self) {
    _destroy_esp(self->esp);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static int
_esp_encode_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    _esp_encode *self = (_esp_encode *)obj;
    view->obj = (PyObject *)self;
    view->buf = (void *)self->esp->mem;
    view->len = self->esp->buf_size;
    view->readonly = 1;
    view->itemsize = sizeof(int8_t);
    view->format = "c";
    view->ndim = 0;
    view->shape = NULL;
    view->strides = NULL;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);
    return 0;
}


static PyBufferProcs _esp_encode_as_buffer = {
  (getbufferproc)_esp_encode_getbuffer,
  (releasebufferproc)0,
};


static PyTypeObject _esp_encode_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_cryio._esp_encode",             /* tp_name */
    sizeof(_esp_encode),              /* tp_basicsize */
    0,                                /* tp_itemsize */
    (destructor)_esp_encode_dealloc,  /* tp_dealloc */
    0,                                /* tp_print */
    0,                                /* tp_getattr */
    0,                                /* tp_setattr */
    0,                                /* tp_reserved */
    0,                                /* tp_repr */
    0,                                /* tp_as_number */
    0,                                /* tp_as_sequence */
    0,                                /* tp_as_mapping */
    0,                                /* tp_hash  */
    0,                                /* tp_call */
    0,                                /* tp_str */
    0,                                /* tp_getattro */
    0,                                /* tp_setattro */
    &_esp_encode_as_buffer,           /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,               /* tp_flags */
    "_esp_encode object",             /* tp_doc */
    0,                                /* tp_traverse */
    0,                                /* tp_clear */
    0,                                /* tp_richcompare */
    0,                                /* tp_weaklistoffset */
    0,                                /* tp_iter */
    0,                                /* tp_iternext */
    0,                                /* tp_methods */
    0,                                /* tp_members */
    0,                                /* tp_getset */
    0,                                /* tp_base */
    0,                                /* tp_dict */
    0,                                /* tp_descr_get */
    0,                                /* tp_descr_set */
    0,                                /* tp_dictoffset */
    (initproc)_esp_encode_init,       /* tp_init */
};


typedef struct {
    PyObject_HEAD
    mardata *mar;
} _mar_decode;


static int
_mar_decode_init(_mar_decode *self, PyObject *args) {
    int32_t dim1, dim2, n_ovf;
    PyObject *mar_bytes, *ovf_bytes;
    Py_buffer mar_buf, ovf_buf;
    mardata *mar;

    if (!PyArg_ParseTuple(args, "IIIOO", &dim1, &dim2, &n_ovf, &ovf_bytes, &mar_bytes))
        return -1;

    _destroy_mar(self->mar);
    PyObject_GetBuffer(ovf_bytes, &ovf_buf, PyBUF_C_CONTIGUOUS);
    PyObject_GetBuffer(mar_bytes, &mar_buf, PyBUF_C_CONTIGUOUS);
    Py_BEGIN_ALLOW_THREADS
    mar = _decode_mar_image(dim1, dim2, n_ovf, (char *)mar_buf.buf, (char *)ovf_buf.buf);
    Py_END_ALLOW_THREADS
    if (mar == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory for MAR345 decompression");
        return -1;
    }
    PyBuffer_Release(&mar_buf);
    PyBuffer_Release(&ovf_buf);
    self->mar = mar;
    return 0;
}


static void
_mar_decode_dealloc(_mar_decode *self) {
    _destroy_mar(self->mar);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static int
_mar_decode_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    _mar_decode *self = (_mar_decode *)obj;
    view->obj = (PyObject *)self;
    view->buf = (void *)self->mar->image;
    view->len = self->mar->buf_size;
    view->readonly = 0;
    view->itemsize = sizeof(uint32_t);
    view->format = "I";
    view->ndim = 2;
    view->shape = self->mar->shape;
    view->strides = self->mar->strides;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);
    return 0;
}


static PyBufferProcs _mar_decode_as_buffer = {
  (getbufferproc)_mar_decode_getbuffer,
  (releasebufferproc)0,
};


static PyTypeObject _mar_decode_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_cryio._mar_decode",             /* tp_name */
    sizeof(_mar_decode),              /* tp_basicsize */
    0,                                /* tp_itemsize */
    (destructor)_mar_decode_dealloc,  /* tp_dealloc */
    0,                                /* tp_print */
    0,                                /* tp_getattr */
    0,                                /* tp_setattr */
    0,                                /* tp_reserved */
    0,                                /* tp_repr */
    0,                                /* tp_as_number */
    0,                                /* tp_as_sequence */
    0,                                /* tp_as_mapping */
    0,                                /* tp_hash  */
    0,                                /* tp_call */
    0,                                /* tp_str */
    0,                                /* tp_getattro */
    0,                                /* tp_setattro */
    &_mar_decode_as_buffer,           /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,               /* tp_flags */
    "_mar_decode object",             /* tp_doc */
    0,                                /* tp_traverse */
    0,                                /* tp_clear */
    0,                                /* tp_richcompare */
    0,                                /* tp_weaklistoffset */
    0,                                /* tp_iter */
    0,                                /* tp_iternext */
    0,                                /* tp_methods */
    0,                                /* tp_members */
    0,                                /* tp_getset */
    0,                                /* tp_base */
    0,                                /* tp_dict */
    0,                                /* tp_descr_get */
    0,                                /* tp_descr_set */
    0,                                /* tp_dictoffset */
    (initproc)_mar_decode_init,       /* tp_init */
};


static PyMethodDef _cryio_methods[] = {
    {NULL, NULL, 0, NULL}
};


struct module_state {
    PyObject *error;
};


#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))


static int _cryio_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}


static int _cryio_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_cryio",
    NULL,
    sizeof(struct module_state),
    _cryio_methods,
    NULL,
    _cryio_traverse,
    _cryio_clear,
    NULL
};


PyMODINIT_FUNC PyInit__cryio(void) {
    PyObject *module;
    struct module_state *st;

    _cbf_decode_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&_cbf_decode_type) < 0)
        return NULL;

    _cbf_encode_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&_cbf_encode_type) < 0)
        return NULL;

    _esp_encode_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&_esp_encode_type) < 0)
        return NULL;

    _mar_decode_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&_mar_decode_type) < 0)
        return NULL;

    module = PyModule_Create(&moduledef);
    if (module == NULL)
        return NULL;
    st = GETSTATE(module);
    st->error = PyErr_NewException("_cryio.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&_cbf_decode_type);
    PyModule_AddObject(module, "_cbf_decode", (PyObject *)&_cbf_decode_type);

    Py_INCREF(&_cbf_encode_type);
    PyModule_AddObject(module, "_cbf_encode", (PyObject *)&_cbf_encode_type);

    Py_INCREF(&_esp_encode_type);
    PyModule_AddObject(module, "_esp_encode", (PyObject *)&_esp_encode_type);

    Py_INCREF(&_mar_decode_type);
    PyModule_AddObject(module, "_mar_decode", (PyObject *)&_mar_decode_type);

    return module;
}
