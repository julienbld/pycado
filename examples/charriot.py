#unit ; cm

side = 5
width = .2
#length

def su_parallelogram (pt_origin, ve_1, ve_2)
  ln_1 = ln(pt_origin, ve_1)
  pt_2 = pt(ln_1, 1)
  ln_2 = ln(pt_2, ve_2)
  pt_3 = pt(ln_2, 1)
  ln_3 = ln(pt_3, -ve_1)
  pt_4 = pt(ln_3, 1)
  ln_4 = ln(pt_4, -ve_2)
  return su(ln_1, ln_2, ln_3, ln_4)

pt_0 = pt(0, 0, 0)
su_sqr_1 = su_parallelogram(pt_0, side*ve_x, side*ve_y)
pt_1 = pt(width, width, 0)
su_sqr_2 = su_parallelogram(pt_1, (side-2*width)*ve_x, (side-2*width)*ve_y)

su_section = su_sqr_1 - su_sqr_2

vo_pipe = vo_extrusion(sf_section, 20*ve_z)