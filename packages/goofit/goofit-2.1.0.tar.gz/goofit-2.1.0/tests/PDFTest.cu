#include "goofit/FitManager.h"
#include "goofit/UnbinnedDataSet.h"
#include "goofit/Variable.h"

#include "goofit/PDFs/basic/ExpPdf.h"
#include "goofit/PDFs/basic/GaussianPdf.h"

#include <random>
#include <memory>

#include "catch.hpp"

using namespace GooFit;

TEST_CASE("PDF run 1D tests truth", "[pdfs][truth]") {
    
    // Independent variable.
    Variable xvar{"xvar", 0, 10};
    
    // Data set
    UnbinnedDataSet data(&xvar);
    
    // PDF to fit
    std::unique_ptr<PdfBase> fittable;
    
    // Variables
    Variable a{"a", -1.5, 0.1, -10, 10};
    Variable b{"b", 2, 0.1, -10, 10};
    Variable c{"c", .5, 0.1, -10, 10};
    Variable d{"d", .75, 0.1, -10, 10};
    
    SECTION("ExpPdf") {
        // Prepare data
        std::mt19937 gen(137);
        std::exponential_distribution<> d(1.5);
        
        for(int i = 0; i < 1000; ++i) {
            xvar = d(gen);
            if(xvar) {
                data.addEvent();
            }
        }
        
        fittable.reset(new ExpPdf{"exppdf", &xvar, &a});
        
        a = -2; // Init value
    }
    SECTION("GaussPdf") {
        // Prepare data
        std::mt19937 gen(137);
        std::normal_distribution<> d(2,.5);
        
        for(int i = 0; i < 1000; ++i) {
            xvar = d(gen);
            if(xvar) {
                data.addEvent();
            }
        }
        
        fittable.reset(new GaussianPdf{"exppdf", &xvar, &b, &c});
        
        b = 1.6; // Init value
        c = .3;
    }
    
    fittable->fitTo(&data);
    
    CHECK(a == Approx(-1.5).epsilon(.05));
    CHECK(b == Approx(2).epsilon(.05));
    CHECK(c == Approx(.5).epsilon(.05));
    CHECK(d == Approx(.75).epsilon(.05));
    
}

class UniqueTestsFixture {
    
    
};
