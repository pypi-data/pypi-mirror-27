#include "common.hpp"

#define N 4

PyObject * GLMVec4_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	GLMVec4 * self = (GLMVec4 *)type->tp_alloc(type, 0);

	if (self) {
	}

	return (PyObject *)self;
}

void GLMVec4_tp_dealloc(GLMVec4 * self) {
	Py_TYPE(self)->tp_free((PyObject *)self);
}

int GLMVec4_tp_init(GLMVec4 * self, PyObject * args, PyObject * kwargs) {
	PyObject * iterable;

	int args_ok = PyArg_ParseTuple(
		args,
		"O",
		&iterable
	);

	if (!args_ok) {
		return -1;
	}

	if (Py_TYPE(iterable) == &PyTuple_Type && PyTuple_GET_SIZE(iterable) == N) {
		self->val[0] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(iterable, 0));
		self->val[1] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(iterable, 1));
		self->val[2] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(iterable, 2));
		self->val[3] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(iterable, 3));

		if (PyErr_Occurred()) {
			return -1;
		}

		return 0;
	}

	self->val = vec4_from_iterable(iterable);

	if (PyErr_Occurred()) {
		return -1;
	}

	return 0;
}

PyObject * GLMVec4_tp_repr(GLMVec4 * self) {
	PyObject * temp = GLMVec4_Tuple(self);
	PyObject * res = PyObject_Repr(temp);
	Py_DECREF(temp);
	return res;
}

PyObject * GLMVec4_nb_add(PyObject * lhs, PyObject * rhs) {
	if (Py_TYPE(lhs) == &GLMVec4_Type && Py_TYPE(rhs) == &GLMVec4_Type) {
		GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
		res->val = ((GLMVec4 *)lhs)->val + ((GLMVec4 *)rhs)->val;
		return (PyObject *)res;
	}

	Py_RETURN_NOTIMPLEMENTED;
}

PyObject * GLMVec4_nb_subtract(PyObject * lhs, PyObject * rhs) {
	if (Py_TYPE(lhs) == &GLMVec4_Type && Py_TYPE(rhs) == &GLMVec4_Type) {
		GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
		res->val = ((GLMVec4 *)lhs)->val - ((GLMVec4 *)rhs)->val;
		return (PyObject *)res;
	}

	Py_RETURN_NOTIMPLEMENTED;
}

PyObject * GLMVec4_nb_multiply(PyObject * lhs, PyObject * rhs) {
	if (Py_TYPE(lhs) == &GLMVec4_Type && Py_TYPE(rhs) == &GLMVec4_Type) {
		GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
		res->val = ((GLMVec4 *)lhs)->val * ((GLMVec4 *)rhs)->val;
		return (PyObject *)res;
	}

	if (Py_TYPE(lhs) == &GLMVec4_Type) {
		float rhs_float = (float)PyFloat_AsDouble(rhs);
		if (!PyErr_Occurred()) {
			GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
			res->val = ((GLMVec4 *)lhs)->val * rhs_float;
			return (PyObject *)res;
		}
	}

	if (Py_TYPE(rhs) == &GLMVec4_Type) {
		glm::mat4 mat4_lhs = mat4_from_iterable(lhs);
		if (!PyErr_Occurred()) {
			GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
			res->val = mat4_lhs * ((GLMVec4 *)rhs)->val;
			return (PyObject *)res;
		}
	}

	PyErr_Clear();
	Py_RETURN_NOTIMPLEMENTED;
}

PyObject * GLMVec4_nb_true_divide(PyObject * lhs, PyObject * rhs) {
	if (Py_TYPE(lhs) == &GLMVec4_Type && Py_TYPE(rhs) == &GLMVec4_Type) {
		GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
		res->val = ((GLMVec4 *)lhs)->val / ((GLMVec4 *)rhs)->val;
		return (PyObject *)res;
	}

	if (Py_TYPE(lhs) == &GLMVec4_Type) {
		float rhs_float = (float)PyFloat_AsDouble(rhs);
		if (!PyErr_Occurred()) {
			GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
			res->val = ((GLMVec4 *)lhs)->val / rhs_float;
			return (PyObject *)res;
		}
	}

	PyErr_Clear();
	Py_RETURN_NOTIMPLEMENTED;
}

PyObject * GLMVec4_nb_inplace_add(PyObject * lhs, PyObject * rhs) {
	if (Py_TYPE(rhs) == &GLMVec4_Type) {
		((GLMVec4 *)lhs)->val += ((GLMVec4 *)rhs)->val;
		Py_INCREF(lhs);
		return lhs;
	}

	Py_RETURN_NOTIMPLEMENTED;
}

PyObject * GLMVec4_nb_inplace_subtract(PyObject * lhs, PyObject * rhs) {
	if (Py_TYPE(rhs) == &GLMVec4_Type) {
		((GLMVec4 *)lhs)->val -= ((GLMVec4 *)rhs)->val;
		Py_INCREF(lhs);
		return lhs;
	}

	Py_RETURN_NOTIMPLEMENTED;
}

PyObject * GLMVec4_nb_inplace_multiply(PyObject * lhs, PyObject * rhs) {
	if (Py_TYPE(rhs) == &GLMVec4_Type) {
		((GLMVec4 *)lhs)->val *= ((GLMVec4 *)rhs)->val;
		Py_INCREF(lhs);
		return lhs;
	}

	float rhs_float = (float)PyFloat_AsDouble(rhs);
	if (!PyErr_Occurred()) {
		((GLMVec4 *)lhs)->val *= rhs_float;
		Py_INCREF(lhs);
		return lhs;
	}

	PyErr_Clear();
	Py_RETURN_NOTIMPLEMENTED;
}

PyObject * GLMVec4_nb_inplace_true_divide(PyObject * lhs, PyObject * rhs) {
	if (Py_TYPE(rhs) == &GLMVec4_Type) {
		((GLMVec4 *)lhs)->val /= ((GLMVec4 *)rhs)->val;
		Py_INCREF(lhs);
		return lhs;
	}

	float rhs_float = (float)PyFloat_AsDouble(rhs);
	if (!PyErr_Occurred()) {
		((GLMVec4 *)lhs)->val /= rhs_float;
		Py_INCREF(lhs);
		return lhs;
	}

	PyErr_Clear();
	Py_RETURN_NOTIMPLEMENTED;
}

PyObject * GLMVec4_nb_negative(GLMVec4 * self) {
	GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
	res->val = -((GLMVec4 *)self)->val;
	return (PyObject *)res;
}

PyObject * GLMVec4_nb_positive(GLMVec4 * self) {
	GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
	res->val = +((GLMVec4 *)self)->val;
	return (PyObject *)res;
}

PyNumberMethods GLMVec4_tp_as_number = {
	(binaryfunc)GLMVec4_nb_add, // binaryfunc nb_add;
	(binaryfunc)GLMVec4_nb_subtract, // binaryfunc nb_subtract;
	(binaryfunc)GLMVec4_nb_multiply, // binaryfunc nb_multiply;
	0, // binaryfunc nb_remainder;
	0, // binaryfunc nb_divmod;
	0, // ternaryfunc nb_power;
	(unaryfunc)GLMVec4_nb_negative, // unaryfunc nb_negative;
	(unaryfunc)GLMVec4_nb_positive, // unaryfunc nb_positive;
	0, // unaryfunc nb_absolute;
	0, // inquiry nb_bool;
	0, // unaryfunc nb_invert;
	0, // binaryfunc nb_lshift;
	0, // binaryfunc nb_rshift;
	0, // binaryfunc nb_and;
	0, // binaryfunc nb_xor;
	0, // binaryfunc nb_or;
	0, // unaryfunc nb_int;
	0, // void *nb_reserved;
	0, // unaryfunc nb_float;
	(binaryfunc)GLMVec4_nb_inplace_add, // binaryfunc nb_inplace_add;
	(binaryfunc)GLMVec4_nb_inplace_subtract, // binaryfunc nb_inplace_subtract;
	(binaryfunc)GLMVec4_nb_inplace_multiply, // binaryfunc nb_inplace_multiply;
	0, // binaryfunc nb_inplace_remainder;
	0, // ternaryfunc nb_inplace_power;
	0, // binaryfunc nb_inplace_lshift;
	0, // binaryfunc nb_inplace_rshift;
	0, // binaryfunc nb_inplace_and;
	0, // binaryfunc nb_inplace_xor;
	0, // binaryfunc nb_inplace_or;
	0, // binaryfunc nb_floor_divide;
	(binaryfunc)GLMVec4_nb_true_divide, // binaryfunc nb_true_divide;
	0, // binaryfunc nb_inplace_floor_divide;
	(binaryfunc)GLMVec4_nb_inplace_true_divide, // binaryfunc nb_inplace_true_divide;
	0, // unaryfunc nb_index;
	// binaryfunc nb_matrix_multiply;
	// binaryfunc nb_inplace_matrix_multiply;
};

Py_ssize_t GLMVec4_sq_length(GLMVec4 * self) {
	return N;
}

PyObject * GLMVec4_sq_item(GLMVec4 * self, Py_ssize_t key) {
	if (key < N) {
		return PyFloat_FromDouble(self->val[key]);
	} else {
		return 0;
	}
}

int GLMVec4_sq_ass_item(GLMVec4 * self, Py_ssize_t key, PyObject * value) {
	if (key < N) {
		float x = (float)PyFloat_AsDouble(value);
		if (PyErr_Occurred()) {
			return -1;
		}
		self->val[key] = x;
		return 0;
	} else {
		return -1;
	}
}

PySequenceMethods GLMVec4_tp_as_sequence = {
	(lenfunc)GLMVec4_sq_length, // lenfunc sq_length;
	0, // binaryfunc sq_concat;
	0, // ssizeargfunc sq_repeat;
	(ssizeargfunc)GLMVec4_sq_item, // ssizeargfunc sq_item;
	0, // void *was_sq_slice;
	(ssizeobjargproc)GLMVec4_sq_ass_item, // ssizeobjargproc sq_ass_item;
	0, // void *was_sq_ass_slice;
	0, // objobjproc sq_contains;
	0, // binaryfunc sq_inplace_concat;
	0, // ssizeargfunc sq_inplace_repeat;
};

int GLMVec4_bf_getbuffer(GLMVec4 * self, Py_buffer * view, int flags) {
	view->buf = (void *)&self->val;
	view->len = sizeof(self->val);
	view->itemsize = 1;

	view->format = 0;
	view->ndim = 0;
	view->shape = 0;
	view->strides = 0;
	view->suboffsets = 0;

	Py_INCREF(self);
	view->obj = (PyObject *)self;
	return 0;
}

PyBufferProcs GLMVec4_tp_as_buffer = {
	(getbufferproc)GLMVec4_bf_getbuffer, // getbufferproc bf_getbuffer;
	0, // releasebufferproc bf_releasebuffer;
};

PyObject * GLMVec4_tp_meth_dot(GLMVec4 * lhs, PyObject * args) {
	PyObject * rhs = PyTuple_GetItem(args, 0);
	if (Py_TYPE(rhs) == &GLMVec4_Type) {
		return PyFloat_FromDouble(glm::dot(lhs->val, ((GLMVec4 *)rhs)->val));
	}
	return 0;
}

PyObject * GLMVec4_tp_meth_reflect(GLMVec4 * self, PyObject * args) {
	PyObject * norm = PyTuple_GetItem(args, 0);
	if (Py_TYPE(norm) == &GLMVec4_Type) {
		GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
		res->val = glm::reflect(self->val, ((GLMVec4 *)norm)->val);
		return (PyObject *)res;
	}
	return 0;
}

PyObject * GLMVec4_tp_meth_refract(GLMVec4 * self, PyObject * args) {
	PyObject * norm = PyTuple_GetItem(args, 0);
	float eta = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	if (PyErr_Occurred()) {
		return 0;
	}
	if (Py_TYPE(norm) == &GLMVec4_Type) {
		GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
		res->val = glm::refract(self->val, ((GLMVec4 *)norm)->val, eta);
		return (PyObject *)res;
	}
	return 0;
}

PyMethodDef GLMVec4_tp_methods[] = {
	{"dot", (PyCFunction)GLMVec4_tp_meth_dot, METH_VARARGS, 0},
	{"reflect", (PyCFunction)GLMVec4_tp_meth_reflect, METH_VARARGS, 0},
	{"refract", (PyCFunction)GLMVec4_tp_meth_refract, METH_VARARGS, 0},
	{0},
};

PyObject * GLMVec4_tp_get_length(GLMVec4 * self, void * closure) {
	return PyFloat_FromDouble(glm::length(self->val));
}

PyObject * GLMVec4_tp_get_normal(GLMVec4 * self, void * closure) {
	GLMVec4 * res = (GLMVec4 *)GLMVec4_tp_new(&GLMVec4_Type, 0, 0);
	res->val = glm::normalize(self->val);
	return (PyObject *)res;
}

PyObject * GLMVec4_tp_get_tup(GLMVec4 * self, void * closure) {
	return GLMVec4_Tuple(self);
}

PyObject * GLMVec4_tp_get_data(GLMVec4 * self, void * closure) {
	PyObject * res = PyBytes_FromStringAndSize(0, sizeof(self->val));
	memcpy(PyBytes_AS_STRING(res), &self->val, sizeof(self->val));
	return res;
}

PyGetSetDef GLMVec4_tp_getseters[] = {
	{(char *)"length", (getter)GLMVec4_tp_get_length, 0, 0, 0},
	{(char *)"normal", (getter)GLMVec4_tp_get_normal, 0, 0, 0},
	{(char *)"tup", (getter)GLMVec4_tp_get_tup, 0, 0, 0},
	{(char *)"data", (getter)GLMVec4_tp_get_data, 0, 0, 0},
	{0},
};

PyTypeObject GLMVec4_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"glm.Vec4", // tp_name
	sizeof(GLMVec4), // tp_basicsize
	0, // tp_itemsize
	(destructor)GLMVec4_tp_dealloc, // tp_dealloc
	0, // tp_print
	0, // tp_getattr
	0, // tp_setattr
	0, // tp_reserved
	(reprfunc)GLMVec4_tp_repr, // tp_repr
	&GLMVec4_tp_as_number, // tp_as_number
	&GLMVec4_tp_as_sequence, // tp_as_sequence
	0, // tp_as_mapping
	0, // tp_hash
	0, // tp_call
	0, // tp_str
	0, // tp_getattro
	0, // tp_setattro
	&GLMVec4_tp_as_buffer, // tp_as_buffer
	Py_TPFLAGS_DEFAULT, // tp_flags
	0, // tp_doc
	0, // tp_traverse
	0, // tp_clear
	0, // tp_richcompare
	0, // tp_weaklistoffset
	0, // tp_iter
	0, // tp_iternext
	GLMVec4_tp_methods, // tp_methods
	0, // tp_members
	GLMVec4_tp_getseters, // tp_getset
	0, // tp_base
	0, // tp_dict
	0, // tp_descr_get
	0, // tp_descr_set
	0, // tp_dictoffset
	(initproc)GLMVec4_tp_init, // tp_init
	0, // tp_alloc
	GLMVec4_tp_new, // tp_new
};

PyObject * GLMVec4_Tuple(GLMVec4 * self) {
	PyObject * tuple = PyTuple_New(N);
	PyTuple_SET_ITEM(tuple, 0, PyFloat_FromDouble(self->val[0]));
	PyTuple_SET_ITEM(tuple, 1, PyFloat_FromDouble(self->val[1]));
	PyTuple_SET_ITEM(tuple, 2, PyFloat_FromDouble(self->val[2]));
	PyTuple_SET_ITEM(tuple, 3, PyFloat_FromDouble(self->val[3]));
	return tuple;
}
