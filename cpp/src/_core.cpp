#include <nanobind/nanobind.h>

namespace nb = nanobind;

int add(int a, int b) {
    return a + b;
}

NB_MODULE(_core, m) {
    m.doc() = "qfold core C++ extension module";
    m.def("add", &add, "Add two integers", nb::arg("a"), nb::arg("b"));
}

