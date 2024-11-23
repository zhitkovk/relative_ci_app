# Welch and asymtptotic Z test

Welch test is mentioned everywhere. If you have unequal variances — use it, even if you're unsure whether you have them, still better stick to Welch, it is more robust etc.

Z test is usually mentioned either in the context of proportions test for 'big' data or in theoretical context of known variance.

But do we really see difference in practice? Is it unsafe to rely on asymptotics?

What question does this note answer? Should you abandon Welch's t-test? The answer is it depends on your data and it is better to carry out simulations for yourself, but in general, judging by the simulations if you expect asymptotic properties to hold, then you can probably just you the z-test.
