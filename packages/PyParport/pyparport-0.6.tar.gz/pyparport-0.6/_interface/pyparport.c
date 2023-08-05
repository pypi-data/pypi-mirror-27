#include <Python.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/io.h>

static PyObject* PortError;

static PyObject* readport(PyObject* self, PyObject *args)
{

    /* Open registers */
    ioperm(0x378,1,1);
    ioperm(0x379,1,1);
    ioperm(0x37A,1,1);

    char *reg;
    int addr;

    if (!PyArg_ParseTuple(args, "si", &reg, &addr))
    {
        return NULL;
    }

    PyArg_ParseTuple(args, "si", &reg, &addr);

    if (!strcmp(reg, "d"))
    {
        /* Set dataport to read mode */
        outb(255, addr+2);
        /* Read the port */
        return Py_BuildValue("i", inb(addr));
    }
    else if (!strcmp(reg, "s") | !strcmp(reg, "c"))
    {
        /* Read the port */
        return Py_BuildValue("i", inb(addr));
    }
    else
    {
        PyErr_SetString(PortError, "Please choose a valid register: d(ata), c(ontroll) or s(tatus)");
        return NULL;
    }
}

static PyObject* writeport(PyObject* self, PyObject *args)
{
    /* Open registers */
    ioperm(0x378,1,1);
    ioperm(0x379,1,1);
    ioperm(0x37A,1,1);

    int val;
    char *reg;
    int addr;

    if (!PyArg_ParseTuple(args, "isi", &val, &reg, &addr))
    {
        return NULL;
    }
    PyArg_ParseTuple(args, "isi", &val, &reg, &addr);

    if (!strcmp(reg, "d"))
    {
        /* Set dataport to write mode */
        outb(0, addr+2);
        /* Set the port */
        outb(val, addr);
    }
    else if (!strcmp(reg, "s") | !strcmp(reg, "c"))
    {
        /* Set the port */
        outb(val, addr);
    }
    else
    {
        PyErr_SetString(PortError, "Please choose a valid register: d(ata), c(ontroll) or s(tatus)");
        return NULL;
    }
    Py_RETURN_NONE;
}


static PyMethodDef pyparport_funcs[] = {
    {"read",    (PyCFunction)readport,  METH_VARARGS},
    {"write",   (PyCFunction)writeport, METH_VARARGS},
    {NULL}
};

#if PY_MAJOR_VERSION >= 3 // Python3 compatibilty
static struct PyModuleDef _interface =
{
    PyModuleDef_HEAD_INIT,
        "_interface",
        "Python parallel port object",
        -1,
        pyparport_funcs
};

PyMODINIT_FUNC PyInit__interface(void) {
    PyObject *module;
    module = PyModule_Create(&_interface);

    PortError = PyErr_NewException("pyparport.PortError", NULL, NULL);
    Py_INCREF(PortError);
    PyModule_AddObject(module, "PortError", PortError);

    return module;
}

#else // Python2 compatibilty
void init_interface(void)
{
    PyObject *module;
    module = Py_InitModule3("_interface", pyparport_funcs, "Python parallel port object");

    PortError = PyErr_NewException("pyparport.PortError", NULL, NULL);
    Py_INCREF(PortError);
    PyModule_AddObject(module, "PortError", PortError);
}
#endif
