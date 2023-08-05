
#include <openssl/err.h>

#ifdef _WIN32
#define PyErr_SetFromErrGeneric(x) PyErr_SetExcFromWindowsErr(x, 0)
#else
#define PyErr_SetFromErrGeneric(x) PyErr_SetFromErrno(x)
#endif

#include "nassl_errors.h"


PyObject *nassl_OpenSSLError_Exception;
static PyObject *nassl_SslError_Exception;
static PyObject *nassl_WantReadError_Exception;
static PyObject *nassl_WantWriteError_Exception;
static PyObject *nassl_WantX509LookupError_Exception;


PyObject* raise_OpenSSL_error()
{
    PyObject *pyFinalErrorString = NULL;
    PyObject *pyNewLineString = NULL;
    unsigned long iterateOpenSslError = 0;

    pyFinalErrorString = PyUnicode_FromString("");
    if (pyFinalErrorString == NULL)
    {
        return PyErr_NoMemory();
    }

    pyNewLineString = PyUnicode_FromString("\n");
    if (pyNewLineString == NULL)
    {
        return PyErr_NoMemory();
    }

    // Just queue all the errors in the error queue to create a giant error string
    // TODO: Improve error handling so we only return one single error; no sure if OpenSSL allows that...
    iterateOpenSslError = ERR_get_error();
    while(iterateOpenSslError != 0)
    {
        PyObject *oldPyFinalErrorString = NULL;
        // Get the current error string
        char *iterateErrorString = ERR_error_string(iterateOpenSslError, NULL);  // This includes a NUL character
        PyObject *pyIterateErrorString = PyUnicode_FromString(iterateErrorString);
        if (pyIterateErrorString == NULL)
            {
                return PyErr_NoMemory();
            }

        // Add it to our final error
        oldPyFinalErrorString = pyFinalErrorString;
        pyFinalErrorString = PyUnicode_Concat(pyFinalErrorString, pyIterateErrorString);
        if (pyFinalErrorString == NULL)
            {
                return PyErr_NoMemory();
            }
        Py_DECREF(oldPyFinalErrorString);

        // Add a new line
        oldPyFinalErrorString = pyFinalErrorString;
        pyFinalErrorString = PyUnicode_Concat(pyFinalErrorString, pyNewLineString);
        if (pyFinalErrorString == NULL)
            {
                return PyErr_NoMemory();
            }
        Py_DECREF(oldPyFinalErrorString);

        Py_DECREF(pyIterateErrorString);
        iterateOpenSslError = ERR_get_error();
    }

#if PY_MAJOR_VERSION >= 3
    PyErr_SetString(nassl_OpenSSLError_Exception, PyUnicode_AsUTF8(pyFinalErrorString));
#else
    PyErr_SetString(nassl_OpenSSLError_Exception, PyString_AsString(pyFinalErrorString));
#endif
    Py_DECREF(pyFinalErrorString);
    Py_DECREF(pyNewLineString);
    return NULL;
}


PyObject* raise_OpenSSL_ssl_error(SSL *ssl, int returnValue)
{
    // TODO: Better error handling
    int sslError = SSL_get_error(ssl, returnValue);
    switch(sslError)
    {
        case SSL_ERROR_NONE:
            break;

        case SSL_ERROR_SSL:
        	return raise_OpenSSL_error();

        case SSL_ERROR_SYSCALL:
            if (ERR_peek_error() == 0)
            {
                if (returnValue == 0)
                {
                    PyErr_SetString(nassl_SslError_Exception, "An EOF was observed that violates the protocol");
                    return NULL;
                }
                else if (returnValue == -1)
                {
                    PyErr_SetFromErrGeneric(nassl_SslError_Exception);
                    return NULL;
                }
                else
                {
                    PyErr_SetString(nassl_SslError_Exception, "SSL_ERROR_SYSCALL");
                    return NULL;
                }
            }
            else
            {
                return raise_OpenSSL_error();
            }

        case SSL_ERROR_ZERO_RETURN:
            PyErr_SetString(nassl_SslError_Exception, "Connection was shut down by peer");
            return NULL;

        case SSL_ERROR_WANT_WRITE:
            PyErr_SetString(nassl_WantWriteError_Exception, "");
            return NULL;

        case SSL_ERROR_WANT_READ:
            PyErr_SetString(nassl_WantReadError_Exception, "");
            return NULL;

        case SSL_ERROR_WANT_X509_LOOKUP:
            PyErr_SetString(nassl_WantX509LookupError_Exception, "");
            return NULL;

        default:
            PyErr_SetString(nassl_SslError_Exception, "TODO: Better error handling");
            return NULL;
    }
    Py_RETURN_NONE;
}


int module_add_errors(PyObject* m)
{
// We want both the modern and legacy nassl to use the same exceptions
#ifdef LEGACY_OPENSSL
    // In the legacy _nassl, we import these exceptions from the modern _nassl module
    PyObject* modern_nassl_module = PyImport_ImportModule("nassl._nassl");
    if (!modern_nassl_module)
    {
        PyErr_SetString(PyExc_RuntimeError, "Could not import _nassl");
        return 0;
    }

    nassl_OpenSSLError_Exception = PyDict_GetItemString(PyModule_GetDict(modern_nassl_module), "OpenSSLError");
    if (!nassl_OpenSSLError_Exception)
    {
        PyErr_SetString(PyExc_RuntimeError, "Could not import OpenSSLError from _nassl");
        return 0;
    }

    nassl_SslError_Exception = PyDict_GetItemString(PyModule_GetDict(modern_nassl_module), "SslError");
    if (!nassl_SslError_Exception)
    {
        PyErr_SetString(PyExc_RuntimeError, "Could not import SslError from _nassl");
        return 0;
    }

    nassl_WantWriteError_Exception = PyDict_GetItemString(PyModule_GetDict(modern_nassl_module), "WantWriteError");
    if (!nassl_WantWriteError_Exception)
    {
        PyErr_SetString(PyExc_RuntimeError, "Could not import WantWriteError from _nassl");
        return 0;
    }

    nassl_WantReadError_Exception = PyDict_GetItemString(PyModule_GetDict(modern_nassl_module), "WantReadError");
    if (!nassl_WantReadError_Exception)
    {
        PyErr_SetString(PyExc_RuntimeError, "Could not import WantReadError from _nassl");
        return 0;
    }

    nassl_WantX509LookupError_Exception = PyDict_GetItemString(PyModule_GetDict(modern_nassl_module), "WantX509LookupError");
    if (!nassl_WantX509LookupError_Exception)
    {
        PyErr_SetString(PyExc_RuntimeError, "Could not import WantX509LookupError from _nassl");
        return 0;
    }
#else
    // In the modern _nassl, we define these exceptions
    nassl_OpenSSLError_Exception = PyErr_NewException("nassl._nassl.OpenSSLError", NULL, NULL);
    Py_INCREF(nassl_OpenSSLError_Exception);
    PyModule_AddObject(m, "OpenSSLError", nassl_OpenSSLError_Exception);

    nassl_SslError_Exception = PyErr_NewException("nassl._nassl.SslError", nassl_OpenSSLError_Exception, NULL);
    Py_INCREF(nassl_SslError_Exception);
    PyModule_AddObject(m, "SslError", nassl_SslError_Exception);

    nassl_WantWriteError_Exception = PyErr_NewException("nassl._nassl.WantWriteError", nassl_SslError_Exception, NULL);
    Py_INCREF(nassl_WantWriteError_Exception);
    PyModule_AddObject(m, "WantWriteError", nassl_WantWriteError_Exception);

    nassl_WantReadError_Exception = PyErr_NewException("nassl._nassl.WantReadError", nassl_SslError_Exception, NULL);
    Py_INCREF(nassl_WantReadError_Exception);
    PyModule_AddObject(m, "WantReadError", nassl_WantReadError_Exception);

    nassl_WantX509LookupError_Exception = PyErr_NewException("nassl._nassl.WantX509LookupError", nassl_SslError_Exception, NULL);
    Py_INCREF(nassl_WantX509LookupError_Exception);
    PyModule_AddObject(m, "WantX509LookupError", nassl_WantX509LookupError_Exception);
#endif
    return 1;
}
