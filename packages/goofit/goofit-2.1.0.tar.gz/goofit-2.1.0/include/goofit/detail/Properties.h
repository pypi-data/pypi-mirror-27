#pragma once

namespace GooFit {

class PdfBase;

namespace Properties {

// Initial idea from https://stackoverflow.com/questions/8368512/does-c11-have-c-style-properties

class Constant {
public:
    Constant(PdfBase& self, fptype value) : value(value) {
        self._pindices.push_back(registrerConstants(1));
        MEMCPY_TO_SYMBOL(functorConstants, &value, sizeof(fptype), cIndex * sizeof(fptype), cudaMemcpyHostToDevice);

    }
    // fptype & operator = (const fptype &f) { return value = f; }
    operator fptype const & () const { return value; }
protected:
    fptype value;
};

} // namespace Properties
} // namespace GooFit
