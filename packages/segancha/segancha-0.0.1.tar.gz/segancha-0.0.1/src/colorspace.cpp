#include <cmath>
#include <color.h>
#include <constant.h>

namespace color {

double sgn(double val) { return (0. < val) - (val < 0.); }
constexpr inline double pow2(double x) { return x * x; }
constexpr inline double pow3(double x) { return x * x * x; }

RGB XYZtoRGB(const XYZ &xyz) {
  double r = xyz.x * A11 + xyz.y * A12 + xyz.z * A13;
  double g = xyz.x * A21 + xyz.y * A22 + xyz.z * A23;
  double b = xyz.x * A31 + xyz.y * A32 + xyz.z * A33;

  r = ((abs(r) > 0.0031308) ? sgn(r) * (1.055 * pow(abs(r), 1 / 2.4) - 0.055)
                            : (12.92 * r));
  g = ((abs(g) > 0.0031308) ? sgn(g) * (1.055 * pow(abs(g), 1 / 2.4) - 0.055)
                            : (12.92 * g));
  b = ((abs(b) > 0.0031308) ? sgn(b) * (1.055 * pow(abs(b), 1 / 2.4) - 0.055)
                            : (12.92 * b));

  return RGB{r, g, b};
}

XYZ LABtoXYZ(const LAB &lab) {
  double y = (lab.l + 16.0) / 116.0;
  double x = lab.a / 500.0 + y;
  double z = y - lab.b / 200.0;

  double x3 = pow3(x);
  double y3 = pow3(y);
  double z3 = pow3(z);

  x = ((x3 > 0.008856) ? x3 : ((x - 16.0 / 116.0) / 7.787)) * PCS_X;
  y = ((y3 > 0.008856) ? y3 : ((y - 16.0 / 116.0) / 7.787)) * PCS_Y;
  z = ((z3 > 0.008856) ? z3 : ((z - 16.0 / 116.0) / 7.787)) * PCS_Z;

  return XYZ{x, y, z};
}

LAB XYZtoLAB(const XYZ &xyz) {
  double x = xyz.x / PCS_X;
  double y = xyz.y / PCS_Y;
  double z = xyz.z / PCS_Z;

  double fx = x > 0.008856 ? pow(x, 1. / 3.) : (7.787 * x + 16. / 116.);
  double fy = y > 0.008856 ? pow(y, 1. / 3.) : (7.787 * y + 16. / 116.);
  double fz = z > 0.008856 ? pow(z, 1. / 3.) : (7.787 * z + 16. / 116.);

  double l = 116 * fy - 16;
  double a = 500 * (fx - fy);
  double b = 200 * (fy - fz);

  return LAB{l, a, b};
}

CMY RGBtoCMY(const RGB &rgb) {
  const double cr = 1 - rgb.r;
  const double cg = 1 - rgb.g;
  const double cb = 1 - rgb.b;
  double c = cr * B11 + cg * B12 + cb * B13;
  double m = cr * B21 + cg * B22 + cb * B23;
  double y = cr * B31 + cg * B32 + cb * B33;

  return CMY{c, m, y};
}

// http://www.brucelindbloom.com/index.html?Eqn_DIlluminant.html
XYZ IlluminantDKelvin(double T, double y) {
  double cx = T < 7000 ? (-4.6070e9 / pow3(T) + 2.9678e6 / pow2(T) +
                          0.09911e3 / T + 0.244063)
                       : (-2.0064e9 / pow3(T) + 1.9018e6 / pow2(T) +
                          0.24748e3 / T + 0.237040);
  return IlluminantDChromaticity(cx, y);
}

XYZ IlluminantDChromaticity(double cx, double y) {
  double cy = -3 * pow2(cx) + 2.87 * cx - 0.275;

  double x = cx * y / cy;
  double z = (1 - cx - cy) * y / cy;

  return XYZ{x, y, z};
}

} // namespace color

std::ostream &operator<<(std::ostream &s, const color::LAB &lab) {
  return (s << "LAB(" << lab.l << "," << lab.a << "," << lab.b << ")");
}

std::ostream &operator<<(std::ostream &s, const color::LCH &lch) {
  return (s << "LCH(" << lch.l << "," << lch.c << "," << lch.h << ")");
}

std::ostream &operator<<(std::ostream &s, const color::XYZ &xyz) {
  return (s << "XYZ(" << xyz.x << "," << xyz.y << "," << xyz.z << ")");
}

std::ostream &operator<<(std::ostream &s, const color::RGB &rgb) {
  return (s << "RGB(" << rgb.r << "," << rgb.g << "," << rgb.b << ")");
}

std::ostream &operator<<(std::ostream &s, const color::CMY &cmy) {
  return (s << "CMY(" << cmy.c << "," << cmy.m << "," << cmy.y << ")");
}
