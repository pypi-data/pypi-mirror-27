#include <gtest/gtest.h>

#include "goofit/Variable.h"
#include "goofit/UnbinnedDataSet.h"
#include "goofit/PDFs/physics/DP4Pdf.h"

using namespace GooFit;

TEST(DP4, Spline) {
    // Independent variable.

    Variable xvar{"xvar", 0, 10};
    Variable yvar{"yvar", 0, 10};

    // Data set
    UnbinnedDataSet data{{&xvar, &yvar}};

    xvar.setValue(1);
    yvar.setValue(2);
    data.addEvent();
}
