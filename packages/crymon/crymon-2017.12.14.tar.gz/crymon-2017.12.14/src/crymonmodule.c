/*
 * Different data format io routines
 */

#include <Python.h>
#include "ccp4.h"


typedef struct {
    PyObject_HEAD
    geometry *geo;
    PyObject *par_struct;
    PyObject *slice_struct;
    Py_buffer par_buf;
    Py_buffer slice_buf;
    Py_ssize_t shape[2];
    Py_ssize_t strides[2];
} _ccp4_encode;


static int
ccp4_encode_init(_ccp4_encode *self, PyObject *args) {
    geometry *geo = NULL;
    PyObject *slice = NULL, *tmp;
    enum int_type type;
    int ret;

    ccp4_destroy(self->geo);
    if (!PyArg_ParseTuple(args, "iO", &type, &slice))
        return -1;
    if (slice) {
        PyBuffer_Release(&self->slice_buf);
        tmp = self->slice_struct;
        Py_INCREF(slice);
        self->slice_struct = slice;
        Py_XDECREF(tmp);
    } else {
        PyErr_SetString(PyExc_TypeError, "Slice cannot be interpreted correctly");
        return -1;
    }
    ret = PyObject_GetBuffer(self->slice_struct, &self->slice_buf, PyBUF_C_CONTIGUOUS);
    if (ret < 0 || self->slice_buf.len != sizeof(t_slice)) {
        PyErr_SetString(PyExc_TypeError, "Slice cannot be interpreted correctly");
        return -1;
    }
    Py_BEGIN_ALLOW_THREADS
    geo = ccp4_init_geo(type, (t_slice *)self->slice_buf.buf);
    Py_END_ALLOW_THREADS
    if (geo == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory for CCP4 calculations");
        return -1;
    }
    self->geo = geo;
    return 0;
}


static PyObject *
ccp4_encode_init_par(_ccp4_encode *self, PyObject *args) {
    PyObject *par_struct = NULL, *tmp;
    int ret;

    if (!PyArg_ParseTuple(args, "O", &par_struct))
        return NULL;
    if (par_struct) {
        PyBuffer_Release(&self->par_buf);
        tmp = self->par_struct;
        Py_INCREF(par_struct);
        self->par_struct = par_struct;
        Py_XDECREF(tmp);
    } else {
        PyErr_SetString(PyExc_TypeError, "Parfile structure cannot be interpreted");
        return NULL;
    }
    ret = PyObject_GetBuffer(self->par_struct, &self->par_buf, PyBUF_C_CONTIGUOUS);
    if (ret < 0 || self->par_buf.len != sizeof(parfile)) {
        PyErr_SetString(PyExc_TypeError, "Parfile structure cannot be interpreted");
        return NULL;
    }
    self->geo->par = (parfile *)self->par_buf.buf;
    Py_BEGIN_ALLOW_THREADS
    ret = ccp4_init_par(self->geo);
    Py_END_ALLOW_THREADS
    if (ret < 0) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory for CCP4 calculations");
        return NULL;
    }
    Py_RETURN_NONE;
}


static void
ccp4_encode_dealloc(_ccp4_encode *self) {
    PyBuffer_Release(&self->slice_buf);
    Py_XDECREF(self->slice_struct);
    PyBuffer_Release(&self->par_buf);
    Py_XDECREF(self->par_struct);
    ccp4_destroy(self->geo);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyObject *
ccp4_encode_add(_ccp4_encode *self, PyObject *args) {
    float angle, osc;
    Py_buffer buf;
    PyObject *array;
    int ret;

    if (self->geo->map_calculated) {
        PyErr_SetString(PyExc_RuntimeError, "It is not possible to add another array if the map has been saved");
        return NULL;
    }

    if (!PyArg_ParseTuple(args, "Off", &array, &angle, &osc))
        return NULL;

    ret = PyObject_GetBuffer(array, &buf, PyBUF_C_CONTIGUOUS);
    if (ret < 0 || buf.len / buf.itemsize != self->geo->s_array) {
        PyBuffer_Release(&buf);
        PyErr_SetString(PyExc_ValueError, "Dimensions of the array are not consistent with the par file");
        return NULL;
    }
    Py_BEGIN_ALLOW_THREADS
    ccp4_add_array(self->geo, (float *)buf.buf, angle, osc);
    Py_END_ALLOW_THREADS
    PyBuffer_Release(&buf);
    Py_RETURN_NONE;
}


static int
ccp4_encode_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    _ccp4_encode *self = (_ccp4_encode *)obj;
    Py_BEGIN_ALLOW_THREADS
    ccp4_map(self->geo);
    Py_END_ALLOW_THREADS
    view->obj = (PyObject *)self;
    view->suboffsets = NULL;
    view->internal = NULL;
    switch (self->geo->type) {
        case volume:
            view->buf = (void *)self->geo->ccp4_hdr;
            view->len = (Py_ssize_t)self->geo->s_output;
            view->readonly = 1;
            view->itemsize = sizeof(char);
            view->format = "c";
            view->ndim = 0;
            view->shape = NULL;
            view->strides = NULL;
            break;
        case layer:
            view->buf = (void *)self->geo->voxels;
            view->len = (Py_ssize_t)(self->geo->s_voxels * sizeof(float));
            view->readonly = 1;
            view->itemsize = sizeof(float);
            view->format = "f";
            view->ndim = 2;
            self->shape[0] = self->shape[1] = (Py_ssize_t)self->geo->slice->n_voxels;
            self->strides[0] = (Py_ssize_t)(self->geo->slice->n_voxels * sizeof(float));
            self->strides[1] = (Py_ssize_t)sizeof(float);
            view->shape = self->shape;
            view->strides = self->strides;
            break;
        default:
            return -1;
    }
    Py_INCREF(self);
    return 0;
}


static PyBufferProcs _ccp4_encode_as_buffer = {
  (getbufferproc)ccp4_encode_getbuffer,
  (releasebufferproc)0,
};


static PyMethodDef _ccp4_encode_methods[] = {
    {"add", (PyCFunction)ccp4_encode_add, METH_VARARGS, "Add an array to the CCP4 map"},
    {"set_par", (PyCFunction)ccp4_encode_init_par, METH_VARARGS, "Set par structure for calculations"},
    {NULL}  /* Sentinel */
};


static PyTypeObject _ccp4_encode_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_crymon._ccp4_encode",                   /* tp_name */
    sizeof(_ccp4_encode),                     /* tp_basicsize */
    0,                                        /* tp_itemsize */
    (destructor)ccp4_encode_dealloc,          /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_reserved */
    0,                                        /* tp_repr */
    0,                                        /* tp_as_number */
    0,                                        /* tp_as_sequence */
    0,                                        /* tp_as_mapping */
    0,                                        /* tp_hash  */
    0,                                        /* tp_call */
    0,                                        /* tp_str */
    0,                                        /* tp_getattro */
    0,                                        /* tp_setattro */
    &_ccp4_encode_as_buffer,                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "_ccp4_encode object",                    /* tp_doc */
    0,                                        /* tp_traverse */
    0,                                        /* tp_clear */
    0,                                        /* tp_richcompare */
    0,                                        /* tp_weaklistoffset */
    0,                                        /* tp_iter */
    0,                                        /* tp_iternext */
    _ccp4_encode_methods,                     /* tp_methods */
    0,                                        /* tp_members */
    0,                                        /* tp_getset */
    0,                                        /* tp_base */
    0,                                        /* tp_dict */
    0,                                        /* tp_descr_get */
    0,                                        /* tp_descr_set */
    0,                                        /* tp_dictoffset */
    (initproc)ccp4_encode_init,               /* tp_init */
    0,                                        /* tp_alloc */
    PyType_GenericNew,                        /* tp_new */
};


static PyMethodDef _crymon_methods[] = {
    {NULL, NULL, 0, NULL}
};


struct module_state {
    PyObject *error;
};


#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))


static int _crymon_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}


static int _crymon_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_crymon",
    NULL,
    sizeof(struct module_state),
    _crymon_methods,
    NULL,
    _crymon_traverse,
    _crymon_clear,
    NULL
};


PyMODINIT_FUNC PyInit__crymon(void) {
    PyObject *module;
    struct module_state *st;

    if (PyType_Ready(&_ccp4_encode_type) < 0)
        return NULL;

    module = PyModule_Create(&moduledef);
    if (module == NULL)
        return NULL;
    st = GETSTATE(module);
    st->error = PyErr_NewException("_crymon.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&_ccp4_encode_type);
    PyModule_AddObject(module, "_ccp4_encode", (PyObject *)&_ccp4_encode_type);

    return module;
}
